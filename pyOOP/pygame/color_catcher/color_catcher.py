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

# 게임 화면 생성
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

    def update(self):
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
    # 보석이 더 자주 나오고, 폭탄은 가끔 나옴
    if random.randint(1, 5) == 1:
        item = FallingItem("bomb")
        bombs.add(item)
    else:
        item = FallingItem("gem")
        gems.add(item)

    all_sprites.add(item)


# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
gems = pygame.sprite.Group()
bombs = pygame.sprite.Group()

# 배경 별 생성
for _ in range(70):
    star = Star()
    stars.add(star)
    all_sprites.add(star)

# 플레이어 생성
player = Player()
all_sprites.add(player)

score = 0
life = 3
game_over = False
spawn_timer = 0

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -7
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 7
            elif event.key == pygame.K_SPACE and game_over:
                # 게임 재시작
                for gem in gems:
                    gem.kill()
                for bomb in bombs:
                    bomb.kill()
                score = 0
                life = 3
                game_over = False
                player.rect.centerx = screen_width // 2

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0

    if not game_over:
        spawn_timer += 1
        if spawn_timer >= 25:
            create_item()
            spawn_timer = 0

        all_sprites.update()

        # 보석을 받으면 점수 증가
        gem_hits = pygame.sprite.spritecollide(player, gems, True)
        for gem in gem_hits:
            score += 10

        # 폭탄을 받으면 생명 감소
        bomb_hits = pygame.sprite.spritecollide(player, bombs, True)
        for bomb in bomb_hits:
            life -= 1

        if life <= 0:
            game_over = True
    else:
        stars.update()

    screen.fill(black)
    all_sprites.draw(screen)

    # 점수판
    score_text = font.render("Score: " + str(score), True, white)
    life_text = font.render("Life: " + str(life), True, white)
    screen.blit(score_text, (20, 20))
    screen.blit(life_text, (20, 55))

    if game_over:
        draw_text("GAME OVER", big_font, red, screen_width // 2, screen_height // 2 - 40)
        draw_text("Press SPACE to restart", font, white, screen_width // 2, screen_height // 2 + 25)

    pygame.display.flip()
    clock.tick(60)
