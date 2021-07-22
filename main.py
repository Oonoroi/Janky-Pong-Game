import pygame
import winsound
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("sprites\\paddle.png")
        self.rect = self.surf.get_rect()

    def move_paddle(self, key):
        if key[pygame.K_UP]:
            if self.rect.top > 0:
                self.rect.move_ip(0, -14)

        elif key[pygame.K_DOWN]:
            if self.rect.bottom < height:
                self.rect.move_ip(0, 14)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("sprites\\paddle.png")
        self.rect = self.surf.get_rect()
        self.screen_div = random.randint(2, 16)

    def scramble(self):
        self.screen_div = random.randint(2, 12)

    def ai(self):
        if ball.rect.centery < self.rect.centery:
            if self.rect.top > 0:
                if ball.bounces == 0:
                    if ball.rect.centerx > (4 * (width / 5)):
                        self.rect.move_ip(0, -14)
                elif ball.bounces > 0:
                    if ball.rect.centerx > ((self.screen_div - 1) * (width / self.screen_div)):
                        self.rect.move_ip(0, -14)

        if ball.rect.centery > self.rect.centery:
            if self.rect.bottom < height:
                if ball.bounces == 0:
                    if ball.rect.centerx > (4 * (width / 5)):
                        self.rect.move_ip(0, 14)
                elif ball.bounces > 0:
                    if ball.rect.centerx > ((self.screen_div - 1) * (width / self.screen_div)):
                        self.rect.move_ip(0, 14)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.image.load("sprites\\ball.png")
        self.rect = self.surf.get_rect()
        self.delta_x = 10
        self.delta_y = 10
        self.bounces = 0

    def move_ball(self):
        if self.rect.bottom >= height:
            self.delta_y *= -1

        elif self.rect.top <= 0:
            self.delta_y *= -1

        if self.rect.colliderect(player):
            self.delta_x = abs(self.delta_x)
            winsound.PlaySound("sfx\\ping_pong_8bit_beeep.wav", winsound.SND_ASYNC)
            self.bounces += 1

        elif self.rect.colliderect(enemy):
            self.delta_x = -abs(self.delta_x)
            winsound.PlaySound("sfx\\ping_pong_8bit_beeep.wav", winsound.SND_ASYNC)
            self.bounces += 1

        if self.rect.right >= width:
            ball.rect.centerx = (width / 2) - 10
            ball.rect.centery = (height / 2) - 10

        elif self.rect.left <= 0:
            ball.rect.centerx = (width / 2) - 10
            ball.rect.centery = (height / 2) - 10

        self.rect.move_ip(self.delta_x, self.delta_y)


class Scoreboard(object):
    def __init__(self):
        self.player_points = 0
        self.enemy_points = 0

        self.font = pygame.font.SysFont("Courier", 24)

        self.scoreboard_player = self.font.render("Player: " + str(self.player_points), True, (255, 255, 255))
        self.scoreboard_enemy = self.font.render("Enemy: " + str(self.enemy_points), True, (255, 255, 255))

    def scorekeep(self):
        if ball.rect.right >= width:
            self.player_points += 1
            self.scoreboard_player = self.font.render("Player: " + str(self.player_points), True, (255, 255, 255))

        elif ball.rect.left <= 0:
            self.enemy_points += 1
            self.scoreboard_enemy = self.font.render("Enemy: " + str(self.enemy_points), True, (255, 255, 255))


# set up screen and framerate
pygame.init()

clock = pygame.time.Clock()
width = 800
height = 600
window = pygame.display.set_mode([width, height])
pygame.display.set_caption("Pong")
icon = pygame.image.load("sprites\\icon.png")
pygame.display.set_icon(icon)

# putting sprites on screen
player = Player()
player.rect.move_ip(25, (height / 2) - 50)

enemy = Enemy()
enemy.rect.move_ip(width-45, (height / 2) - 50)

ball = Ball()
ball.rect.move_ip((width / 2) - 10, (height / 2) - 10)

scoreboard = Scoreboard()

# Game loop
still_playing = True
while still_playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False

    window.fill((0, 0, 0))

    key_pressed = pygame.key.get_pressed()
    player.move_paddle(key_pressed)

    enemy.scramble()
    enemy.ai()

    ball.move_ball()

    scoreboard.scorekeep()

    window.blit(player.surf, player.rect)
    window.blit(enemy.surf, enemy.rect)
    window.blit(ball.surf, ball.rect)
    window.blit(scoreboard.scoreboard_player, (200, 6))
    window.blit(scoreboard.scoreboard_enemy, (450, 6))

    pygame.display.flip()
    clock.tick(30)


pygame.quit()
