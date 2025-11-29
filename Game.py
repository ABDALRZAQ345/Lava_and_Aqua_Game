import pygame
from fontTools.ttLib.ttVisitor import visit
from pywin.dialogs import status
from collections import deque

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
        self.visited = set()
        self.solution=[]

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
        #  print(self.current_board.get_available_moves())

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

    visited = []

    def undo(self):
        self.current_board = self.states.get_current_state()

    def solve(self, algorithm="dfs"):
        self.visited = set()
        self.solution = []
        self.moves=0
        if algorithm == "dfs":
            self.moves=self.dfs(self.current_board)
        else:
            self.moves = self.bfs(self.current_board)

        return self.moves > 0

    def get_solution(self):
        self.solution = self.solution[::-1]
        print(self.solution)
        print("solved in ", self.moves, "move")
        print("states", len(self.visited))





    def dfs(self, board):
       state=board.hashed()
       if state in self.visited or board.number_of_moves >= 200:
           return False
       if board.GameStatus == "won":
           return board.number_of_moves
       if board.GameStatus == "lose" :
           return False
       self.visited.add(state)
       ret=0
       moves=board.get_available_moves()
       for direction , name in moves:
            new_board=board.clone()
            new_board.handleMovment(direction)
            ret = self.dfs(new_board)
            if ret:
                self.solution.append(name)
                break
       return ret




    def bfs(self, start_board):
        start_state = start_board.hashed()

        queue = deque([start_board])
        self.visited = set([start_state])
        visited_nodes=0
        parent = {start_state: (None, None)}

        while queue:
            board = queue.popleft()
            state = board.hashed()
            visited_nodes+=1
            if board.GameStatus == "won" :
                print("visited nodes: ", visited_nodes)
                self.reconstruct_path(parent, state)
                return board.number_of_moves
            if board.GameStatus == "lose" or board.is_goal_surrounded_by_lava() or board.number_of_moves > 50 :
                continue
            for direction, name in board.get_available_moves():
                new_board = board.clone()
                new_board.handleMovment(direction)
                new_state = new_board.hashed()

                if new_state not in self.visited:
                    self.visited.add(new_state)
                    parent[new_state] = (state, name)
                    queue.append(new_board)
        return 0

    def reconstruct_path(self, parent, final_state):

        state = final_state

        while True:
            prev_state, move = parent[state]
            if prev_state is None:
                break
            self.solution.append(move)
            state = prev_state

    def animate_solution(self, delay_ms=300):


        if not self.solution:
            return

        move_to_dir = {
            "Left": (-1, 0),
            "Right": (1, 0),
            "Up": (0, -1),
            "Down": (0, 1),
        }

        for move in self.solution:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            direction = move_to_dir.get(move)
            if not direction:
                print("Unknown move:", move)
                continue

            moved = self.current_board.handleMovment(direction)
            if moved:
                self.states.push_state(self.current_board)
                self.current_board = self.states.get_current_state()

            self.draw()

            pygame.time.wait(delay_ms)

            self.clock.tick(60)

