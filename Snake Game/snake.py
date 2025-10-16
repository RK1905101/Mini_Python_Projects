import sys
import random
import pygame

# -----------------------------
# Configuration
# -----------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20
FPS = 15

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (220, 50, 50)
COLOR_GREEN_HEAD = (0, 220, 0)
COLOR_GREEN_TAIL = (0, 120, 0)

DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)


def is_opposite_direction(dir_a, dir_b):
    return dir_a[0] == -dir_b[0] and dir_a[1] == -dir_b[1]


def grid_center_start(width, height, block):
    start_x = (width // block // 2) * block
    start_y = (height // block // 2) * block
    return start_x, start_y


def random_food_position(snake_body):
    while True:
        x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
        y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
        if (x, y) not in snake_body:
            return x, y


def lerp_color(color_a, color_b, t):
    ax, ay, az = color_a
    bx, by, bz = color_b
    return (int(ax + (bx - ax) * t), int(ay + (by - ay) * t), int(az + (bz - az) * t))


def draw_snake(surface, snake_body):
    length = len(snake_body)
    for index, (x, y) in enumerate(snake_body):
        t = 0.0 if length <= 1 else index / (length - 1)
        color = lerp_color(COLOR_GREEN_HEAD, COLOR_GREEN_TAIL, t)
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, color, rect)


def draw_food(surface, pos):
    rect = pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(surface, COLOR_RED, rect)


def render_score(surface, font, score):
    text = font.render(f"Score: {score}", True, COLOR_WHITE)
    surface.blit(text, (10, 6))


def render_center_text(surface, font, text, color):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    surface.blit(rendered, rect)


def render_overlay(surface, text_lines, big_font, small_font):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    y = WINDOW_HEIGHT // 2 - 30 * len(text_lines) // 2
    for idx, (text, size) in enumerate(text_lines):
        font = big_font if size == "big" else small_font
        rendered = font.render(text, True, COLOR_WHITE)
        rect = rendered.get_rect(center=(WINDOW_WIDTH // 2, y + idx * 40))
        surface.blit(rendered, rect)


def main():
    pygame.init()
    pygame.display.set_caption("Snake (pygame)")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    score_font = pygame.font.SysFont(None, 26)
    big_font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    running = True
    while running:
        # Initialize game state
        start_x, start_y = grid_center_start(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
        snake = [
            (start_x, start_y),
            (start_x - BLOCK_SIZE, start_y),
            (start_x - 2 * BLOCK_SIZE, start_y),
        ]
        direction = DIRECTION_RIGHT
        food = random_food_position(snake)
        score = 0
        paused = False
        game_over = False
        restart_requested = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        pygame.quit()
                        sys.exit(0)

                    if not game_over:
                        if event.key in (pygame.K_p, pygame.K_SPACE):
                            paused = not paused

                        if not paused:
                            if event.key == pygame.K_UP:
                                if not is_opposite_direction(direction, DIRECTION_UP):
                                    direction = DIRECTION_UP
                            elif event.key == pygame.K_DOWN:
                                if not is_opposite_direction(direction, DIRECTION_DOWN):
                                    direction = DIRECTION_DOWN
                            elif event.key == pygame.K_LEFT:
                                if not is_opposite_direction(direction, DIRECTION_LEFT):
                                    direction = DIRECTION_LEFT
                            elif event.key == pygame.K_RIGHT:
                                if not is_opposite_direction(direction, DIRECTION_RIGHT):
                                    direction = DIRECTION_RIGHT
                    else:
                        if event.key == pygame.K_r:
                            restart_requested = True

            if not paused and not game_over:
                head_x, head_y = snake[0]
                dx, dy = direction
                new_head = (head_x + dx * BLOCK_SIZE, head_y + dy * BLOCK_SIZE)

                # Wall collision
                if (
                    new_head[0] < 0
                    or new_head[0] >= WINDOW_WIDTH
                    or new_head[1] < 0
                    or new_head[1] >= WINDOW_HEIGHT
                ):
                    game_over = True
                # Self collision
                elif new_head in snake:
                    game_over = True
                else:
                    snake.insert(0, new_head)
                    if new_head == food:
                        score += 1
                        food = random_food_position(snake)
                    else:
                        snake.pop()

            # Draw
            screen.fill(COLOR_BLACK)
            draw_food(screen, food)
            draw_snake(screen, snake)
            render_score(screen, score_font, score)

            if paused and not game_over:
                render_overlay(
                    screen,
                    [
                        ("Paused", "big"),
                        ("Press P/Space to resume  •  Q/Esc to quit", "small"),
                    ],
                    big_font,
                    small_font,
                )

            if game_over:
                render_overlay(
                    screen,
                    [
                        ("Game Over", "big"),
                        (f"Final Score: {score}", "small"),
                        ("Press R to Restart  •  Q/Esc to Quit", "small"),
                    ],
                    big_font,
                    small_font,
                )

            pygame.display.flip()
            clock.tick(FPS)

            if game_over and restart_requested:
                break  # restart inner loop with fresh state

        # Restart falls through; running stays True to start a new round


if __name__ == "__main__":
    main()
