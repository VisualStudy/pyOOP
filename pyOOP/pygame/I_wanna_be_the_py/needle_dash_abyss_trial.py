import pygame
import sys
import math
import random

pygame.init()

# ============================================================
# Needle Dash: Abyss Trial
# ------------------------------------------------------------
# Original precision platformer made with pygame only.
# No copyrighted characters, sprites, maps, music, or assets.
#
# Controls
#   ← / →        Move
#   Z / Space    Jump
#   X / LShift   Dash
#   R            Restart from checkpoint
#   ESC          Quit
# ============================================================

WIDTH, HEIGHT = 960, 540
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Needle Dash: Abyss Trial")
clock = pygame.time.Clock()

# Colors
BLACK = (10, 10, 16)
BG_TOP = (12, 15, 28)
BG_BOTTOM = (24, 12, 32)
WHITE = (240, 240, 245)
SOFT_WHITE = (210, 215, 230)
GRAY = (80, 84, 98)
DARK = (28, 30, 42)
DARK2 = (38, 40, 56)
BLUE = (82, 174, 255)
CYAN = (80, 240, 230)
GREEN = (82, 230, 140)
RED = (245, 70, 85)
ORANGE = (255, 160, 80)
YELLOW = (255, 225, 90)
PURPLE = (178, 112, 255)
PINK = (255, 90, 180)

font = pygame.font.SysFont(None, 26)
small_font = pygame.font.SysFont(None, 20)
big_font = pygame.font.SysFont(None, 58)


def clamp(value, low, high):
    return max(low, min(high, value))


def draw_text(text, x, y, color=WHITE, font_obj=font, center=False):
    image = font_obj.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def draw_gradient_background():
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shake_timer = 0
        self.shake_power = 0

    def follow(self, target):
        desired_x = target.rect.centerx - WIDTH // 2
        desired_y = target.rect.centery - HEIGHT // 2

        self.x += (desired_x - self.x) * 0.08
        self.y += (desired_y - self.y) * 0.08

        self.x = clamp(self.x, 0, LEVEL_WIDTH - WIDTH)
        self.y = clamp(self.y, 0, LEVEL_HEIGHT - HEIGHT)

    def shake(self, frames=12, power=5):
        self.shake_timer = frames
        self.shake_power = power

    def offset(self):
        ox = int(self.x)
        oy = int(self.y)

        if self.shake_timer > 0:
            self.shake_timer -= 1
            ox += random.randint(-self.shake_power, self.shake_power)
            oy += random.randint(-self.shake_power, self.shake_power)

        return ox, oy


class Particle:
    def __init__(self, x, y, color, vx, vy, life, size):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.12
        self.life -= 1

    def draw(self, cam_x, cam_y):
        if self.life <= 0:
            return
        alpha_ratio = self.life / self.max_life
        radius = max(1, int(self.size * alpha_ratio))
        pygame.draw.circle(screen, self.color, (int(self.x - cam_x), int(self.y - cam_y)), radius)


particles = []


def spawn_particles(x, y, color, amount=14, power=4):
    for _ in range(amount):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.0, power)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        particles.append(Particle(x, y, color, vx, vy, random.randint(18, 36), random.randint(2, 5)))


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=DARK2):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        pygame.draw.rect(self.image, (62, 65, 84), (0, 0, w, h), 2)
        self.rect = self.image.get_rect(topleft=(x, y))


class GlowBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=PURPLE):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (*color, 80), (0, 0, w, h))
        pygame.draw.rect(self.image, color, (0, 0, w, h), 2)
        self.rect = self.image.get_rect(topleft=(x, y))


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, size=32, direction="up", color=RED):
        super().__init__()
        self.size = size
        self.direction = direction
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        if direction == "up":
            points = [(0, size), (size // 2, 0), (size, size)]
        elif direction == "down":
            points = [(0, 0), (size // 2, size), (size, 0)]
        elif direction == "left":
            points = [(size, 0), (0, size // 2), (size, size)]
        else:
            points = [(0, 0), (size, size // 2), (0, size)]

        pygame.draw.polygon(self.image, color, points)
        pygame.draw.polygon(self.image, WHITE, points, 1)

        self.rect = self.image.get_rect(topleft=(x, y))


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, delay, active_time, inactive_time):
        super().__init__()
        self.base_rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.delay = delay
        self.timer = delay
        self.active_time = active_time
        self.inactive_time = inactive_time
        self.active = False

    def update(self):
        self.timer += 1
        cycle = self.active_time + self.inactive_time
        phase = self.timer % cycle
        self.active = phase < self.active_time

        self.image.fill((0, 0, 0, 0))
        if self.active:
            pygame.draw.rect(self.image, (*PINK, 120), (0, 0, self.rect.width, self.rect.height))
            pygame.draw.rect(self.image, PINK, (0, 0, self.rect.width, self.rect.height))
            if self.rect.width > self.rect.height:
                pygame.draw.line(self.image, WHITE, (0, self.rect.height // 2), (self.rect.width, self.rect.height // 2), 1)
            else:
                pygame.draw.line(self.image, WHITE, (self.rect.width // 2, 0), (self.rect.width // 2, self.rect.height), 1)
        else:
            pygame.draw.rect(self.image, (90, 30, 60), (0, 0, self.rect.width, self.rect.height), 1)


class MovingSpike(pygame.sprite.Sprite):
    def __init__(self, x, y, size, axis, distance, speed, phase=0):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, ORANGE, [(0, size), (size // 2, 0), (size, size)])
        pygame.draw.polygon(self.image, WHITE, [(0, size), (size // 2, 0), (size, size)], 1)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.start_x = x
        self.start_y = y
        self.axis = axis
        self.distance = distance
        self.speed = speed
        self.timer = phase

    def update(self):
        self.timer += self.speed
        offset = math.sin(self.timer) * self.distance
        if self.axis == "x":
            self.rect.x = self.start_x + int(offset)
        else:
            self.rect.y = self.start_y + int(offset)


class CrumbleBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.original_y = y
        self.image = pygame.Surface((w, h))
        self.image.fill((92, 86, 66))
        pygame.draw.rect(self.image, YELLOW, (0, 0, w, h), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.triggered = False
        self.timer = 0
        self.gone = False

    def trigger(self):
        if not self.triggered:
            self.triggered = True
            spawn_particles(self.rect.centerx, self.rect.centery, YELLOW, 10, 3)

    def update(self):
        if self.triggered:
            self.timer += 1
            if self.timer < 32:
                self.rect.x += random.choice([-1, 0, 1])
                self.rect.y = self.original_y + random.choice([-1, 0, 1])
            else:
                self.gone = True
                self.kill()


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((34, 56), pygame.SRCALPHA)
        self.active = False
        self.draw_flag()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw_flag(self):
        self.image.fill((0, 0, 0, 0))
        color = YELLOW if self.active else CYAN
        pygame.draw.rect(self.image, GREEN, (13, 6, 6, 44))
        pygame.draw.polygon(self.image, color, [(19, 6), (34, 15), (19, 24)])
        pygame.draw.circle(self.image, color, (16, 50), 6)

    def activate(self):
        if not self.active:
            self.active = True
            self.draw_flag()
            spawn_particles(self.rect.centerx, self.rect.centery, CYAN, 24, 5)


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((56, 56), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.timer = 0

    def update(self):
        self.timer += 0.08
        self.image.fill((0, 0, 0, 0))
        r = 22 + int(math.sin(self.timer) * 3)
        pygame.draw.circle(self.image, (*PURPLE, 70), (28, 28), r + 8)
        pygame.draw.circle(self.image, PURPLE, (28, 28), r)
        pygame.draw.circle(self.image, WHITE, (28, 28), 9)
        pygame.draw.circle(self.image, CYAN, (28, 28), 4)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((24, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.spawn_x = x
        self.spawn_y = y

        self.vel_x = 0
        self.vel_y = 0
        self.facing = 1

        self.move_speed = 5.2
        self.accel = 0.85
        self.friction = 0.78
        self.gravity = 0.62
        self.jump_power = -12.0
        self.max_fall_speed = 16

        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.double_jump_available = True

        self.dash_available = True
        self.dash_timer = 0
        self.dash_cooldown = 0

        self.invincible_timer = 0
        self.trail_timer = 0

        self.last_direction = 1

        self.draw_player()

    def draw_player(self):
        self.image.fill((0, 0, 0, 0))
        body_color = BLUE if self.invincible_timer % 6 < 3 else CYAN
        pygame.draw.rect(self.image, body_color, (3, 4, 18, 23), border_radius=4)
        pygame.draw.rect(self.image, WHITE, (6, 8, 5, 5))
        pygame.draw.rect(self.image, BLACK, (8, 10, 2, 2))

        # tiny scarf
        if self.facing >= 0:
            pygame.draw.polygon(self.image, YELLOW, [(4, 17), (-4, 21), (4, 23)])
        else:
            pygame.draw.polygon(self.image, YELLOW, [(20, 17), (28, 21), (20, 23)])

    def set_checkpoint(self, x, y):
        self.spawn_x = x
        self.spawn_y = y

    def respawn(self):
        self.rect.topleft = (self.spawn_x, self.spawn_y)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.double_jump_available = True
        self.dash_available = True
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.invincible_timer = 45
        spawn_particles(self.rect.centerx, self.rect.centery, BLUE, 20, 5)

    def update_input(self):
        keys = pygame.key.get_pressed()

        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]

        if left:
            self.last_direction = -1
        if right:
            self.last_direction = 1

        if left and not right:
            self.vel_x -= self.accel
            self.facing = -1
        elif right and not left:
            self.vel_x += self.accel
            self.facing = 1
        elif left and right:
            self.vel_x += self.accel * self.last_direction
            self.facing = self.last_direction
        else:
            self.vel_x *= self.friction
            if abs(self.vel_x) < 0.08:
                self.vel_x = 0

        self.vel_x = clamp(self.vel_x, -self.move_speed, self.move_speed)

    def request_jump(self):
        self.jump_buffer = 8

    def request_dash(self):
        if self.dash_available and self.dash_cooldown <= 0:
            self.dash_available = False
            self.dash_timer = 10
            self.dash_cooldown = 28
            self.vel_x = self.facing * 13
            self.vel_y = 0
            spawn_particles(self.rect.centerx, self.rect.centery, CYAN, 20, 6)

    def jump_logic(self):
        if self.jump_buffer > 0:
            if self.on_ground or self.coyote_timer > 0:
                self.vel_y = self.jump_power
                self.on_ground = False
                self.coyote_timer = 0
                self.jump_buffer = 0
                self.double_jump_available = True
                spawn_particles(self.rect.centerx, self.rect.bottom, WHITE, 10, 3)
            elif self.double_jump_available:
                self.vel_y = self.jump_power * 0.88
                self.double_jump_available = False
                self.jump_buffer = 0
                spawn_particles(self.rect.centerx, self.rect.centery, PURPLE, 16, 4)

    def physics(self):
        if self.dash_timer > 0:
            self.dash_timer -= 1
            self.trail_timer += 1
            if self.trail_timer % 2 == 0:
                spawn_particles(self.rect.centerx, self.rect.centery, CYAN, 2, 2)
        else:
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed

        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.coyote_timer > 0:
            self.coyote_timer -= 1
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def move_and_collide(self, platforms):
        self.rect.x += int(round(self.vel_x))
        hits = pygame.sprite.spritecollide(self, platforms, False)

        for block in hits:
            if isinstance(block, CrumbleBlock) and block.gone:
                continue

            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                self.rect.left = block.rect.right

            self.vel_x = 0

        self.rect.y += int(round(self.vel_y))
        hits = pygame.sprite.spritecollide(self, platforms, False)

        was_grounded = self.on_ground
        self.on_ground = False

        for block in hits:
            if isinstance(block, CrumbleBlock) and block.gone:
                continue

            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
                self.vel_y = 0
                self.on_ground = True
                self.double_jump_available = True
                self.dash_available = True
                if isinstance(block, CrumbleBlock):
                    block.trigger()
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom
                self.vel_y = 0

        if was_grounded and not self.on_ground:
            self.coyote_timer = 8

    def update(self, platforms):
        self.update_input()
        self.jump_logic()
        self.physics()
        self.move_and_collide(platforms)
        self.draw_player()


LEVEL_WIDTH = 3300
LEVEL_HEIGHT = 1000


def make_groups():
    return {
        "all": pygame.sprite.Group(),
        "platforms": pygame.sprite.Group(),
        "hazards": pygame.sprite.Group(),
        "moving_hazards": pygame.sprite.Group(),
        "lasers": pygame.sprite.Group(),
        "crumbles": pygame.sprite.Group(),
        "checkpoints": pygame.sprite.Group(),
        "goal": pygame.sprite.Group(),
        "decor": pygame.sprite.Group(),
    }


def add_block(groups, x, y, w, h, color=DARK2):
    block = Block(x, y, w, h, color)
    groups["all"].add(block)
    groups["platforms"].add(block)
    return block


def add_glow(groups, x, y, w, h, color=PURPLE):
    block = GlowBlock(x, y, w, h, color)
    groups["all"].add(block)
    groups["decor"].add(block)
    return block


def add_spike(groups, x, y, size=32, direction="up", color=RED):
    spike = Spike(x, y, size, direction, color)
    groups["all"].add(spike)
    groups["hazards"].add(spike)
    return spike


def add_moving_spike(groups, x, y, size, axis, distance, speed, phase=0):
    spike = MovingSpike(x, y, size, axis, distance, speed, phase)
    groups["all"].add(spike)
    groups["moving_hazards"].add(spike)
    return spike


def add_laser(groups, x, y, w, h, delay, active_time=75, inactive_time=65):
    laser = Laser(x, y, w, h, delay, active_time, inactive_time)
    groups["all"].add(laser)
    groups["lasers"].add(laser)
    return laser


def add_crumble(groups, x, y, w, h):
    c = CrumbleBlock(x, y, w, h)
    groups["all"].add(c)
    groups["platforms"].add(c)
    groups["crumbles"].add(c)
    return c


def build_level():
    groups = make_groups()

    # World borders
    add_block(groups, 0, 940, LEVEL_WIDTH, 60)
    add_block(groups, 0, 0, LEVEL_WIDTH, 36)
    add_block(groups, 0, 0, 36, LEVEL_HEIGHT)
    add_block(groups, LEVEL_WIDTH - 36, 0, 36, LEVEL_HEIGHT)

    # Decorative neon panels
    for x in range(220, LEVEL_WIDTH, 420):
        add_glow(groups, x, 90 + (x // 200) % 4 * 40, 120, 18, random.choice([PURPLE, CYAN, GREEN]))

    # Area 1: basic movement
    for rect in [
        (80, 860, 220, 30),
        (390, 805, 160, 26),
        (650, 760, 130, 26),
        (900, 710, 150, 26),
        (1120, 655, 110, 26),
        (1340, 600, 180, 26),
    ]:
        add_block(groups, *rect)

    for x in range(330, 390, 30):
        add_spike(groups, x, 908, 32)
    for x in range(565, 650, 30):
        add_spike(groups, x, 908, 32)
    for x in range(790, 900, 30):
        add_spike(groups, x, 908, 32)
    add_spike(groups, 940, 678, 32)
    add_spike(groups, 975, 678, 32)

    # Area 2: moving hazards
    for rect in [
        (1620, 620, 130, 26),
        (1850, 690, 110, 26),
        (2070, 620, 130, 26),
        (2300, 560, 150, 26),
    ]:
        add_block(groups, *rect)

    add_moving_spike(groups, 1570, 820, 34, "y", 130, 0.055)
    add_moving_spike(groups, 1780, 740, 34, "x", 90, 0.050, 2)
    add_moving_spike(groups, 2010, 720, 34, "y", 110, 0.060, 5)
    add_moving_spike(groups, 2220, 670, 34, "x", 100, 0.047, 8)

    # Area 3: crumble blocks and laser rhythm
    for rect in [
        (2540, 670, 100, 24),
        (2700, 620, 90, 24),
        (2860, 570, 90, 24),
    ]:
        add_block(groups, *rect)

    add_crumble(groups, 2470, 760, 80, 24)
    add_crumble(groups, 2600, 730, 80, 24)
    add_crumble(groups, 2730, 700, 80, 24)
    add_crumble(groups, 2860, 670, 80, 24)

    add_laser(groups, 2510, 500, 18, 260, 0)
    add_laser(groups, 2670, 430, 18, 280, 45)
    add_laser(groups, 2830, 390, 18, 300, 90)

    # Ceiling spikes
    for x in range(470, 620, 32):
        add_spike(groups, x, 36, 32, "down")
    for x in range(1320, 1450, 32):
        add_spike(groups, x, 36, 32, "down")
    for x in range(2250, 2450, 32):
        add_spike(groups, x, 36, 32, "down")

    # Final tower
    for rect in [
        (3000, 760, 120, 26),
        (3140, 690, 100, 26),
        (3000, 610, 100, 26),
        (3160, 530, 90, 26),
        (3000, 450, 120, 26),
    ]:
        add_block(groups, *rect)

    for y in [730, 650, 570, 490]:
        add_spike(groups, 3090, y, 32, "right")
        add_spike(groups, 3190, y - 35, 32, "left")

    # Checkpoints
    checkpoints = [
        (96, 804, "Start"),
        (1360, 544, "Needle Gate"),
        (2310, 504, "Laser Bridge"),
        (3010, 394, "Final Rise"),
    ]

    for x, y, name in checkpoints:
        cp = Checkpoint(x, y, name)
        groups["all"].add(cp)
        groups["checkpoints"].add(cp)

    # Goal
    goal = Goal(3200, 384)
    groups["all"].add(goal)
    groups["goal"].add(goal)

    return groups


def draw_world_grid(cam_x, cam_y):
    grid_color = (23, 25, 38)
    start_x = -cam_x % 60
    start_y = -cam_y % 60

    for x in range(start_x, WIDTH, 60):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))
    for y in range(start_y, HEIGHT, 60):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))


def draw_sprite_group(group, cam_x, cam_y):
    for sprite in group:
        screen.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))


def draw_hud(deaths, checkpoint_name, player):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 76))
    pygame.draw.line(screen, (60, 62, 80), (0, 76), (WIDTH, 76), 2)

    draw_text("Needle Dash: Abyss Trial", 22, 16, WHITE)
    draw_text("←/→ Move   Z/Space Jump   X/Shift Dash   R Checkpoint", 22, 45, CYAN, small_font)
    draw_text("Deaths: " + str(deaths), 790, 16, YELLOW)
    draw_text("Checkpoint: " + checkpoint_name, 700, 45, SOFT_WHITE, small_font)

    dash_text = "Dash: READY" if player.dash_available else "Dash: WAIT"
    dash_color = GREEN if player.dash_available else ORANGE
    draw_text(dash_text, 790, 45, dash_color, small_font)


def reset_level():
    global particles
    particles = []
    groups = build_level()
    player = Player(115, 810)
    groups["all"].add(player)

    first_cp = None
    for cp in groups["checkpoints"]:
        if cp.name == "Start":
            first_cp = cp
            break

    checkpoint_name = "Start"
    if first_cp:
        first_cp.activate()
        player.set_checkpoint(first_cp.rect.x, first_cp.rect.y - 32)

    camera = Camera()
    return groups, player, camera, checkpoint_name


groups, player, camera, checkpoint_name = reset_level()
deaths = 0
cleared = False
clear_timer = 0

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key in (pygame.K_z, pygame.K_SPACE):
                if not cleared:
                    player.request_jump()

            if event.key in (pygame.K_x, pygame.K_LSHIFT, pygame.K_RSHIFT):
                if not cleared:
                    player.request_dash()

            if event.key == pygame.K_r:
                if not cleared:
                    player.respawn()
                    camera.shake(6, 3)

            if event.key == pygame.K_RETURN and cleared:
                groups, player, camera, checkpoint_name = reset_level()
                deaths = 0
                cleared = False
                clear_timer = 0

    if not cleared:
        player.update(groups["platforms"])
        groups["moving_hazards"].update()
        groups["lasers"].update()
        groups["crumbles"].update()
        groups["goal"].update()

        # Check crumble blocks touched from top or side
        for c in groups["crumbles"]:
            if player.rect.colliderect(c.rect.inflate(8, 4)):
                if player.rect.bottom <= c.rect.top + 12 or player.rect.centery < c.rect.centery:
                    c.trigger()

        # Hazard detection
        hit_hazard = pygame.sprite.spritecollide(player, groups["hazards"], False)
        hit_moving = pygame.sprite.spritecollide(player, groups["moving_hazards"], False)
        hit_laser = [laser for laser in groups["lasers"] if laser.active and player.rect.colliderect(laser.rect)]

        if (hit_hazard or hit_moving or hit_laser or player.rect.top > LEVEL_HEIGHT) and player.invincible_timer <= 0:
            deaths += 1
            camera.shake(14, 7)
            spawn_particles(player.rect.centerx, player.rect.centery, RED, 32, 7)
            player.respawn()

        # Checkpoints
        for cp in pygame.sprite.spritecollide(player, groups["checkpoints"], False):
            if not cp.active:
                cp.activate()
                player.set_checkpoint(cp.rect.x, cp.rect.y - 32)
                checkpoint_name = cp.name

        # Goal
        if pygame.sprite.spritecollide(player, groups["goal"], False):
            cleared = True
            clear_timer = 0
            spawn_particles(player.rect.centerx, player.rect.centery, PURPLE, 60, 8)
            camera.shake(20, 5)

    else:
        clear_timer += 1
        groups["goal"].update()

    # Particles
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

    camera.follow(player)
    cam_x, cam_y = camera.offset()

    # Draw
    draw_gradient_background()
    draw_world_grid(cam_x, cam_y)

    # Draw sprite layers
    draw_sprite_group(groups["decor"], cam_x, cam_y)

    # draw non-decor sprites except player in a stable layer order
    draw_sprite_group(groups["platforms"], cam_x, cam_y)
    draw_sprite_group(groups["checkpoints"], cam_x, cam_y)
    draw_sprite_group(groups["hazards"], cam_x, cam_y)
    draw_sprite_group(groups["moving_hazards"], cam_x, cam_y)
    draw_sprite_group(groups["lasers"], cam_x, cam_y)
    draw_sprite_group(groups["goal"], cam_x, cam_y)

    # player
    screen.blit(player.image, (player.rect.x - cam_x, player.rect.y - cam_y))

    for p in particles:
        p.draw(cam_x, cam_y)

    draw_hud(deaths, checkpoint_name, player)

    if cleared:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(220, 145, 520, 250)
        pygame.draw.rect(screen, (18, 20, 32), box, border_radius=12)
        pygame.draw.rect(screen, PURPLE, box, 3, border_radius=12)

        draw_text("TRIAL CLEAR!", WIDTH // 2, 205, GREEN, big_font, center=True)
        draw_text("Deaths: " + str(deaths), WIDTH // 2, 270, WHITE, font, center=True)
        draw_text("Press ENTER to restart", WIDTH // 2, 325, CYAN, font, center=True)
        draw_text("Original pygame-only precision platformer", WIDTH // 2, 360, SOFT_WHITE, small_font, center=True)

    pygame.display.flip()
