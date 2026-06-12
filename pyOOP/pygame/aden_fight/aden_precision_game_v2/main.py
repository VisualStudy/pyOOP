
import sys
from pathlib import Path
import random
import math
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
SLATE2 = (70, 76, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aden's Needle Trial v2")
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


def draw_text(text, x, y, color=WHITE, font_obj=font, center=False):
    image = font_obj.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


PLAYER_ASSETS = {
    "idle": [load_image("aden_idle_0.png", (40, 56)), load_image("aden_idle_1.png", (40, 56))],
    "run": [
        load_image("aden_run_0.png", (40, 56)),
        load_image("aden_run_1.png", (40, 56)),
        load_image("aden_run_2.png", (40, 56)),
        load_image("aden_run_3.png", (40, 56)),
    ],
    "jump": load_image("aden_jump.png", (40, 56)),
    "fall": load_image("aden_fall.png", (40, 56)),
    "dash": load_image("aden_dash.png", (40, 56)),
    "shoot": load_image("aden_shoot.png", (40, 56)),
}

ADEN_SHOT = load_image("aden_shot.png", (28, 18))
ENEMY_BULLET = load_image("enemy_bullet.png", (18, 18))
WALKER_FRAMES = [load_image("enemy_walker_0.png", (34, 30)), load_image("enemy_walker_1.png", (34, 30))]
SHOOTER_FRAMES = [load_image("enemy_shooter_0.png", (34, 34)), load_image("enemy_shooter_1.png", (34, 34))]
BOSS_FRAMES = [load_image(f"boss_{i}.png", (128, 96)) for i in range(4)]

HEART_IMAGE = load_image("heart.png", (22, 22))
TILE_IMAGE = load_image("tile_ground.png", (TILE_SIZE, TILE_SIZE))
CRUMBLE_IMAGE = load_image("tile_crumble.png", (TILE_SIZE, TILE_SIZE))
SPIKE_IMAGE = load_image("spike.png", (TILE_SIZE, TILE_SIZE))
CHECKPOINT_OFF = load_image("checkpoint_off.png", (24, 36))
CHECKPOINT_ON = load_image("checkpoint_on.png", (24, 36))
PORTAL_FRAMES = [load_image(f"portal_{i}.png", (96, 128)) for i in range(6)]


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

    def draw(self, camera):
        if self.life <= 0:
            return
        ratio = self.life / self.max_life
        radius = max(1, int(self.radius * ratio))
        pygame.draw.circle(screen, self.color, (int(self.x - camera.x), int(self.y - camera.y)), radius)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shake_time = 0
        self.shake_power = 0

    def shake(self, time=10, power=4):
        self.shake_time = time
        self.shake_power = power

    def update(self, target, world_width, world_height):
        desired_x = target.rect.centerx - SCREEN_WIDTH // 2
        desired_y = target.rect.centery - SCREEN_HEIGHT // 2
        self.x += (desired_x - self.x) * 0.08
        self.y += (desired_y - self.y) * 0.08
        self.x = clamp(self.x, 0, max(0, world_width - SCREEN_WIDTH))
        self.y = clamp(self.y, 0, max(0, world_height - SCREEN_HEIGHT))

        if self.shake_time > 0:
            self.shake_time -= 1
            self.x += random.randint(-self.shake_power, self.shake_power)
            self.y += random.randint(-self.shake_power, self.shake_power)


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
            self.timer = 25

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


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = PORTAL_FRAMES
        self.frame_index = 0
        self.timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(x + TILE_SIZE // 2, y + TILE_SIZE))

    def update(self):
        self.timer += 1
        if self.timer >= 7:
            self.timer = 0
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


class PlayerShot(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.image = ADEN_SHOT if direction > 0 else pygame.transform.flip(ADEN_SHOT, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 11 * direction
        self.life = 70
        self.damage = 1

    def update(self, solids):
        self.rect.x += self.vx
        self.life -= 1
        if self.life <= 0 or pygame.sprite.spritecollideany(self, solids):
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy=0):
        super().__init__()
        self.image = ENEMY_BULLET
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.life = 180

    def update(self, solids):
        self.rect.x += int(round(self.vx))
        self.rect.y += int(round(self.vy))
        self.life -= 1
        if self.life <= 0 or pygame.sprite.spritecollideany(self, solids):
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
        if self.anim_timer >= 16:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        image = self.frames[self.frame_index]
        if self.direction > 0:
            image = pygame.transform.flip(image, True, False)
        self.image = image

    def take_damage(self, amount=1):
        self.health -= amount
        return self.health <= 0


class WalkerEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y + 2, WALKER_FRAMES)
        self.vel_x = -1.4
        self.health = 2

    def update(self, solids, bullets, player):
        self.animate()
        self.vel_y += GRAVITY * 0.55
        self.vel_y = clamp(self.vel_y, -10, 8)

        self.rect.x += int(round(self.vel_x))
        hits = pygame.sprite.spritecollide(self, solids, False)
        for tile in hits:
            if self.vel_x > 0:
                self.rect.right = tile.rect.left
                self.vel_x *= -1
                self.direction = -1
            elif self.vel_x < 0:
                self.rect.left = tile.rect.right
                self.vel_x *= -1
                self.direction = 1

        self.rect.y += int(round(self.vel_y))
        hits = pygame.sprite.spritecollide(self, solids, False)
        grounded = False
        for tile in hits:
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                grounded = True
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

        if grounded:
            front_x = self.rect.centerx + (18 if self.vel_x > 0 else -18)
            test = pygame.Rect(front_x, self.rect.bottom + 2, 4, 4)
            if not any(test.colliderect(t.rect) for t in solids):
                self.vel_x *= -1
                self.direction *= -1


class ShooterEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, SHOOTER_FRAMES)
        self.health = 2
        self.cooldown = random.randint(45, 90)

    def update(self, solids, bullets, player):
        self.animate()
        self.direction = 1 if player.rect.centerx >= self.rect.centerx else -1
        self.cooldown -= 1
        if self.cooldown <= 0 and abs(player.rect.centerx - self.rect.centerx) < 560:
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, 5.3 * self.direction))
            self.cooldown = random.randint(70, 110)


class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x - 48, y - 58, BOSS_FRAMES)
        self.health = 24
        self.max_health = 24
        self.cooldown = 40
        self.move_timer = 0
        self.base_y = self.rect.y
        self.direction = 1

    def update(self, solids, bullets, player):
        self.animate()
        self.move_timer += 1
        self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
        self.rect.y = self.base_y + int(math.sin(self.move_timer * 0.045) * 28)
        self.cooldown -= 1

        if self.cooldown <= 0:
            # radial-ish pattern, avoid too many bullets
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, math.hypot(dx, dy))
            speed = 4.2
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, 4.5 * self.direction, -1.8))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, 4.5 * self.direction, 1.8))
            self.cooldown = 42 if self.health > self.max_health // 2 else 30


class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.frame_index = 0
        self.anim_timer = 0
        self.shoot_timer = 0
        self.image = PLAYER_ASSETS["idle"][0]
        self.rect = pygame.Rect(spawn_x, spawn_y, 24, 42)
        self.draw_offset_x = -8
        self.draw_offset_y = -11
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.facing = 1
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.speed = 4.0
        self.accel = 0.72
        self.friction = 0.76
        self.jump_power = -11.8
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.can_dash = True
        self.shoot_cooldown = 0
        self.invincible_timer = 0
        self.max_hp = 4
        self.hp = 4

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
            self.vel_x = self.facing * 10
            self.vel_y = 0

    def request_shoot(self, shot_group):
        if self.shoot_cooldown <= 0:
            shot_x = self.rect.centerx + self.facing * 18
            shot_y = self.rect.centery - 4
            shot_group.add(PlayerShot(shot_x, shot_y, self.facing))
            self.shoot_cooldown = 12
            self.shoot_timer = 8

    def take_damage(self, amount=1):
        if self.invincible_timer > 0:
            return False
        self.hp -= amount
        self.invincible_timer = 55
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

        was_grounded = self.on_ground
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

        if was_grounded and not self.on_ground and self.vel_y >= 0:
            self.coyote_timer = 8

        for tile in crumble_group:
            if self.rect.colliderect(tile.rect) and self.rect.bottom <= tile.rect.bottom + 2:
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
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
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

        speed_limit = self.speed if self.dash_timer <= 0 else 10
        self.vel_x = clamp(self.vel_x, -speed_limit, speed_limit)
        self.vel_y = clamp(self.vel_y, -15, 12)

        self._move_and_collide(solids, crumble_group)
        self._update_animation()

    def _update_animation(self):
        if self.shoot_timer > 0:
            image = PLAYER_ASSETS["shoot"]
        elif self.dash_timer > 0:
            image = PLAYER_ASSETS["dash"]
        elif not self.on_ground and self.vel_y < 0:
            image = PLAYER_ASSETS["jump"]
        elif not self.on_ground and self.vel_y >= 0:
            image = PLAYER_ASSETS["fall"]
        elif abs(self.vel_x) > 0.35:
            self.anim_timer += 1
            if self.anim_timer >= 7:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(PLAYER_ASSETS["run"])
            image = PLAYER_ASSETS["run"][self.frame_index]
        else:
            self.anim_timer += 1
            if self.anim_timer >= 22:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(PLAYER_ASSETS["idle"])
            image = PLAYER_ASSETS["idle"][self.frame_index % len(PLAYER_ASSETS["idle"])]

        if self.facing < 0:
            image = pygame.transform.flip(image, True, False)
        self.image = image

    def draw(self, camera):
        img = self.image
        if self.invincible_timer > 0 and self.invincible_timer % 6 < 3:
            img = self.image.copy()
            img.set_alpha(120)
        screen.blit(img, (self.rect.x - camera.x + self.draw_offset_x, self.rect.y - camera.y + self.draw_offset_y))


class Level:
    def __init__(self, path):
        self.path = path
        self.solids = pygame.sprite.Group()
        self.crumble = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.portal = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.all_tiles = pygame.sprite.Group()
        self.player_spawn = (64, 64)
        self.width = 0
        self.height = 0
        self.boss = None
        self._load()

    def _load(self):
        rows = [line.rstrip("\n") for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.height = len(rows) * TILE_SIZE
        self.width = max(len(row) for row in rows) * TILE_SIZE if rows else SCREEN_WIDTH

        cp_index = 0
        for y, row in enumerate(rows):
            for x, cell in enumerate(row):
                wx = x * TILE_SIZE
                wy = y * TILE_SIZE

                if cell == "#":
                    tile = SolidTile(wx, wy)
                    self.solids.add(tile)
                    self.all_tiles.add(tile)
                elif cell == "B":
                    tile = CrumbleTile(wx, wy)
                    self.solids.add(tile)
                    self.crumble.add(tile)
                    self.all_tiles.add(tile)
                elif cell == "^":
                    self.hazards.add(Spike(wx, wy))
                elif cell == "P":
                    self.player_spawn = (wx + 4, wy - 10)
                elif cell == "O":
                    self.portal.add(Portal(wx, wy))
                elif cell == "C":
                    cp = Checkpoint(wx, wy, cp_index)
                    cp_index += 1
                    self.checkpoints.add(cp)
                elif cell == "E":
                    self.enemies.add(WalkerEnemy(wx, wy))
                elif cell == "S":
                    self.enemies.add(ShooterEnemy(wx, wy))
                elif cell == "K":
                    self.boss = BossEnemy(wx, wy)
                    self.enemies.add(self.boss)

    def update(self, player):
        self.crumble.update()
        self.portal.update()
        for enemy in list(self.enemies):
            enemy.update(self.solids, self.enemy_bullets, player)
        for bullet in list(self.enemy_bullets):
            bullet.update(self.solids)

    def draw(self, camera):
        for tile in self.all_tiles:
            screen.blit(tile.image, (tile.rect.x - camera.x, tile.rect.y - camera.y))
        for cp in self.checkpoints:
            screen.blit(cp.image, (cp.rect.x - camera.x, cp.rect.y - camera.y))
        for portal in self.portal:
            screen.blit(portal.image, (portal.rect.x - camera.x, portal.rect.y - camera.y))
        for hazard in self.hazards:
            screen.blit(hazard.image, (hazard.rect.x - camera.x, hazard.rect.y - camera.y))
        for enemy in self.enemies:
            screen.blit(enemy.image, (enemy.rect.x - camera.x, enemy.rect.y - camera.y))
        for bullet in self.enemy_bullets:
            screen.blit(bullet.image, (bullet.rect.x - camera.x, bullet.rect.y - camera.y))


class Game:
    def __init__(self):
        self.level_paths = sorted(LEVEL_DIR.glob("level_*.txt"))
        self.level_index = 0
        self.level = None
        self.player = None
        self.camera = Camera()
        self.particles = []
        self.player_shots = pygame.sprite.Group()
        self.deaths = 0
        self.state = "title"
        self.checkpoint_label = "Start"
        self.message_timer = 0
        self.load_level(0, reset_deaths=True)

    def spawn_particles(self, x, y, color, amount=12):
        for _ in range(amount):
            self.particles.append(
                Particle(
                    x,
                    y,
                    color,
                    random.uniform(-2.8, 2.8),
                    random.uniform(-4.2, 0.4),
                    random.randint(16, 34),
                    random.randint(2, 4),
                )
            )

    def load_level(self, index, reset_deaths=False):
        self.level_index = index
        self.level = Level(self.level_paths[index])
        self.player = Player(*self.level.player_spawn)
        self.camera = Camera()
        self.player_shots.empty()
        self.checkpoint_label = "Start"
        if reset_deaths:
            self.deaths = 0
        self.spawn_particles(self.player.rect.centerx, self.player.rect.centery, CYAN, 18)

    def activate_checkpoint(self, cp):
        for other in self.level.checkpoints:
            other.deactivate()
        cp.activate()
        self.player.set_spawn(cp.rect.x, cp.rect.y - 6)
        self.checkpoint_label = f"CP-{cp.index + 1}"
        self.spawn_particles(cp.rect.centerx, cp.rect.centery, YELLOW, 18)

    def respawn(self):
        self.deaths += 1
        self.camera.shake(12, 5)
        self.spawn_particles(self.player.rect.centerx, self.player.rect.centery, RED, 26)
        self.player.respawn()

    def handle_combat(self):
        for shot in list(self.player_shots):
            for enemy in list(self.level.enemies):
                if shot.rect.colliderect(enemy.rect):
                    shot.kill()
                    self.spawn_particles(shot.rect.centerx, shot.rect.centery, CYAN, 8)
                    if enemy.take_damage(shot.damage):
                        self.spawn_particles(enemy.rect.centerx, enemy.rect.centery, GREEN, 24)
                        enemy.kill()
                    break
            for bullet in list(self.level.enemy_bullets):
                if shot.rect.colliderect(bullet.rect):
                    shot.kill()
                    bullet.kill()
                    self.spawn_particles(bullet.rect.centerx, bullet.rect.centery, PURPLE, 10)

    def handle_player_collisions(self):
        if pygame.sprite.spritecollideany(self.player, self.level.hazards):
            self.respawn()
            return

        if pygame.sprite.spritecollideany(self.player, self.level.enemies):
            if self.player.take_damage(1):
                self.respawn()
                return
            self.camera.shake(6, 3)

        bullet_hit = pygame.sprite.spritecollideany(self.player, self.level.enemy_bullets)
        if bullet_hit:
            bullet_hit.kill()
            if self.player.take_damage(1):
                self.respawn()
                return
            self.camera.shake(6, 3)
            self.spawn_particles(self.player.rect.centerx, self.player.rect.centery, PURPLE, 10)

        for cp in pygame.sprite.spritecollide(self.player, self.level.checkpoints, False):
            if not cp.active:
                self.activate_checkpoint(cp)

        portal_hit = pygame.sprite.spritecollideany(self.player, self.level.portal)
        if portal_hit:
            # Boss stage requires boss defeat before portal works.
            if self.level.boss is not None and self.level.boss.alive():
                self.message_timer = 90
            else:
                self.spawn_particles(self.player.rect.centerx, self.player.rect.centery, GREEN, 32)
                if self.level_index + 1 < len(self.level_paths):
                    self.state = "stage_clear"
                else:
                    self.state = "game_clear"

    def update_particles(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def update(self):
        if self.state != "playing":
            self.update_particles()
            return

        self.player.update(self.level.solids, self.level.crumble)
        self.level.update(self.player)
        for shot in list(self.player_shots):
            shot.update(self.level.solids)

        self.handle_combat()
        self.handle_player_collisions()

        if self.player.rect.top > self.level.height + 160:
            self.respawn()

        self.update_particles()
        self.camera.update(self.player, self.level.width, self.level.height)

        if self.message_timer > 0:
            self.message_timer -= 1

    def draw_background(self):
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

    def draw_hud(self):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, 78))
        pygame.draw.line(screen, SLATE2, (0, 78), (SCREEN_WIDTH, 78), 2)

        draw_text("Aden's Needle Trial v2", 18, 12)
        draw_text("Move: ←/→ or A/D   Jump: Z/Space   Dash: Shift/C   Shoot: X/J   Respawn: R", 18, 43, CYAN, small_font)
        draw_text(f"Stage {self.level_index + 1}/{len(self.level_paths)}", 790, 12, YELLOW, small_font)
        draw_text(f"Deaths {self.deaths}", 790, 34, TEXT, small_font)
        draw_text(f"Checkpoint {self.checkpoint_label}", 790, 54, TEXT, small_font)

        for i in range(self.player.hp):
            screen.blit(HEART_IMAGE, (640 + i * 24, 14))

        if self.level.boss is not None and self.level.boss.alive():
            boss = self.level.boss
            bar_w = 300
            hp_w = int(bar_w * (boss.health / boss.max_health))
            pygame.draw.rect(screen, (40, 25, 50), (330, 14, bar_w, 14))
            pygame.draw.rect(screen, RED, (330, 14, hp_w, 14))
            pygame.draw.rect(screen, WHITE, (330, 14, bar_w, 14), 1)
            draw_text("BOSS", 280, 10, RED, small_font)

        if self.message_timer > 0:
            draw_text("Boss must be defeated before entering the portal!", SCREEN_WIDTH // 2, 96, ORANGE, small_font, True)

    def draw_panel(self, title, body, sub):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 155))
        screen.blit(overlay, (0, 0))
        box = pygame.Rect(165, 145, 630, 230)
        pygame.draw.rect(screen, (18, 20, 30), box, border_radius=14)
        pygame.draw.rect(screen, PURPLE, box, 3, border_radius=14)
        draw_text(title, SCREEN_WIDTH // 2, 205, GREEN, big_font, True)
        draw_text(body, SCREEN_WIDTH // 2, 270, WHITE, font, True)
        draw_text(sub, SCREEN_WIDTH // 2, 322, CYAN, small_font, True)

    def draw(self):
        self.draw_background()
        self.level.draw(self.camera)

        for shot in self.player_shots:
            screen.blit(shot.image, (shot.rect.x - self.camera.x, shot.rect.y - self.camera.y))

        self.player.draw(self.camera)

        for p in self.particles:
            p.draw(self.camera)

        self.draw_hud()

        if self.state == "title":
            self.draw_panel(
                "aden",
                "Remote shooting, animated portal, 20 stages, and a boss fight.",
                "Press any key to start",
            )
        elif self.state == "stage_clear":
            self.draw_panel(
                "STAGE CLEAR",
                f"Stage {self.level_index + 1} cleared.",
                "Press Enter or Space for next stage",
            )
        elif self.state == "game_clear":
            self.draw_panel(
                "ALL CLEAR",
                f"Aden cleared all {len(self.level_paths)} stages.",
                "Press Enter or Space to restart",
            )

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
                    elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_c):
                        self.player.request_dash()
                    elif event.key in (pygame.K_x, pygame.K_j):
                        self.player.request_shoot(self.player_shots)
                    elif event.key == pygame.K_r:
                        self.respawn()

                elif self.state == "stage_clear":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.load_level(self.level_index + 1)
                        self.state = "playing"

                elif self.state == "game_clear":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.load_level(0, reset_deaths=True)
                        self.state = "playing"


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
