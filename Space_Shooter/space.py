```python
import pygame
import sys
SCREEN_WIDTH, SCREEN_HEIGHT = 960, 640
FPS = 60

TILE = 40
GRAVITY = 4
MOVE_ACC = 60
MAX_MOVE_SPEED = 30
GROUND_FRICTION = 2000
AIR_FRICTION = 40

JUMP_SPEED = 140
COYOTE_TIME = 0.08
JUMP_BUFFER_TIME = 0.08
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
SKY = (125, 200, 255)
GREEN = (80, 200, 120)
BROWN = (140, 100, 60)
GOLD = (255, 200, 0)
RED = (220, 60, 60)


LEVEL_MAP = [
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "                            ",
    "      C             C       ",
    "            BBB             ",
    "        BBB         C     F ",
    "   P                        ",
    "BBBBBBBB     BBBBBBB    BBBB",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBB",
]


def clamp(x, a, b):
    return max(a, min(x, b))



class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def apply(self, rect):
        return pygame.Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)

    def update(self, target_rect):
        self.x = clamp(target_rect.centerx - SCREEN_WIDTH // 2, 0, self.width - SCREEN_WIDTH)
        self.y = clamp(target_rect.centery - SCREEN_HEIGHT // 2, 0, self.height - SCREEN_HEIGHT)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w=TILE, h=TILE, color=BROWN):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = TILE // 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD, (size//2, size//2), size//2)
        self.rect = self.image.get_rect(center=(x + TILE//2, y + TILE//2))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_w=2*TILE):
        super().__init__()
        self.image = pygame.Surface((TILE, TILE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.patrol_w = patrol_w
        self.speed = 80
        self.dir = 1

    def update(self, dt):
        self.rect.x += int(self.dir * self.speed * dt)
        if self.rect.x < self.start_x or self.rect.x > self.start_x + self.patrol_w:
            self.dir *= -1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        w, h = int(TILE * 0.8), int(TILE * 1.2)
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0
        self.can_double_jump = True

    def update(self, dt, keys):
        ax = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            ax -= MOVE_ACC
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            ax += MOVE_ACC

        friction = GROUND_FRICTION if self.on_ground else AIR_FRICTION
        if ax == 0:
            if self.vx > 0:
                self.vx = max(0, self.vx - friction * dt)
            elif self.vx < 0:
                self.vx = min(0, self.vx + friction * dt)
        else:
            self.vx += ax * dt
            self.vx = clamp(self.vx, -MAX_MOVE_SPEED, MAX_MOVE_SPEED)

        self.vy += GRAVITY * dt

        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)

        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
            self.can_double_jump = True
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        self.jump_buffer_timer = max(0.0, self.jump_buffer_timer - dt)

        if not (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]):
            if self.vy < 0:
                self.vy *= 0.55

    def try_jump(self):
        self.jump_buffer_timer = JUMP_BUFFER_TIME

    def perform_jump(self):
        if self.coyote_timer > 0:
            self.vy = -JUMP_SPEED
            self.on_ground = False
            self.coyote_timer = 0.0
            return True
        elif self.can_double_jump:
            self.vy = -JUMP_SPEED
            self.can_double_jump = False
            return True
        return False
def build_level(level_map):
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = None
    finish_rect = None

    h = len(level_map)
    w = max(len(row) for row in level_map)
    level_pixel_w = w * TILE
    level_pixel_h = h * TILE

    for row_i, row in enumerate(level_map):
        for col_i, ch in enumerate(row):
            x = col_i * TILE
            y = row_i * TILE
            if ch in ("G", "B"):
                platforms.add(Platform(x, y, TILE, TILE))
            elif ch == "C":
                coins.add(Coin(x, y))
            elif ch == "E":
                enemies.add(Enemy(x, y - TILE//8))
            elif ch == "P":
                player = Player(x, y)
            elif ch == "F":
                finish_rect = pygame.Rect(x + TILE//8, y + TILE//8, TILE - TILE//4, TILE - TILE//4)

    return platforms, coins, enemies, player, finish_rect, level_pixel_w, level_pixel_h



def resolve_collisions(player, platforms):
    hits = pygame.sprite.spritecollide(player, platforms, dokill=False)
    for p in hits:
        if p.rect.colliderect(player.rect):
            dx = (player.rect.centerx - p.rect.centerx)
            overlap_x = (player.rect.width + p.rect.width) // 2 - abs(dx)
            dy = (player.rect.centery - p.rect.centery)
            overlap_y = (player.rect.height + p.rect.height) // 2 - abs(dy)

            if overlap_x < overlap_y:
                if dx > 0:
                    player.rect.left += overlap_x
                else:
                    player.rect.left -= overlap_x
                player.vx = 0
            else:
                if dy > 0:
                    player.rect.top += overlap_y
                    player.vy = 0
                else:
                    player.rect.top -= overlap_y
                    player.vy = 0


def check_ground(player, platforms):
    probe = player.rect.copy()
    probe.y += 2
    probe.height = 2
    return any(p.rect.colliderect(probe) for p in platforms)
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple 2D Platformer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    platforms, coins, enemies, player, finish_rect, level_w, level_h = build_level(LEVEL_MAP)
    if player is None:
        player = Player(TILE, SCREEN_HEIGHT - 3*TILE)

    all_platforms = platforms
    score = 0
    running = True

    camera = Camera(level_w, level_h)

    jump_was_pressed = False

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    player.try_jump()
                    jump_was_pressed = True
                if event.key == pygame.K_r:
                    platforms, coins, enemies, player, finish_rect, level_w, level_h = build_level(LEVEL_MAP)
                    score = 0
                    camera = Camera(level_w, level_h)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    jump_was_pressed = False

        keys = pygame.key.get_pressed()
        player.update(dt, keys)

        resolve_collisions(player, platforms)

        was_on_ground = player.on_ground
        player.on_ground = check_ground(player, platforms)

        if player.jump_buffer_timer > 0:
            if player.perform_jump():
                player.jump_buffer_timer = 0

        for e in enemies:
            e.update(dt)

        grabbed = pygame.sprite.spritecollide(player, coins, dokill=True)
        score += len(grabbed)

        if pygame.sprite.spritecollideany(player, enemies):
            platforms, coins, enemies, player, finish_rect, level_w, level_h = build_level(LEVEL_MAP)
            score = 0
            camera = Camera(level_w, level_h)
            continue

        if finish_rect:
            if player.rect.colliderect(finish_rect):
                print("You reached the goal! Score:", score)
                platforms, coins, enemies, player, finish_rect, level_w, level_h = build_level(LEVEL_MAP)
                score = 0
                camera = Camera(level_w, level_h)
                continue

        camera.update(player.rect)

        screen.fill(SKY)

        for p in all_platforms:
            r = camera.apply(p.rect)
            screen.blit(p.image, r.topleft)

        for c in coins:
            screen.blit(c.image, camera.apply(c.rect).topleft)

        for e in enemies:
            screen.blit(e.image, camera.apply(e.rect).topleft)

        if finish_rect:
            fr = camera.apply(finish_rect)
            pygame.draw.rect(screen, (80, 160, 255), fr)

        screen.blit(player.image, camera.apply(player.rect).topleft)

        hud = font.render(f"Score: {score}   Press R to restart", True, BLACK)
        screen.blit(hud, (10, 10))

        instructions = font.render("Move: A/D or ←/→   Jump: Space/W/↑", True, BLACK)
        screen.blit(instructions, (10, 34))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```
