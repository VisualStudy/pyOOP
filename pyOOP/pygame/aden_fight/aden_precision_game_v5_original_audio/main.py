
import sys
from pathlib import Path
import random
import math
import pygame

pygame.init()

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
LEVEL_DIR = BASE_DIR / "levels"
MUSIC_DIR = BASE_DIR / "music"
SOUND_DIR = BASE_DIR / "sounds"

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
PINK = (255, 100, 180)
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
WARDEN_FRAMES = [load_image(f"boss_warden_{i}.png", (144, 112)) for i in range(8)]
VOID_FRAMES = [load_image(f"boss_void_{i}.png", (192, 144)) for i in range(10)]
GIRLFRIEND_FRAMES = [load_image("girlfriend_idle_0.png", (40, 56)), load_image("girlfriend_idle_1.png", (40, 56))]

HEART_IMAGE = load_image("heart.png", (22, 22))
TILE_IMAGE = load_image("tile_ground.png", (TILE_SIZE, TILE_SIZE))
CRUMBLE_IMAGE = load_image("tile_crumble.png", (TILE_SIZE, TILE_SIZE))
SPIKE_IMAGE = load_image("spike.png", (TILE_SIZE, TILE_SIZE))
CHECKPOINT_OFF = load_image("checkpoint_off.png", (24, 36))
CHECKPOINT_ON = load_image("checkpoint_on.png", (24, 36))
PORTAL_FRAMES = [load_image(f"portal_{i}.png", (96, 128)) for i in range(6)]
POPUP_SPIKE_FRAMES = [load_image(f"popup_spike_{i}.png", (TILE_SIZE, TILE_SIZE)) for i in range(4)]
LASER_EMITTER_IMAGE = load_image("laser_emitter.png", (TILE_SIZE, TILE_SIZE))
LASER_BEAM_FRAMES = [load_image(f"laser_beam_{i}.png", (TILE_SIZE, TILE_SIZE)) for i in range(3)]


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



class PopupSpike(pygame.sprite.Sprite):
    """
    Hidden trap spike.
    Map symbol: !
    It waits until aden gets close, shows a short warning, then pops up.
    """

    def __init__(self, x, y):
        super().__init__()
        self.frames = POPUP_SPIKE_FRAMES
        self.state = "hidden"
        self.timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage_active = False
        self.trigger_distance = 86

    def reset(self):
        self.state = "hidden"
        self.timer = 0
        self.image = self.frames[0]
        self.damage_active = False

    def reset_dynamic_objects(self):
        # Respawn crumble blocks by reloading the current text map.
        # This is called on checkpoint restart / death so softlocks are avoided.
        old_path = self.path
        fresh = Level(old_path)
        self.solids = fresh.solids
        self.crumble = fresh.crumble
        self.hazards = fresh.hazards
        self.popup_spikes = fresh.popup_spikes
        self.lasers = fresh.lasers
        self.portal = fresh.portal
        self.checkpoints = fresh.checkpoints
        self.enemies = fresh.enemies
        self.enemy_bullets = fresh.enemy_bullets
        self.all_tiles = fresh.all_tiles
        self.boss = fresh.boss
        self.width = fresh.width
        self.height = fresh.height
        self.player_spawn = fresh.player_spawn

    def update(self, player):
        if self.state == "hidden":
            self.image = self.frames[0]
            self.damage_active = False
            if abs(player.rect.centerx - self.rect.centerx) < self.trigger_distance and abs(player.rect.centery - self.rect.centery) < 100:
                self.state = "warning"
                self.timer = 18

        elif self.state == "warning":
            self.timer -= 1
            self.image = self.frames[1] if self.timer % 6 < 3 else self.frames[0]
            self.damage_active = False
            if self.timer <= 0:
                self.state = "active"
                self.timer = 42
                self.image = self.frames[3]
                self.damage_active = True

        elif self.state == "active":
            self.timer -= 1
            self.image = self.frames[3 if self.timer % 8 < 4 else 2]
            self.damage_active = True
            if self.timer <= 0:
                self.state = "hidden"
                self.timer = 0
                self.damage_active = False
                self.image = self.frames[0]


class LaserTrap(pygame.sprite.Sprite):
    """
    Sudden vertical laser.
    Map symbol: L
    It blinks as warning, then fires vertically for a short time.
    """

    def __init__(self, x, y):
        super().__init__()
        self.emitter_image = LASER_EMITTER_IMAGE
        self.image = self.emitter_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.timer = random.randint(0, 90)
        self.state = "idle"
        self.state_timer = random.randint(30, 90)
        self.beam_rect = pygame.Rect(x + 11, y - 520, 10, 520)
        self.damage_active = False
        self.frame = 0

    def reset(self):
        self.timer = random.randint(0, 90)
        self.state = "idle"
        self.state_timer = random.randint(30, 90)
        self.damage_active = False
        self.frame = 0

    def update(self, player=None):
        self.state_timer -= 1

        if self.state == "idle":
            self.damage_active = False
            if self.state_timer <= 0:
                self.state = "warning"
                self.state_timer = 28

        elif self.state == "warning":
            self.damage_active = False
            if self.state_timer <= 0:
                self.state = "fire"
                self.state_timer = 34

        elif self.state == "fire":
            self.damage_active = True
            self.frame = (self.frame + 1) % len(LASER_BEAM_FRAMES)
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = random.randint(65, 115)
                self.damage_active = False

    def draw(self, camera):
        screen.blit(self.emitter_image, (self.rect.x - camera.x, self.rect.y - camera.y))
        if self.state == "warning":
            if self.state_timer % 8 < 4:
                pygame.draw.rect(
                    screen,
                    (255, 100, 180),
                    (self.beam_rect.x - camera.x, self.beam_rect.y - camera.y, self.beam_rect.w, self.beam_rect.h),
                    1,
                )
        elif self.state == "fire":
            tile = LASER_BEAM_FRAMES[self.frame]
            y = self.beam_rect.y
            while y < self.beam_rect.bottom:
                screen.blit(tile, (self.rect.x - camera.x, y - camera.y))
                y += TILE_SIZE

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
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, math.hypot(dx, dy))
            speed = 4.2
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, 4.5 * self.direction, -1.8))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, 4.5 * self.direction, 1.8))
            self.cooldown = 42 if self.health > self.max_health // 2 else 30


class WardenBoss(Enemy):
    """Stage 21 boss: fast aimed shots + rotating needle bursts."""

    def __init__(self, x, y):
        super().__init__(x - 56, y - 60, WARDEN_FRAMES)
        self.health = 36
        self.max_health = 36
        self.move_timer = 0
        self.cooldown = 36
        self.burst_timer = 120
        self.phase = 1
        self.base_x = self.rect.x
        self.base_y = self.rect.y

    def update(self, solids, bullets, player):
        self.animate()
        self.move_timer += 1
        self.phase = 2 if self.health <= self.max_health // 2 else 1

        # Floating figure-eight movement
        self.rect.x = self.base_x + int(math.sin(self.move_timer * 0.035) * 90)
        self.rect.y = self.base_y + int(math.sin(self.move_timer * 0.06) * 38)

        self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
        self.cooldown -= 1
        self.burst_timer -= 1

        if self.cooldown <= 0:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, math.hypot(dx, dy))
            speed = 4.8 if self.phase == 1 else 5.6
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed - 1.2))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed + 1.2))
            self.cooldown = 42 if self.phase == 1 else 28

        if self.burst_timer <= 0:
            count = 10 if self.phase == 1 else 16
            speed = 3.2 if self.phase == 1 else 3.9
            offset = self.move_timer * 0.08
            for i in range(count):
                a = offset + i * math.tau / count
                bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, math.cos(a) * speed, math.sin(a) * speed))
            self.burst_timer = 140 if self.phase == 1 else 95


class VoidFinalBoss(Enemy):
    """Final boss: dense but still fair projectile patterns."""

    def __init__(self, x, y):
        super().__init__(x - 80, y - 78, VOID_FRAMES)
        self.health = 60
        self.max_health = 60
        self.move_timer = 0
        self.cooldown = 24
        self.ring_timer = 80
        self.sweep_timer = 150
        self.base_x = self.rect.x
        self.base_y = self.rect.y
        self.phase = 1

    def update(self, solids, bullets, player):
        self.animate()
        self.move_timer += 1
        if self.health <= self.max_health * 0.35:
            self.phase = 3
        elif self.health <= self.max_health * 0.70:
            self.phase = 2
        else:
            self.phase = 1

        # Aggressive floating movement
        self.rect.x = self.base_x + int(math.sin(self.move_timer * 0.032) * 120)
        self.rect.y = self.base_y + int(math.sin(self.move_timer * 0.071) * 52)

        self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
        self.cooldown -= 1
        self.ring_timer -= 1
        self.sweep_timer -= 1

        if self.cooldown <= 0:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, math.hypot(dx, dy))
            speed = 4.6 + self.phase * 0.45
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed - 1.0))
            bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, dx / dist * speed, dy / dist * speed + 1.0))
            self.cooldown = max(12, 30 - self.phase * 5)

        if self.ring_timer <= 0:
            count = 14 + self.phase * 4
            speed = 3.0 + self.phase * 0.35
            offset = self.move_timer * 0.09
            for i in range(count):
                a = offset + i * math.tau / count
                # every other bullet is slightly faster, making a spiral gap pattern
                spd = speed + (0.6 if i % 2 == 0 else 0)
                bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, math.cos(a) * spd, math.sin(a) * spd))
            self.ring_timer = max(55, 105 - self.phase * 16)

        if self.sweep_timer <= 0:
            # Horizontal curtain with jumpable gaps
            for k in range(-3, 4):
                if k == 0:
                    continue
                bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery + k * 18, 5.2 * self.direction, 0))
            if self.phase >= 2:
                for k in range(-2, 3):
                    bullets.add(EnemyBullet(self.rect.centerx, self.rect.centery, 4.3 * self.direction, k * 1.2))
            self.sweep_timer = max(95, 155 - self.phase * 20)


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
            self.shoot_cooldown = 10
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
        self.popup_spikes = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
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
                elif cell == "!":
                    self.popup_spikes.add(PopupSpike(wx, wy))
                elif cell == "L":
                    self.lasers.add(LaserTrap(wx, wy))
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
                elif cell == "M":
                    self.boss = WardenBoss(wx, wy)
                    self.enemies.add(self.boss)
                elif cell == "Z":
                    self.boss = VoidFinalBoss(wx, wy)
                    self.enemies.add(self.boss)

    def reset_dynamic_objects(self):
        """
        Rebuild the current level state after death/checkpoint restart.
        This respawns crumble blocks, popup spikes, lasers, enemies, bullets,
        and boss state. Static level layout is re-read from the text map.
        """
        fresh = Level(self.path)

        self.solids = fresh.solids
        self.crumble = fresh.crumble
        self.hazards = fresh.hazards
        self.popup_spikes = getattr(fresh, "popup_spikes", pygame.sprite.Group())
        self.lasers = getattr(fresh, "lasers", pygame.sprite.Group())
        self.portal = fresh.portal
        self.checkpoints = fresh.checkpoints
        self.enemies = fresh.enemies
        self.enemy_bullets = fresh.enemy_bullets
        self.all_tiles = fresh.all_tiles
        self.boss = fresh.boss
        self.width = fresh.width
        self.height = fresh.height
        self.player_spawn = fresh.player_spawn

    def update(self, player):
        self.crumble.update()
        if hasattr(self, "popup_spikes"):
            for popup in list(self.popup_spikes):
                popup.update(player)
        if hasattr(self, "lasers"):
            for laser in list(self.lasers):
                laser.update(player)
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
        for popup in getattr(self, "popup_spikes", []):
            screen.blit(popup.image, (popup.rect.x - camera.x, popup.rect.y - camera.y))
        for laser in getattr(self, "lasers", []):
            laser.draw(camera)
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
        self.ending_timer = 0
        self.current_music = None
        self.music_enabled = True
        self.sfx_enabled = True
        self.sounds = {}
        self.load_sounds()
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






    def load_sounds(self):
        self.sounds = {}
        if not self.sfx_enabled:
            return
        for name in [
            "jump",
            "dash",
            "shoot",
            "hit",
            "death",
            "checkpoint",
            "portal",
            "boss_hit",
            "laser",
            "clear",
        ]:
            path = SOUND_DIR / f"{name}.wav"
            if path.exists():
                try:
                    self.sounds[name] = pygame.mixer.Sound(str(path))
                    self.sounds[name].set_volume(0.55)
                except pygame.error:
                    self.sfx_enabled = False
                    self.sounds = {}
                    return

    def play_sfx(self, name):
        if not self.sfx_enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass

    def music_for_level(self, index):
        stage_number = index + 1
        if stage_number <= 20:
            return "original_stage_early.wav"
        if stage_number == 21:
            return "original_mid_boss.wav"
        if stage_number == 31:
            return "original_final_boss.wav"
        return "original_stage_late.wav"

    def play_music_for_level(self, index):
        if not self.music_enabled:
            return
        music_name = self.music_for_level(index)
        if self.current_music == music_name:
            return
        path = MUSIC_DIR / music_name
        if not path.exists():
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(0.42)
            pygame.mixer.music.play(-1)
            self.current_music = music_name
        except pygame.error:
            self.music_enabled = False

    def play_ending_music(self):
        if not self.music_enabled:
            return
        music_name = "original_ending.wav"
        if self.current_music == music_name:
            return
        path = MUSIC_DIR / music_name
        if not path.exists():
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(0.45)
            pygame.mixer.music.play(-1)
            self.current_music = music_name
        except pygame.error:
            self.music_enabled = False

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
        self.play_music_for_level(index)

    def activate_checkpoint(self, cp):
        for other in self.level.checkpoints:
            other.deactivate()
        cp.activate()
        self.play_sfx("checkpoint")
        self.player.set_spawn(cp.rect.x, cp.rect.y - 6)
        self.checkpoint_label = f"CP-{cp.index + 1}"
        self.spawn_particles(cp.rect.centerx, cp.rect.centery, YELLOW, 18)

    def respawn(self):
        self.deaths += 1
        self.camera.shake(12, 5)
        self.play_sfx("death")
        self.spawn_particles(self.player.rect.centerx, self.player.rect.centery, RED, 26)

        spawn_x, spawn_y = self.player.spawn_x, self.player.spawn_y
        hp_max = self.player.max_hp

        if hasattr(self.level, "reset_dynamic_objects"):
            self.level.reset_dynamic_objects()
        else:
            self.level = Level(self.level.path)

        self.player = Player(spawn_x, spawn_y)
        self.player.max_hp = hp_max
        self.player.hp = hp_max
        self.player.set_spawn(spawn_x, spawn_y)
        self.player.invincible_timer = 60
        self.player_shots.empty()

        for cp in self.level.checkpoints:
            if abs(cp.rect.x - spawn_x) < 96 and abs(cp.rect.y - spawn_y) < 128:
                cp.activate()
                break

    def handle_combat(self):
        for shot in list(self.player_shots):
            for enemy in list(self.level.enemies):
                if shot.rect.colliderect(enemy.rect):
                    shot.kill()
                    self.spawn_particles(shot.rect.centerx, shot.rect.centery, CYAN, 8)
                    if enemy.take_damage(shot.damage):
                        self.play_sfx("boss_hit")
                        self.spawn_particles(enemy.rect.centerx, enemy.rect.centery, GREEN, 24)
                        enemy.kill()
                    else:
                        self.play_sfx("hit")
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

        for popup in getattr(self.level, "popup_spikes", []):
            if popup.damage_active and self.player.rect.colliderect(popup.rect):
                self.respawn()
                return

        for laser in getattr(self.level, "lasers", []):
            if laser.damage_active and self.player.rect.colliderect(laser.beam_rect):
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
                self.play_sfx("portal")
                self.spawn_particles(self.player.rect.centerx, self.player.rect.centery, GREEN, 32)
                if self.level_index + 1 < len(self.level_paths):
                    self.play_sfx("clear")
                    self.state = "stage_clear"
                else:
                    self.play_sfx("clear")
                    self.state = "ending"
                    self.ending_timer = 0
                    self.play_ending_music()

    def update_particles(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def update(self):
        if self.state != "playing":
            if self.state == "ending":
                self.ending_timer += 1
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
            hp_w = int(bar_w * max(0, boss.health) / boss.max_health)
            pygame.draw.rect(screen, (40, 25, 50), (330, 14, bar_w, 14))
            pygame.draw.rect(screen, RED, (330, 14, hp_w, 14))
            pygame.draw.rect(screen, WHITE, (330, 14, bar_w, 14), 1)
            boss_name = "VOID HEART" if isinstance(boss, VoidFinalBoss) else "NEEDLE WARDEN" if isinstance(boss, WardenBoss) else "BOSS"
            draw_text(boss_name, 230, 10, RED, small_font)

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
        elif self.state == "ending":
            self.draw_ending()


    def draw_ending(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # simple date spot
        pygame.draw.rect(screen, (28, 22, 38), (150, 135, 660, 285), border_radius=18)
        pygame.draw.rect(screen, PINK if 'PINK' in globals() else PURPLE, (150, 135, 660, 285), 3, border_radius=18)

        # moon / lights
        pygame.draw.circle(screen, (255, 235, 160), (710, 190), 34)
        for x in range(210, 760, 70):
            pygame.draw.circle(screen, (255, 220, 120), (x, 170 + int(math.sin((x + self.ending_timer) * 0.03) * 8)), 5)

        # ground
        pygame.draw.rect(screen, (50, 38, 55), (150, 360, 660, 60))

        # aden and girlfriend approach each other
        t = min(1.0, self.ending_timer / 180)
        aden_x = int(240 + 180 * t)
        girl_x = int(690 - 180 * t)
        y = 300

        aden_img = PLAYER_ASSETS["idle"][(self.ending_timer // 24) % 2]
        girl_img = GIRLFRIEND_FRAMES[(self.ending_timer // 24) % 2]

        if t < 0.97:
            screen.blit(aden_img, (aden_x, y))
            screen.blit(pygame.transform.flip(girl_img, True, False), (girl_x, y))
        else:
            screen.blit(aden_img, (420, y))
            screen.blit(pygame.transform.flip(girl_img, True, False), (465, y))
            draw_text("♥", 480, 275, RED, big_font, True)

        draw_text("THE END", SCREEN_WIDTH // 2, 205, GREEN, big_font, True)
        draw_text("Aden finally meets his girlfriend safely.", SCREEN_WIDTH // 2, 400, WHITE, font, True)
        draw_text("They leave for a peaceful date.", SCREEN_WIDTH // 2, 430, CYAN, small_font, True)
        draw_text("Press Enter or Space to restart", SCREEN_WIDTH // 2, 465, YELLOW, small_font, True)

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
                        self.play_sfx("jump")
                    elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_c):
                        self.player.request_dash()
                        self.play_sfx("dash")
                    elif event.key in (pygame.K_x, pygame.K_j):
                        self.player.request_shoot(self.player_shots)
                        self.play_sfx("shoot")
                    elif event.key == pygame.K_r:
                        self.respawn()

                elif self.state == "stage_clear":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.load_level(self.level_index + 1)
                        self.state = "playing"

                elif self.state == "ending":
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
