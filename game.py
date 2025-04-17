import pygame
import sys
import random

# Настройки экрана
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FPS = 70

# Цвета
LIGHT_PINK = (255, 228, 235)
DARK_PINK = (220, 100, 140)
BLACK = (0, 0, 0)

# Параметры платформ
PADDLE_WIDTH = 112
PADDLE_HEIGHT = 200
PADDLE_GAP = 300
PADDLE_SPEED = 6

# Параметры мяча
BALL_RADIUS = 45
BALL_SPEED = 5
BALL_ACCELERATION = 0.2

# Отступы
BORDER_OFFSET = 25
BLACK_BORDER = 9

# Инициализация
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paww Pong")
clock = pygame.time.Clock()
font = pygame.font.Font("nin.otf", 48)
small_font = pygame.font.Font("nin.otf", 28)  # меньший шрифт для подсказок


# Загрузка и масштабирование спрайтов
ball_image = pygame.image.load("ball.png").convert_alpha()
paddle_image = pygame.image.load("plat.png").convert_alpha()

ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
paddle_image = pygame.transform.scale(paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

def reset_game():
    paddle_shake_timer = 0
    global ball_x, ball_y, ball_dx, ball_dy, score, game_over, fade_alpha, game_started
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = random.choice([-1, 1]) * BALL_SPEED
    ball_dy = -BALL_SPEED
    score = 0
    game_over = False
    fade_alpha = 0
    game_started = False

# Платформы
paddle_left = pygame.Rect(
    (SCREEN_WIDTH // 2 - PADDLE_GAP // 2 - PADDLE_WIDTH, SCREEN_HEIGHT - PADDLE_HEIGHT),
    (PADDLE_WIDTH, PADDLE_HEIGHT)
)
paddle_right = pygame.Rect(
    (SCREEN_WIDTH // 2 + PADDLE_GAP // 2, SCREEN_HEIGHT - PADDLE_HEIGHT),
    (PADDLE_WIDTH, PADDLE_HEIGHT)
)

reset_game()

def draw_text_with_fade(text, font, color, pos, screen, alpha):
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(alpha)
    screen.blit(text_surface, pos)

def draw_vertical_gradient(surface, top_color, bottom_color):
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        r = top_color[0] * (1 - ratio) + bottom_color[0] * ratio
        g = top_color[1] * (1 - ratio) + bottom_color[1] * ratio
        b = top_color[2] * (1 - ratio) + bottom_color[2] * ratio
        pygame.draw.line(surface, (int(r), int(g), int(b)), (0, y), (surface.get_width(), y))


def bounce_from_paddle(paddle):
    
    global ball_dx, ball_dy, ball_x, ball_y, score
    if ball_rect.colliderect(paddle):
        if ball_y + BALL_RADIUS - ball_dy <= paddle.top:
            ball_dy *= -1
            ball_y = paddle.top - BALL_RADIUS
            score += 1
            ball_dx += BALL_ACCELERATION * (1 if ball_dx > 0 else -1)
            ball_dy -= BALL_ACCELERATION
        elif ball_x < paddle.left and ball_dx > 0:
            ball_dx *= -1
            ball_x = paddle.left - BALL_RADIUS
        elif ball_x > paddle.right and ball_dx < 0:
            ball_dx *= -1
            ball_x = paddle.right + BALL_RADIUS

def draw_shadows():
    # Тень под мячом
    if game_started:
        shadow_surf = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), shadow_surf.get_rect())
        shadow_pos = (ball_x - BALL_RADIUS + 5 , ball_y + BALL_RADIUS - 75)
        screen.blit(shadow_surf, shadow_pos)

    # Тени под платформами
    for paddle in [paddle_left, paddle_right]:
        shadow_width = PADDLE_WIDTH
        shadow_height = 30
        shadow_surf = pygame.Surface((shadow_width  -15 , shadow_height +180), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 70), shadow_surf.get_rect())
        shadow_pos = (paddle.x+21, paddle.y + PADDLE_HEIGHT - 180)
        screen.blit(shadow_surf, shadow_pos)

running = True
paddle_shake_timer = 0
while running:
    draw_vertical_gradient(screen, (255, 235, 240), (255, 210, 220))  # светло-розовый → клубничный


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            reset_game()
        if not game_started and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_started = True

    keys = pygame.key.get_pressed()

    # Управление левой платформой (только в своей половине)
    if keys[pygame.K_z] and paddle_left.left > BORDER_OFFSET + BLACK_BORDER:
        paddle_left.x -= PADDLE_SPEED
    if keys[pygame.K_x] and paddle_left.right < SCREEN_WIDTH // 2:
        paddle_left.x += PADDLE_SPEED

    # Управление правой платформой (только в своей половине)
    if keys[pygame.K_c] and paddle_right.left > SCREEN_WIDTH // 2:
        paddle_right.x -= PADDLE_SPEED
    if keys[pygame.K_v] and paddle_right.right < SCREEN_WIDTH - BORDER_OFFSET - BLACK_BORDER:
        paddle_right.x += PADDLE_SPEED

    if game_started and not game_over:
        ball_x += ball_dx
        ball_y += ball_dy

        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

        if ball_x - BALL_RADIUS <= BORDER_OFFSET + BLACK_BORDER or ball_x + BALL_RADIUS >= SCREEN_WIDTH - BORDER_OFFSET - BLACK_BORDER:
            ball_dx *= -1
        if ball_y - BALL_RADIUS <= BORDER_OFFSET + BLACK_BORDER:
            ball_dy *= -1

        bounce_from_paddle(paddle_left)
        bounce_from_paddle(paddle_right)

        if ball_y + BALL_RADIUS >= SCREEN_HEIGHT - BORDER_OFFSET - BLACK_BORDER:
            if not paddle_left.colliderect(ball_rect) and not paddle_right.colliderect(ball_rect):
                game_over = True

    # ==== ОТРИСОВКА ====
    draw_shadows()

    if game_started:
        screen.blit(ball_image, (ball_x - BALL_RADIUS, ball_y - BALL_RADIUS))

    screen.blit(paddle_image, paddle_left)
    screen.blit(paddle_image, paddle_right)

    # Рамка поверх всего
    pygame.draw.rect(screen, DARK_PINK, (0, 0, SCREEN_WIDTH, BORDER_OFFSET))
    pygame.draw.rect(screen, DARK_PINK, (0, SCREEN_HEIGHT - BORDER_OFFSET, SCREEN_WIDTH, BORDER_OFFSET))
    pygame.draw.rect(screen, DARK_PINK, (0, 0, BORDER_OFFSET, SCREEN_HEIGHT))
    pygame.draw.rect(screen, DARK_PINK, (SCREEN_WIDTH - BORDER_OFFSET, 0, BORDER_OFFSET, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BLACK,
        (BORDER_OFFSET, BORDER_OFFSET, SCREEN_WIDTH - 2 * BORDER_OFFSET, SCREEN_HEIGHT - 2 * BORDER_OFFSET),
        BLACK_BORDER)

    # Счёт
    score_text = font.render(f"{score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 75))

    # Тексты
    if game_over:
        fade_alpha += 5
        if fade_alpha > 255:
            fade_alpha = 255

        game_over_text = "Game Over. Score: " + str(score)
        restart_text = "Press Enter to Restart"

        draw_text_with_fade(game_over_text, font, BLACK,
                            (SCREEN_WIDTH // 2 - font.size(game_over_text)[0] // 2, SCREEN_HEIGHT // 2 - 30),
                            screen, fade_alpha)
        draw_text_with_fade(restart_text, font, BLACK,
                            (SCREEN_WIDTH // 2 - font.size(restart_text)[0] // 2, SCREEN_HEIGHT // 2 + 20),
                            screen, fade_alpha)
    elif not game_started:
        start_text = "Press Enter to Start"
        left_controls = "Left Paddle: Z (left), X (right)"
        right_controls = "Right Paddle: C (left), V (right)"


        draw_text_with_fade(start_text, font, BLACK,
                            (SCREEN_WIDTH // 2 - font.size(start_text)[0] // 2, SCREEN_HEIGHT // 2 - 60),
                            screen, 255)
        draw_text_with_fade(left_controls, small_font, BLACK,
                            (SCREEN_WIDTH // 2 - small_font.size(left_controls)[0] // 2, SCREEN_HEIGHT // 2 + 10),
                            screen, 255)
        draw_text_with_fade(right_controls, small_font, BLACK,
                            (SCREEN_WIDTH // 2 - small_font.size(right_controls)[0] // 2, SCREEN_HEIGHT // 2 + 45),
                            screen, 255)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
