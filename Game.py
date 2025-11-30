import pygame
from Board import Board
from States import StateManager
import random

stars = []
for _ in range(10):
    stars.append([random.randint(-100, 400), random.randint(0, 800), random.randint(1, 3)])
for _ in range(10):
    stars.append([random.randint(1300, 1600), random.randint(0, 800), random.randint(1, 3)])


class Game:
    def __init__(self, screen, level_file):
        self.moves = None
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.states = StateManager()
        self.states.push_state(Board(level_file))
        self.current_board = self.states.get_current_state()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.current_board.GameStatus = "quit"
                return

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_z:
                self.states.undo()
                self.current_board = self.states.get_current_state()
                return

            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.current_board.GameStatus = "back"
                return

            if event.key == pygame.K_r:
                self.states.reset()
                first_board = self.states.get_current_state().clone()
                self.states.push_state(first_board)
                self.current_board = self.states.get_current_state()
                return
            move_map = {
                pygame.K_LEFT: (-1, 0),
                pygame.K_a: (-1, 0),
                pygame.K_RIGHT: (1, 0),
                pygame.K_d: (1, 0),
                pygame.K_UP: (0, -1),
                pygame.K_w: (0, -1),
                pygame.K_DOWN: (0, 1),
                pygame.K_s: (0, 1),
            }
            if event.key not in move_map:
                return False

            moved = self.current_board.handleMovment(move_map[event.key])

            if moved:
                self.states.push_state(self.current_board)
                self.current_board = self.states.get_current_state()

    def update(self):
        if self.current_board.GameStatus in ("won", "lose"):
            self.running = False

    def draw(self):
        self.screen.fill((30, 30, 30))

        for star in stars:
            x, y, size = star
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size)
            star[1] += 1
            if star[1] > self.screen.get_height():
                star[1] = 0
                star[0] = random.randint(0, self.screen.get_width())
        font = pygame.font.SysFont("Arial", 24)

        text1 = font.render("press Z to Undo", True, (255, 255, 255))
        text2 = font.render("press R to Reset", True, (255, 255, 255))
        text3 = font.render("press esc to Back ", True, (255, 255, 255))
        self.screen.blit(text1, (10, 10))
        self.screen.blit(text2, (10, 40))
        self.screen.blit(text3, (10, 70))

        self.current_board.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(30)

        pygame.event.clear()

    def undo(self):
        self.current_board = self.states.get_current_state()

    def animate_solution(self,solution,delay_ms=300):

        move_to_dir = {
            "Left": (-1, 0),
            "Right": (1, 0),
            "Up": (0, -1),
            "Down": (0, 1),
        }

        for move in solution:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            direction = move_to_dir.get(move)
            if not direction:
                print("Unknown move:", move)
                continue

            self.current_board.handleMovment(direction)
            self.draw()

            pygame.time.wait(delay_ms)

            self.clock.tick(60)

