import sys
from pathlib import Path
import random
import pygame

pygame.init()

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
LEVEL_DIR = BASE_DIR / "levels"

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 544
FPS = 60
TILE_SIZE = 32
GRAVITY = 0.65
MAX_LEVELS = 20

BLACK = (12, 13, 20)
BG_TOP = (18, 20, 34)
BG_BOTTOM = (34, 18, 40)
WHITE = (242, 244, 248)
TEXT = (223, 228, 240)
CYAN = (95, 230, 255)
GREEN = (110, 225, 135)
RED = (238, 75, 92)
YELLOW = (255, 220, 88)
PURPLE = (176, 116, 255)
ORANGE = (255, 160, 92)
SLATE = (55, 60, 80)
SLATE2 = (70, 76, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aden's Needle Trial")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 22)
big_font = pygame.font.SysFont(None, 56)


def clamp(value, low, high):
    return max(low, min(high, value))


def load_image(name, size=None):
    image = pygame.image.load(str(ASSET_DIR / name)).convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


PLAYER_ASSETS = {
    "idle": [load_image("aden_idle_0.png", (32, 48)), load_image("aden_idle_1.png", (32, 48))],
    "run": [load_image("aden_run_0.png", (32, 48)), load_image("aden_run_1.png", (32, 48))],
    "jump": load_image("aden_jump.png", (32, 48)),
    "dash": load_image("aden_dash.png", (32, 48)),
}
SLASH_IMAGE = load_image("slash.png", (54, 54))
WALKER_FRAMES = [load_image("enemy_walker_0.png", (28, 28)), load_image("enemy_walker_1.png", (28, 28))]
SHOOTER_FRAMES = [load_image("enemy_shooter_0.png", (28, 28)), load_image("enemy_shooter_1.png", (28, 28))]
BULLET_IMAGE = load_image("bullet.png", (14, 14))
HEART_IMAGE = load_image("heart.png", (22, 22))
TILE_IMAGE = load_image("tile_ground.png", (TILE_SIZE, TILE_SIZE))
CRUMBLE_IMAGE = load_image("tile_crumble.png", (TILE_SIZE, TILE_SIZE))
SPIKE_IMAGE = load_image("spike.png", (TILE_SIZE, TILE_SIZE))
CHECKPOINT_OFF = load_image("checkpoint_off.png", (24, 36))
CHECKPOINT_ON = load_image("checkpoint_on.png", (24, 36))
GOAL_IMAGE = load_image("goal.png", (28, 28))


class Particle:
    def __init__(self, x, y, color, vx, vy, life, radius):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.radius = radius

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.life -= 1

    def draw(self, surface, camera):
        if self.life <= 0:
            return
        ratio = self.life / self.max_life
        radius = max(1, int(self.radius * ratio))
        pygame.draw.circle(surface, self.color, (int(self.x - camera.x), int(self.y - camera.y)), radius)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target, world_width, world_height):
        desired_x = target.rect.centerx - SCREEN_WIDTH // 2
        desired_y = target.rect.centery - SCREEN_HEIGHT // 2
        self.x += (desired_x - self.x) * 0.08
        self.y += (desired_y - self.y) * 0.08
        self.x = clamp(self.x, 0, max(0, world_width - SCREEN_WIDTH))
        self.y = clamp(self.y, 0, max(0, world_height - SCREEN_HEIGHT))


class SolidTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = TILE_IMAGE
        self.rect = self.image.get_rect(topleft=(x, y))


class CrumbleTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = CRUMBLE_IMAGE
        self.rect = self.image.get_rect(topleft=(x, y))
        self.timer = None

    def trigger(self):
        if self.timer is None:
            self.timer = 20

    def update(self):
        if self.timer is not None:
            self.timer -= 1
            if self.timer <= 0:
                self.kill()


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = SPIKE_IMAGE
        self.rect = self.image.get_rect(topleft=(x, y))


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [GOAL_IMAGE, pygame.transform.flip(GOAL_IMAGE, True, False)]
        self.frame_index = 0
        self.anim_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x + 2, y + 2))

    def update(self):
        self.anim_timer += 1
        if self.anim_timer >= 20:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, index):
        super().__init__()
        self.index = index
        self.active = False
        self.image = CHECKPOINT_OFF
        self.rect = self.image.get_rect(midbottom=(x + TILE_SIZE // 2, y + TILE_SIZE))

    def activate(self):
        self.active = True
        self.image = CHECKPOINT_ON

    def deactivate(self):
        self.active = False
        self.image = CHECKPOINT_OFF


class SlashEffect(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.facing = player.facing
        self.image = SLASH_IMAGE if self.facing > 0 else pygame.transform.flip(SLASH_IMAGE, True, False)
        offset_x = 24 if self.facing > 0 else -54
        self.rect = self.image.get_rect(topleft=(player.rect.x + offset_x, player.rect.y - 2))
        self.hitbox = pygame.Rect(self.rect.x + 8, self.rect.y + 10, self.rect.width - 16, self.rect.height - 20)
        self.timer = 8

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 6 * direction

    def update(self, solids):
        self.rect.x += self.vx
        if pygame.sprite.spritecollideany(self, solids):
            self.kill()
        if self.rect.right < 0 or self.rect.left > 100000:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.anim_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.health = 1
        self.direction = -1

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer >= 18:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            if self.direction > 0:
                self.image = pygame.transform.flip(self.image, True, False)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0


class WalkerEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x + 2, y + 4, WALKER_FRAMES)
        self.vel_x = -1.2

    def update(self, solids):
        self.animate()
        self.vel_y += GRAVITY * 0.6
        self.vel_y = clamp(self.vel_y, -10, 8)

        self.rect.x += int(round(self.vel_x))
        collided = pygame.sprite.spritecollide(self, solids, False)
        for tile in collided:
            if self.vel_x > 0:
                self.rect.right = tile.rect.left
                self.vel_x *= -1
                self.direction = -1
            elif self.vel_x < 0:
                self.rect.left = tile.rect.right
                self.vel_x *= -1
                self.direction = 1

        self.rect.y += int(round(self.vel_y))
        collided = pygame.sprite.spritecollide(self, solids, False)
        grounded = False
        for tile in collided:
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                grounded = True
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

        if grounded:
            front_x = self.rect.centerx + (14 if self.vel_x > 0 else -14)
            test_rect = pygame.Rect(front_x, self.rect.bottom + 1, 4, 4)
            if not any(test_rect.colliderect(tile.rect) for tile in solids):
                self.vel_x *= -1
                self.direction *= -1


class ShooterEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x + 2, y + 2, SHOOTER_FRAMES)
        self.cooldown = random.randint(50, 90)

    def update(self, solids, bullets, player):
        self.animate()
        self.cooldown -= 1
        self.direction = 1 if player.rect.centerx >= self.rect.centerx else -1
        if self.cooldown <= 0 and abs(player.rect.centerx - self.rect.centerx) < 500:
            bullets.add(Bullet(self.rect.centerx, self.rect.centery, self.direction))
            self.cooldown = random.randint(75, 120)


class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.anim_state = "idle"
        self.frame_index = 0
        self.anim_timer = 0
        self.image = PLAYER_ASSETS["idle"][0]
        self.rect = pygame.Rect(spawn_x, spawn_y, 24, 42)
        self.draw_offset_y = -6
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.facing = 1
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.speed = 3.8
        self.accel = 0.7
        self.friction = 0.75
        self.jump_power = -11.8
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.can_dash = True
        self.attack_cooldown = 0
        self.invincible_timer = 0
        self.max_hp = 3
        self.hp = 3
        self.dead = False

    def set_spawn(self, x, y):
        self.spawn_x = x
        self.spawn_y = y

    def request_jump(self):
        self.jump_buffer = 10

    def request_dash(self):
        if self.can_dash and self.dash_cooldown <= 0:
            self.dash_timer = 8
            self.dash_cooldown = 24
            self.can_dash = False
            self.vel_x = self.facing * 9.5
            self.vel_y = 0

    def request_attack(self, slash_group):
        if self.attack_cooldown <= 0:
            slash_group.add(SlashEffect(self))
            self.attack_cooldown = 18

    def take_damage(self, amount=1):
        if self.invincible_timer > 0:
            return False
        self.hp -= amount
        self.invincible_timer = 60
        return self.hp <= 0

    def respawn(self):
        self.pos_x = float(self.spawn_x)
        self.pos_y = float(self.spawn_y)
        self.rect.topleft = (self.spawn_x, self.spawn_y)
        self.vel_x = 0
        self.vel_y = 0
        self.hp = self.max_hp
        self.invincible_timer = 60
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.can_dash = True

    def _update_animation(self):
        if self.dash_timer > 0:
            self.anim_state = "dash"
            self.image = PLAYER_ASSETS["dash"]
        elif not self.on_ground:
            self.anim_state = "jump"
            self.image = PLAYER_ASSETS["jump"]
        elif abs(self.vel_x) > 0.4:
            self.anim_state = "run"
            self.anim_timer += 1
            if self.anim_timer >= 10:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(PLAYER_ASSETS["run"])
            self.image = PLAYER_ASSETS["run"][self.frame_index]
        else:
            self.anim_state = "idle"
            self.anim_timer += 1
            if self.anim_timer >= 24:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(PLAYER_ASSETS["idle"])
            self.image = PLAYER_ASSETS["idle"][self.frame_index]
        if self.facing < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def _move_and_collide(self, solids, crumble_group):
        self.pos_x += self.vel_x
        self.rect.x = int(round(self.pos_x))
        hits = pygame.sprite.spritecollide(self, solids, False)
        for tile in hits:
            if self.vel_x > 0:
                self.rect.right = tile.rect.left
            elif self.vel_x < 0:
                self.rect.left = tile.rect.right
            self.pos_x = self.rect.x
            self.vel_x = 0

        prev_bottom = self.rect.bottom
        self.pos_y += self.vel_y
        self.rect.y = int(round(self.pos_y))
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, solids, False)
        for tile in hits:
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
                self.pos_y = self.rect.y
                self.vel_y = 0
                self.on_ground = True
                self.can_dash = True
                if isinstance(tile, CrumbleTile):
                    tile.trigger()
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
                self.pos_y = self.rect.y
                self.vel_y = 0
        if not self.on_ground and prev_bottom == self.rect.bottom:
            pass

        for tile in crumble_group:
            if self.rect.colliderect(tile.rect) and self.rect.bottom <= tile.rect.bottom:
                tile.trigger()

    def update(self, solids, crumble_group):
        keys = pygame.key.get_pressed()
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        if left and not right:
            self.vel_x -= self.accel
            self.facing = -1
        elif right and not left:
            self.vel_x += self.accel
            self.facing = 1
        elif left and right:
            self.vel_x *= 0.92
        else:
            self.vel_x *= self.friction
            if abs(self.vel_x) < 0.08:
                self.vel_x = 0

        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.coyote_timer > 0:
            self.coyote_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if self.jump_buffer > 0 and (self.on_ground or self.coyote_timer > 0):
            self.vel_y = self.jump_power
            self.jump_buffer = 0
            self.on_ground = False
            self.coyote_timer = 0

        if self.dash_timer > 0:
            self.dash_timer -= 1
        else:
            self.vel_y += GRAVITY

        self.vel_x = clamp(self.vel_x, -self.speed if self.dash_timer <= 0 else -9.5, self.speed if self.dash_timer <= 0 else 9.5)
        self.vel_y = clamp(self.vel_y, -15, 12)

        was_on_ground = self.on_ground
        self._move_and_collide(solids, crumble_group)
        if was_on_ground and not self.on_ground and self.vel_y >= 0:
            self.coyote_timer = 8

        self._update_animation()

    def draw(self, surface, camera):
        if self.invincible_timer > 0 and self.invincible_timer % 6 < 3:
            alpha_img = self.image.copy()
            alpha_img.set_alpha(130)
            surface.blit(alpha_img, (self.rect.x - camera.x - 4, self.rect.y - camera.y + self.draw_offset_y))
        else:
            surface.blit(self.image, (self.rect.x - camera.x - 4, self.rect.y - camera.y + self.draw_offset_y))


class Level:
    def __init__(self, path):
        self.path = path
        self.solids = pygame.sprite.Group()
        self.crumble = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.shooters = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.all_tiles = pygame.sprite.Group()
        self.player_spawn = (64, 64)
        self.width = 0
        self.height = 0
        self.name = path.stem.replace("_", " ").title()
        self._load()

    def _load(self):
        rows = [line.rstrip("\n") for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip() != ""]
        self.height = len(rows) * TILE_SIZE
        self.width = max(len(row) for row in rows) * TILE_SIZE if rows else SCREEN_WIDTH

        checkpoint_index = 0
        for y, row in enumerate(rows):
            for x, cell in enumerate(row):
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE
                if cell == "#":
                    tile = SolidTile(world_x, world_y)
                    self.solids.add(tile)
                    self.all_tiles.add(tile)
                elif cell == "B":
                    tile = CrumbleTile(world_x, world_y)
                    self.solids.add(tile)
                    self.crumble.add(tile)
                    self.all_tiles.add(tile)
                elif cell == "^":
                    self.hazards.add(Spike(world_x, world_y))
                elif cell == "P":
                    self.player_spawn = (world_x + 4, world_y - 10)
                elif cell == "G":
                    self.goal.add(Goal(world_x + 2, world_y + 2))
                elif cell == "C":
                    cp = Checkpoint(world_x, world_y, checkpoint_index)
                    checkpoint_index += 1
                    self.checkpoints.add(cp)
                elif cell == "E":
                    self.enemies.add(WalkerEnemy(world_x, world_y))
                elif cell == "S":
                    shooter = ShooterEnemy(world_x, world_y)
                    self.enemies.add(shooter)
                    self.shooters.add(shooter)

    def update(self, player):
        self.crumble.update()
        self.goal.update()
        for enemy in self.enemies:
            if isinstance(enemy, WalkerEnemy):
                enemy.update(self.solids)
            elif isinstance(enemy, ShooterEnemy):
                enemy.update(self.solids, self.enemy_bullets, player)
        for bullet in list(self.enemy_bullets):
            bullet.update(self.solids)

    def draw(self, surface, camera):
        for tile in self.all_tiles:
            surface.blit(tile.image, (tile.rect.x - camera.x, tile.rect.y - camera.y))
        for cp in self.checkpoints:
            surface.blit(cp.image, (cp.rect.x - camera.x, cp.rect.y - camera.y))
        for goal in self.goal:
            surface.blit(goal.image, (goal.rect.x - camera.x, goal.rect.y - camera.y))
        for hazard in self.hazards:
            surface.blit(hazard.image, (hazard.rect.x - camera.x, hazard.rect.y - camera.y))
        for enemy in self.enemies:
            surface.blit(enemy.image, (enemy.rect.x - camera.x, enemy.rect.y - camera.y))
        for bullet in self.enemy_bullets:
            surface.blit(bullet.image, (bullet.rect.x - camera.x, bullet.rect.y - camera.y))


class Game:
    def __init__(self):
        self.level_paths = sorted(LEVEL_DIR.glob("level_*.txt"))
        self.current_level_index = 0
        self.level = None
        self.player = None
        self.camera = Camera()
        self.particles = []
        self.slashes = pygame.sprite.Group()
        self.deaths = 0
        self.checkpoint_label = "Start"
        self.state = "title"
        self._load_level(0)

    def _spawn_particles(self, x, y, color, amount=12):
        for _ in range(amount):
            vx = random.uniform(-2.5, 2.5)
            vy = random.uniform(-3.8, 0.2)
            self.particles.append(Particle(x, y, color, vx, vy, random.randint(16, 28), random.randint(2, 4)))

    def _load_level(self, index, keep_deaths=True):
        if not keep_deaths:
            self.deaths = 0
        self.current_level_index = index
        self.level = Level(self.level_paths[index])
        self.player = Player(*self.level.player_spawn)
        self.camera = Camera()
        self.slashes.empty()
        self.checkpoint_label = "Start"
        self._spawn_particles(self.player.rect.centerx, self.player.rect.centery, CYAN, 18)

    def _activate_checkpoint(self, target_cp):
        for cp in self.level.checkpoints:
            cp.deactivate()
        target_cp.activate()
        self.player.set_spawn(target_cp.rect.x, target_cp.rect.y - 6)
        self.checkpoint_label = f"CP-{target_cp.index + 1}"
        self._spawn_particles(target_cp.rect.centerx, target_cp.rect.centery, YELLOW, 14)

    def _respawn_player(self):
        self.deaths += 1
        self._spawn_particles(self.player.rect.centerx, self.player.rect.centery, RED, 24)
        self.player.respawn()

    def _handle_collisions(self):
        if pygame.sprite.spritecollideany(self.player, self.level.hazards):
            self._respawn_player()
            return

        enemy_touch = pygame.sprite.spritecollideany(self.player, self.level.enemies)
        if enemy_touch and self.player.take_damage(1):
            self._respawn_player()
            return

        bullet_hit = pygame.sprite.spritecollideany(self.player, self.level.enemy_bullets)
        if bullet_hit:
            bullet_hit.kill()
            if self.player.take_damage(1):
                self._respawn_player()
                return
            self._spawn_particles(self.player.rect.centerx, self.player.rect.centery, PURPLE, 8)

        for cp in pygame.sprite.spritecollide(self.player, self.level.checkpoints, False):
            if not cp.active:
                self._activate_checkpoint(cp)

        if pygame.sprite.spritecollideany(self.player, self.level.goal):
            if self.current_level_index + 1 < len(self.level_paths):
                self.state = "stage_clear"
                self._spawn_particles(self.player.rect.centerx, self.player.rect.centery, GREEN, 30)
            else:
                self.state = "game_clear"
                self._spawn_particles(self.player.rect.centerx, self.player.rect.centery, CYAN, 50)

    def _handle_attack_hits(self):
        for slash in list(self.slashes):
            for enemy in [e for e in self.level.enemies if slash.hitbox.colliderect(e.rect)]:
                if enemy.take_damage():
                    self._spawn_particles(enemy.rect.centerx, enemy.rect.centery, GREEN, 16)
                    enemy.kill()
            for bullet in [b for b in self.level.enemy_bullets if slash.hitbox.colliderect(b.rect)]:
                self._spawn_particles(bullet.rect.centerx, bullet.rect.centery, PURPLE, 8)
                bullet.kill()

    def _update_particles(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def _draw_background(self):
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
            g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
            b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        start_x = int(-self.camera.x) % 48
        start_y = int(-self.camera.y) % 48
        for x in range(start_x, SCREEN_WIDTH, 48):
            pygame.draw.line(screen, (30, 34, 50), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(start_y, SCREEN_HEIGHT, 48):
            pygame.draw.line(screen, (30, 34, 50), (0, y), (SCREEN_WIDTH, y))

    def _draw_hud(self):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, 70))
        pygame.draw.line(screen, SLATE2, (0, 70), (SCREEN_WIDTH, 70), 2)
        draw_text = screen.blit
        title = font.render("Aden's Needle Trial", True, WHITE)
        info = small_font.render("Move: ←/→ or A/D   Jump: Z/Space   Dash: Shift   Attack: X/J   Respawn: R", True, CYAN)
        stage = small_font.render(f"Stage {self.current_level_index + 1}/{len(self.level_paths)}", True, YELLOW)
        deaths = small_font.render(f"Deaths {self.deaths}", True, TEXT)
        cp = small_font.render(f"Checkpoint {self.checkpoint_label}", True, TEXT)
        draw_text(title, (18, 12))
        draw_text(info, (18, 40))
        draw_text(stage, (780, 12))
        draw_text(deaths, (780, 34))
        draw_text(cp, (780, 52))
        for i in range(self.player.hp):
            screen.blit(HEART_IMAGE, (640 + i * 24, 12))

    def _draw_slashes(self):
        for slash in self.slashes:
            screen.blit(slash.image, (slash.rect.x - self.camera.x, slash.rect.y - self.camera.y))

    def _draw_center_panel(self, title_text, body_text, sub_text):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        box = pygame.Rect(180, 150, 600, 210)
        pygame.draw.rect(screen, (18, 20, 30), box, border_radius=14)
        pygame.draw.rect(screen, PURPLE, box, 3, border_radius=14)
        title = big_font.render(title_text, True, GREEN)
        body = font.render(body_text, True, WHITE)
        sub = small_font.render(sub_text, True, CYAN)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 205)))
        screen.blit(body, body.get_rect(center=(SCREEN_WIDTH // 2, 260)))
        screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 312)))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.state == "title":
                    self.state = "playing"
                    continue
                if self.state == "playing":
                    if event.key in (pygame.K_z, pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.player.request_jump()
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_c):
                        self.player.request_dash()
                    if event.key in (pygame.K_x, pygame.K_j):
                        self.player.request_attack(self.slashes)
                    if event.key == pygame.K_r:
                        self._respawn_player()
                elif self.state == "stage_clear":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._load_level(self.current_level_index + 1)
                        self.state = "playing"
                elif self.state == "game_clear":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._load_level(0, keep_deaths=False)
                        self.state = "playing"

    def update(self):
        if self.state != "playing":
            self._update_particles()
            return
        self.player.update(self.level.solids, self.level.crumble)
        self.level.update(self.player)
        self.slashes.update()
        self._handle_attack_hits()
        self._handle_collisions()
        if self.player.rect.top > self.level.height + 200:
            self._respawn_player()
        self._update_particles()
        self.camera.update(self.player, self.level.width, self.level.height)

    def draw(self):
        self._draw_background()
        self.level.draw(screen, self.camera)
        self._draw_slashes()
        self.player.draw(screen, self.camera)
        for particle in self.particles:
            particle.draw(screen, self.camera)
        self._draw_hud()

        if self.state == "title":
            self._draw_center_panel(
                "aden",
                "Pixel hero based on your photo. Beat 20 text-map stages.",
                "Press any key to start",
            )
        elif self.state == "stage_clear":
            self._draw_center_panel(
                "STAGE CLEAR",
                f"You cleared stage {self.current_level_index + 1}.",
                "Press Enter or Space for the next stage",
            )
        elif self.state == "game_clear":
            self._draw_center_panel(
                "ALL CLEAR",
                f"Aden conquered all {len(self.level_paths)} stages.",
                "Press Enter or Space to restart from stage 1",
            )


def main():
    game = Game()
    while True:
        clock.tick(FPS)
        game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
