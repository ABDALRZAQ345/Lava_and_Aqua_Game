from obj.Block import Block
from obj.Goal import Goal
from obj.Ground import Ground
from obj.Key import Key
from obj.NumericBlock import NumericBlock
from obj.Player import Player
from obj.Tube import Tube
from obj.Wall import Wall
from obj.Water import Water
from obj.lava import Lava


class Loader:

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        height = len(lines)
        width = max(len(line.split(',')) for line in lines)
        grid = [[[] for _ in range(width)] for _ in range(height)]

        keys = 0
        player = None
        goal = None

        for y, line in enumerate(lines):
            cells = [c.strip() for c in line.split(',')]
            for x in range(width):
                ch = cells[x] if x < len(cells) else '.'

                grid[y][x].append(Ground(x, y))

                if ch == '#':
                    grid[y][x].append(Wall(x, y))

                elif ch == 'L':
                    grid[y][x].append(Lava(x, y))

                elif ch == 'A':
                    grid[y][x].append(Water(x, y))

                elif ch == 'G':
                    goal = Goal(x, y)
                    grid[y][x].append(goal)

                elif ch == 'P':
                    player = Player(x, y)

                elif ch == 'S':
                    grid[y][x].append(Block(x, y))

                elif ch == "H":
                    grid[y][x].append(Tube(x, y))

                elif ch == "K":
                    keys += 1
                    grid[y][x].append(Key(x, y))

                elif ch.isdigit():
                    grid[y][x].append(NumericBlock(x, y, int(ch)))

        if goal:
            goal.updateKeysLeft(keys)

        return {
            "grid": grid,
            "width": width,
            "height": height,
            "player": player,
            "goal": goal,
            "keys": keys
        }
