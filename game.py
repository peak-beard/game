import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_w,
    K_s,
    K_a,
    K_d,
    K_RIGHT,
    K_LEFT,
    K_DOWN,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("textures/airship.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        pygame.transform.scale(self.surf, (10, 2))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -7)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 7)
        if pressed_keys[K_a]:
            self.rect.move_ip(-7, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(7, 0)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -7)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 7)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-7, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(7, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("textures/missile1.png").convert()
        self.surf.set_colorkey((66, 194, 245), RLEACCEL)
        pygame.transform.scale(self.surf, (10, 2))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.Surface((50, 30))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


clock = pygame.time.Clock()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
score = 0

font = pygame.font.Font('fonts/Roboto-Black.ttf', 32)
text = font.render("Game Over!", True, (235, 64, 52))
textRect = text.get_rect()


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
SCORE = pygame.USEREVENT + 3
pygame.time.set_timer(SCORE, 1000)
GAMEOVER = pygame.USEREVENT + 4
gameover_event = pygame.event.Event(GAMEOVER, message="Game over!")


player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


running = True
gameover = False


while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == GAMEOVER:
            gameover = True
            screen.fill((255, 255, 255))
            player.kill()
            screen.blit(text, textRect)

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == SCORE:
            if gameover == False:

                score = score + 1
                print(score)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    if pygame.sprite.spritecollideany(player, enemies) or gameover:
        pygame.event.post(gameover_event)

    else:

        screen.fill((66, 194, 245))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
    pygame.display.flip()

    clock.tick(30)
