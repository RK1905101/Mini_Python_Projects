import numpy as np
from scipy.integrate import solve_ivp
import pygame
import sys

# --------------------------------------------
def two_body_ode(t, y, G, m1, m2):
    x1, y1, x2, y2, vx1, vy1, vx2, vy2 = y
    r1 = np.array([x1, y1])
    r2 = np.array([x2, y2])
    r12 = r2 - r1
    norm_r = np.linalg.norm(r12)
    a1 = G * m2 * r12 / norm_r**3
    a2 = -G * m1 * r12 / norm_r**3
    return [vx1, vy1, vx2, vy2, a1[0], a1[1], a2[0], a2[1]]


# --------------------------------------------
G = 6.67430e-11
dt = 3600

def make_state(mode, m1, m2, r, v1_scale=0, v2_scale=0):
    if mode == "Circular":
        m1 = m2 = 1e22
        r = 1e8
        v = np.sqrt(G * (m1 + m2) / r)
        r1 = [-r / 2, 0]
        r2 = [r / 2, 0]
        v1 = [0, v * m2 / (m1 + m2)]
        v2 = [0, -v * m1 / (m1 + m2)]
    elif mode == "Elliptical":
        m1 = 5.972e24
        m2 = 7.348e22
        r = 384400e3
        v = np.sqrt(G * (m1 + m2) / r)
        r1 = [0, 0]
        r2 = [r, 0]
        v1 = [0, 0]
        v2 = [0, 0.6 * v]
    elif mode == "Spinning":
        m1 = m2 = 1e24
        r = 1.5e8
        v = np.sqrt(G * (m1 + m2) / r)
        r1 = [-r / 2, 0]
        r2 = [r / 2, 0]
        v1 = [0, v * m2 / (m1 + m2)]
        v2 = [0, -v * m1 / (m1 + m2)]
    elif mode == "Other":
        v = np.sqrt(G * (m1 + m2) / r)
        r1 = [0, 0]
        r2 = [r, 0]
        v1 = [0, v1_scale * v]
        v2 = [0, v2_scale * v]
    else:
        raise ValueError("Invalid mode")
    return np.array(r1 + r2 + v1 + v2), m1, m2, r

# propagation of orbit uses Range-Kutta of order 5(4)
def propagate_orbit(state, t, dt, m1, m2):
    sol = solve_ivp(
        lambda t, y: two_body_ode(t, y, G, m1, m2),
        t_span=[t, t+dt],
        y0=state,
        method='RK45',
        rtol=1e-9, atol=1e-9
    )
    return sol.y[:, -1], t + dt


# --------------------------------------------
pygame.init()
WIDTH, HEIGHT = 1000, 800
SIDEBAR_WIDTH = 260
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

WHITE = (255, 255, 255)
EARTH_COLOR = (255, 165, 0)
SAT_COLOR = (255, 0, 0)
TRAIL1_COLOR = (255, 220, 180)
TRAIL2_COLOR = (150, 255, 255)
SIDEBAR_BG = (25, 25, 45)

scale = 1e-6
prev_scale = scale
trail_1, trail_2 = [], []
TIME_SCALE = 4
t = 0

def to_screen_coords(pos, com, scale):
    x, y = pos
    cx, cy = com
    return int((WIDTH - SIDEBAR_WIDTH) / 2 + (x-cx) * scale), int(HEIGHT / 2 - (y-cy) * scale)


# Preset logic
presets = ["Circular", "Elliptical", "Spinning", "Other"]
active_preset = "Elliptical"
custom = {
    "m1": 5.972e24,
    "m2": 7.348e22,
    "r": 384400e3,
    "v1_scale": 0.0,
    "v2_scale": 0.6,
}
state, m1, m2, r = make_state(active_preset, **custom)

t = 0


def draw_checkbox(x, y, label, checked):
    pygame.draw.rect(screen, (80, 80, 100), (x, y, 20, 20))
    if checked:
        pygame.draw.rect(screen, (120, 200, 255), (x+3, y+3, 14, 14))
    text = font.render(label, True, WHITE)
    screen.blit(text, (x + 30, y - 2))
    return pygame.Rect(x, y, 20, 20)


def draw_slider(x, y, label, val, minv, maxv, width=150):
    pygame.draw.rect(screen, (70, 70, 90), (x, y + 15, width, 5))
    ratio = (val - minv) / (maxv - minv)
    handle_x = x + int(ratio * width)
    pygame.draw.circle(screen, (120, 200, 255), (handle_x, y + 17), 7)
    text = font.render(f"{label}: {val:.2e}", True, WHITE)
    screen.blit(text, (x, y - 5))
    return pygame.Rect(x, y + 10, width, 15), (minv, maxv)


def draw_sidebar():
    pygame.draw.rect(screen, SIDEBAR_BG, (WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
    base_x = WIDTH - SIDEBAR_WIDTH + 10
    y = 40
    global active_preset
    rects = {}

    # preset boxes
    for p in presets:
        rects[p] = draw_checkbox(base_x, y, p, active_preset == p)
        y += 35

    # sliders if other selected
    slider_rects = {}
    if active_preset == "Other":
        y += 15
        for key, (mn, mx) in {
            "m1": (1e20, 1e26),
            "m2": (1e20, 1e26),
            "r": (1e6, 1e9),
            "v1_scale": (0.0, 2.0),
            "v2_scale": (0.0, 2.0),
        }.items():
            rect, limits = draw_slider(base_x, y, key, custom[key], mn, mx)
            slider_rects[key] = (rect, limits)
            y += 50


    hint = font.render("[T/G] Speed | [+/-] Zoom | [ESC] Quit", True, (200, 200, 255))
    screen.blit(hint, (base_x, HEIGHT - 30))
    return rects, slider_rects


# --------------------------------------------
running = True
dragging = None
while running:
    screen.fill((5, 5, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if mx > WIDTH - SIDEBAR_WIDTH:
                # Check for preset box clicks
                for p, rect in draw_sidebar()[0].items():
                    if rect.collidepoint(mx, my):
                        active_preset = p
                        state, m1, m2, r = make_state(active_preset, **custom)
                        trail_1.clear()
                        trail_2.clear()
                        break
                # Check for slider drag
                if active_preset == "Other":
                    _, sliders = draw_sidebar()
                    for key, (rect, limits) in sliders.items():
                        if rect.collidepoint(mx, my):
                            dragging = (key, limits)
                            break

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Handle dragging for sliders
    if dragging:
        mx, my = pygame.mouse.get_pos()
        key, (minv, maxv) = dragging
        slider_x = WIDTH - SIDEBAR_WIDTH + 10
        rel_x = mx - (slider_x)
        rel_x = np.clip(rel_x, 0, 150)
        ratio = rel_x / 150
        custom[key] = minv + ratio * (maxv - minv)
        state, m1, m2, r = make_state(active_preset, **custom)
        trail_1.clear()
        trail_2.clear()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_t]:
        TIME_SCALE *= 1.1
    if keys[pygame.K_g]:
        TIME_SCALE /= 1.1
    if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
        scale *= 1.05
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        scale /= 1.05

    for _ in range(int(TIME_SCALE)):
        state, t = propagate_orbit(state, t, dt, m1, m2)

    x1, y1, x2, y2 = state[:4]
    pos_1, pos_2 = np.array([x1, y1]), np.array([x2, y2])
    com = (pos_1 * m1 + pos_2 * m2) / (m1 + m2)
    screen_pos1 = to_screen_coords(pos_1, com, scale)
    screen_pos2 = to_screen_coords(pos_2, com, scale)
    trail_1.append(screen_pos1)
    trail_2.append(screen_pos2)

    # trail not too long not too short
    trail_1 = trail_1[-25:]
    trail_2 = trail_2[-25:]

    if len(trail_1) > 1:
        pygame.draw.lines(screen, TRAIL1_COLOR, False, trail_1, 1)
    if len(trail_2) > 1:
        pygame.draw.lines(screen, TRAIL2_COLOR, False, trail_2, 1)
    pygame.draw.circle(screen, EARTH_COLOR, screen_pos1, 4)
    pygame.draw.circle(screen, SAT_COLOR, screen_pos2, 4)

    speed_text = font.render(f"Zoom: {scale:.1e} | Speed x{TIME_SCALE:,.0f}", True, (200, 200, 255))
    screen.blit(speed_text, (10, 10))

    preset_rects, slider_rects = draw_sidebar()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
