import time

import pygame
from Game import Game
from Pygame.Resource import Resource
import random
from enum import Enum


# =====================================================================
#   Stars System
# =====================================================================

class Star:
    def __init__(self, screen_w, screen_h):
        self.size = None
        self.y = None
        self.x = None
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screen_w)
        self.y = random.randint(0, self.screen_h)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += 1
        if self.y > self.screen_h:
            self.y = 0
            self.x = random.randint(0, self.screen_w)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.size)


# =====================================================================
#   Fonts Manager
# =====================================================================

class Fonts:
    small = None
    large = None
    emoji = None


# =====================================================================
#   Game Status Enum
# =====================================================================

class GameStatus(Enum):
    WON = 1
    LOSE = 2
    QUIT = 3
    BACK = 4


# =====================================================================
#   Main Setup
# =====================================================================

pygame.init()
screen = pygame.display.set_mode((1500, 720))

SCREEN_W, SCREEN_H = screen.get_size()
clock = pygame.time.Clock()

Fonts.small = pygame.font.SysFont("Arial", 32)
Fonts.large = pygame.font.SysFont("Arial", 48)
Fonts.emoji = pygame.font.SysFont("Segoe UI Emoji", 64)

pygame.mixer.music.load(Resource.path(r"Sounds\ma.mp3"))
pygame.mixer.music.set_volume(0.3)

levels = [
    "level1.txt", "level3.txt", "level2.txt", "level4.txt",
    "level5.txt", "level6.txt", "level7.txt", "level9.txt",
    "level10.txt", "level14.txt", "level15.txt", "level13.txt",
]

stars = [Star(SCREEN_W, SCREEN_H) for _ in range(40)]

level_rects = []
last_selected_index = None


# =====================================================================
#   Utility
# =====================================================================

def draw_button(rect, color, text):
    pygame.draw.rect(screen, color, rect)
    txt = Fonts.small.render(text, True, (255, 255, 255))
    screen.blit(txt, (rect.x + 20, rect.y + 10))


# =====================================================================
#   Draw Level Selection Screen
# =====================================================================

def draw_level_selection(selected_index=None):
    global level_rects

    screen.fill((30, 30, 30))
    title = Fonts.large.render("Choose level", True, (255, 255, 255))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 10))
    for star in stars:
        star.update()
        star.draw(screen)

    level_rects = []
    for idx, lvl in enumerate(levels):
        color = (76, 175, 80) if idx != selected_index else (255, 200, 0)
        rect = pygame.Rect(500, 80 + idx * 60, 500, 50)
        draw_button(rect, color, lvl.replace(".txt", ""))
        level_rects.append(rect)
    text1 = Fonts.small.render("press esc to Leave", True, (255, 0, 0))
    screen.blit(text1, (10, 10))

    pygame.display.flip()


# =====================================================================
#   Level Selection Loop
# =====================================================================
selected_index = 0
def level_selection_loop():
    selected_index = 0
    draw_level_selection(selected_index)
    total_options = len(levels)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % total_options
                    draw_level_selection(selected_index)

                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % total_options
                    draw_level_selection(selected_index)

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return levels[selected_index]

                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for i, rect in enumerate(level_rects):
                    if rect.collidepoint(pos):
                        return levels[i]

        else:
            draw_level_selection(selected_index)

        clock.tick(60)


# =====================================================================
#   Play Level
# =====================================================================
def algorithm_selection_loop():
    options = ["dfs", "bfs"]
    selected_index = 0

    while True:
        screen.fill((20, 20, 20))

        title = Fonts.large.render("Choose Algorithm", True, (255, 255, 255))
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 50))

        for i, option in enumerate(options):
            color = (76, 175, 80) if i != selected_index else (255, 200, 0)
            rect = pygame.Rect(500, 200 + i * 80, 500, 60)
            pygame.draw.rect(screen, color, rect)
            txt = Fonts.small.render(option.upper(), True, (255, 255, 255))
            screen.blit(txt, (rect.x + 20, rect.y + 15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected_index]
                elif event.key == pygame.K_ESCAPE:
                    return None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                rect = pygame.Rect(500, 200 + selected_index * 80, 500, 60)
                if rect.collidepoint(pos):
                    return options[selected_index]


def play_level(level_file):
    algo = algorithm_selection_loop()
    if algo is None:
        return GameStatus.BACK

    game = Game(screen, Resource.path(f"levels/{level_file}"))
    print(f"starting level {selected_level} solving")

    # start_time = time.time()
    # game.solve(algo)
    # solve_time = time.time() - start_time
    # game.get_solution()
    # print("Solve Time using algorithm ",algo,solve_time,"seconds")
    # game.animate_solution(125)

    game.run()

    return show_end_screen(game.states.get_current_state().GameStatus)

# =====================================================================
#   End Screen
# =====================================================================

def show_end_screen(status):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    if status == "won":
        msg = "🎉 Winner! 🎉"
        color = (0, 255, 0)
    elif status == "lose":
        msg = "😢 Try Again 😢"
        color = (255, 0, 0)
    else:
        return GameStatus.BACK

    text = Fonts.emoji.render(msg, True, color)
    rect = text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 150))
    screen.blit(text, rect)
    back_rect = pygame.Rect(SCREEN_W // 2 - 150, SCREEN_H // 2 + 20, 300, 60)

    pygame.draw.rect(screen, (60, 60, 60), back_rect, border_radius=8)
    back_label = Fonts.small.render("BACK", True, (255, 255, 255))
    lbl_rect = back_label.get_rect(center=back_rect.center)
    screen.blit(back_label, lbl_rect)

    pygame.display.flip()



    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return GameStatus.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return GameStatus.BACK

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return GameStatus.BACK

        clock.tick(60)




# =====================================================================
#   MAIN LOOP
# =====================================================================

while True:

    selected_level = level_selection_loop()
    if selected_level is None:
        break

    result = play_level(selected_level)

    if result == GameStatus.QUIT:
        break

pygame.quit()
