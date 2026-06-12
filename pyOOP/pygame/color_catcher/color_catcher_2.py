import pygame
import sys
import random

pygame.init()

# 게임 화면 크기
screen_width = 800
screen_height = 600

# 색상 정의
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 220, 120)
red = (240, 70, 70)
yellow = (255, 220, 80)
blue = (80, 160, 255)
purple = (190, 110, 255)
gray = (80, 80, 80)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Color Catcher")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((90, 30))
        self.image.fill(green)

        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 30

        self.speed_x = 0
        self.move_speed = 7

        # 왼쪽/오른쪽이 동시에 눌렸을 때 마지막으로 누른 방향을 우선하기 위한 변수
        self.last_direction = None

    def update(self):
        keys = pygame.key.get_pressed()

        left_pressed = keys[pygame.K_LEFT]
        right_pressed = keys[pygame.K_RIGHT]

        # 왼쪽과 오른쪽이 동시에 눌린 경우
        # 마지막으로 누른 방향을 우선한다.
        if left_pressed and right_pressed:
            if self.last_direction == "left":
                self.speed_x = -self.move_speed
            elif self.last_direction == "right":
                self.speed_x = self.move_speed
            else:
                self.speed_x = 0

        # 왼쪽만 눌린 경우
        elif left_pressed:
            self.speed_x = -self.move_speed
            self.last_direction = "left"

        # 오른쪽만 눌린 경우
        elif right_pressed:
            self.speed_x = self.move_speed
            self.last_direction = "right"

        # 아무 방향키도 눌리지 않은 경우
        else:
            self.speed_x = 0

        self.rect.x += self.speed_x

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width


class FallingItem(pygame.sprite.Sprite):
    def __init__(self, item_type):
        super().__init__()

        self.item_type = item_type

        if self.item_type == "gem":
            self.image = pygame.Surface((28, 28))
            self.image.fill(random.choice([yellow, blue, purple]))
            self.speed_y = random.randint(3, 6)
        else:
            self.image = pygame.Surface((34, 34))
            self.image.fill(red)
            self.speed_y = random.randint(4, 7)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -20)

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.top > screen_height:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((3, 3))
        self.image.fill(gray)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(0, screen_height)

        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.top > screen_height:
            self.rect.y = 0
            self.rect.x = random.randint(0, screen_width)


def draw_text(text, font_object, color, x, y):
    message = font_object.render(text, True, color)
    rect = message.get_rect()
    rect.center = (x, y)
    screen.blit(message, rect)


def create_item():
    if random.randint(1, 5) == 1:
        item = FallingItem("bomb")
        bombs.add(item)
    else:
        item = FallingItem("gem")
        gems.add(item)

    all_sprites.add(item)


all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
gems = pygame.sprite.Group()
bombs = pygame.sprite.Group()

for _ in range(70):
    star = Star()
    stars.add(star)
    all_sprites.add(star)

player = Player()
all_sprites.add(player)

score = 0
life = 3
game_over = False
spawn_timer = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # 마지막으로 누른 방향키를 기록한다.
            # 이렇게 하면 왼쪽을 누른 상태에서 오른쪽을 눌러도 자연스럽게 오른쪽 이동이 된다.
            if event.key == pygame.K_LEFT:
                player.last_direction = "left"

            elif event.key == pygame.K_RIGHT:
                player.last_direction = "right"

            elif event.key == pygame.K_SPACE and game_over:
                for gem in gems:
                    gem.kill()

                for bomb in bombs:
                    bomb.kill()

                score = 0
                life = 3
                game_over = False
                player.rect.centerx = screen_width // 2
                player.speed_x = 0
                player.last_direction = None

    if not game_over:
        spawn_timer += 1

        if spawn_timer >= 25:
            create_item()
            spawn_timer = 0

        all_sprites.update()

        gem_hits = pygame.sprite.spritecollide(player, gems, True)
        for gem in gem_hits:
            score += 10

        bomb_hits = pygame.sprite.spritecollide(player, bombs, True)
        for bomb in bomb_hits:
            life -= 1

        if life <= 0:
            game_over = True
    else:
        stars.update()

    screen.fill(black)
    all_sprites.draw(screen)

    score_text = font.render("Score: " + str(score), True, white)
    life_text = font.render("Life: " + str(life), True, white)

    screen.blit(score_text, (20, 20))
    screen.blit(life_text, (20, 55))

    if game_over:
        draw_text("GAME OVER", big_font, red, screen_width // 2, screen_height // 2 - 40)
        draw_text("Press SPACE to restart", font, white, screen_width // 2, screen_height // 2 + 25)

    pygame.display.flip()
    clock.tick(60)