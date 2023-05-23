import pygame
from pygame.locals import *
pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arcanoid')

# farbicky
bg = (255, 255, 255)
brick_colors = [(40, 129, 237), (152, 43, 224), (43, 224, 127)]
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
text_col = (78, 81, 139)

# basic nastavenia
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0
font = pygame.font.SysFont('Arial', 30)

class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50
        self.create_wall()

    def create_wall(self):
        self.bricks = []
        for row in range(rows):
            brick_row = []
            for col in range(cols):
                brick_x = col * self.width
                brick_y = row * self.height
                rect = pygame.Rect(brick_x, brick_y, self.width, self.height)
                strength = 3 - row // 2
                brick_individual = [rect, strength]
                brick_row.append(brick_individual)
            self.bricks.append(brick_row)

    def draw_wall(self):
        for row in self.bricks:
            for brick in row:
                brick_col = brick_colors[brick[1] - 1]
                pygame.draw.rect(screen, brick_col, brick[0])
                pygame.draw.rect(screen, bg, brick[0], 2)

class Paddle:
    def __init__(self):
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = screen_width // cols
        self.x = (screen_width // 2) - (self.width // 2)
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

class GameBall:
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        collision_thresh = 5
        wall_destroyed = 1
        row_count = 0
        for row in wall.bricks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    if item[1] > 1:
                        item[1] -= 1
                    else:
                        item[0] = (0, 0, 0, 0)
                if item[0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        if wall_destroyed == 1:
            self.game_over = 1

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        if self.rect.colliderect(player_paddle.rect):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                self.speed_x = min(self.speed_x, self.speed_max)
                self.speed_x = max(self.speed_x, -self.speed_max)
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

wall = Wall()
player_paddle = Paddle()
ball = GameBall(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:
    clock.tick(fps)
    screen.fill(bg)
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        player_paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

    if not live_ball:
        if game_over == 0:
            draw_text('Arcanoid velky twist - v Pygame', font, text_col, 140, screen_height // 2 + 50)
            draw_text('klikni hocikam na začatie hry', font, text_col, 140, screen_height // 2 + 100)
            draw_text('pouzivaj sipocky', font, text_col, 140, screen_height // 2 + 150)

        elif game_over == 1:
            draw_text('VÝHRA!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('klikni hocikam na začatie hry', font, text_col, 140, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('AJAJAJ, ZNOVA!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('klikni hocikam na začatie hry', font, text_col, 140, screen_height // 2 + 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()

    pygame.display.update()

pygame.quit()
