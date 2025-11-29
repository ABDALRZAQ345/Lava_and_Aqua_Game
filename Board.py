import struct

import pygame

from Loader import Loader
from obj.Goal import Goal
from obj.Ground import Ground
from obj.Key import Key
from obj.Tube import Tube
from obj.NumericBlock import NumericBlock
from obj.Block import Block
from obj.lava import Lava
from obj.Player import Player
from obj.Wall import Wall
from obj.Water import Water
import xxhash

pack_u32 = struct.Struct("<I").pack
pack_u16 = struct.Struct("<H").pack
class Board:
    tile_size=75
    def __init__(self, filename=None):
        self.grid = None
        self.keys = 0
        self.width = 0
        self.height = 0
        self.player = None
        self.goal = None
        self.GameStatus = "Running"
        self.number_of_moves=0
        if filename:
            self.load_from_file(filename)

    def load_from_file(self, filename):
        loader = Loader()
        data = loader.load_from_file(filename)
        self.grid = data["grid"]
        self.width = data["width"]
        self.height = data["height"]
        self.player = data["player"]
        self.goal = data["goal"]
        self.keys = data["keys"]

    def clone(self):
        new_board = Board.__new__(Board)
        new_board.width = self.width
        new_board.height = self.height
        new_board.tile_size = Board.tile_size
        new_board.GameStatus = self.GameStatus
        new_board.number_of_moves=self.number_of_moves
        new_board.player = Player(self.player.x, self.player.y)

        new_board.keys = self.keys
        new_board.goal = Goal(self.goal.x, self.goal.y,new_board.keys)
        new_grid = [[[] for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                for obj in self.grid[y][x]:
                    if isinstance(obj, Wall):
                        new_obj = Wall(x, y)
                    elif isinstance(obj, Ground):
                        new_obj = Ground(x, y)
                    elif isinstance(obj, Lava):
                        new_obj = Lava(x, y)
                    elif isinstance(obj, Water):
                        new_obj = Water(x, y)
                    elif isinstance(obj, Block):
                        new_obj = Block(x, y)
                    elif isinstance(obj, Tube):
                        new_obj = Tube(x, y)
                    elif isinstance(obj, NumericBlock):
                        new_obj = NumericBlock(x, y, obj.value)
                    elif isinstance(obj, Key):
                        new_obj = Key(x, y)
                    elif isinstance(obj, Player):
                        new_obj = Player(x, y)
                    elif isinstance(obj, Goal):
                        new_obj = new_board.goal
                    else:
                        new_obj = Ground(x, y)

                    new_grid[y][x].append(new_obj)
        new_board.grid = new_grid
        return new_board



    def get_object_at(self, x, y):
        return self.grid[y][x]


    def handleMovment(self, direction):


        dx, dy = direction
        new_x, new_y = self.player.x + dx, self.player.y + dy

        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return False

        target_layers = self.grid[new_y][new_x]

        for obj in target_layers:
            if isinstance(obj, (Wall, Tube, NumericBlock)):
                return False


        block_to_push = None
        for obj in target_layers:
            if isinstance(obj, Block):
                block_to_push = obj
                break

        if block_to_push:
            push_x = new_x + dx
            push_y = new_y + dy
            if not (0 <= push_x < self.width and 0 <= push_y < self.height):
                return False

            push_target_layers = self.grid[push_y][push_x]

            for obj in push_target_layers:
                if isinstance(obj, (Wall, Block, Tube, NumericBlock)):
                    return False

            push_cell = self.grid[push_y][push_x]

            push_cell = [layer for layer in push_cell if not isinstance(layer, (Lava, Water))]

            push_cell.append(Block(push_x, push_y))

            self.grid[push_y][push_x] = push_cell

            self.grid[new_y][new_x] = [layer for layer in self.grid[new_y][new_x] if layer != block_to_push]

        self.player.x, self.player.y = new_x, new_y

        self.updatelavandwater()
        self.updateNumericBlocks()
        self.collect_keys()
        self.game_status()
        self.number_of_moves+=1
        return True

    def game_status(self):

        if self.goal.x == self.player.x and self.player.y == self.goal.y and self.keys == 0:
            self.GameStatus = "won"
            return True
        player_layers = self.grid[self.player.y][self.player.x]
        if any(isinstance(obj, (Lava, Wall)) for obj in player_layers):
            self.GameStatus = "lose"
            self.player.dead()
        return  False

    def collect_keys(self):
        player_layers = self.grid[self.player.y][self.player.x]


        for obj in player_layers:
            if isinstance(obj, Key):
                player_layers.remove(obj)
                self.keys -= 1
                if self.keys == 0:
                    self.goal.updateKeysLeft(self.keys)
                return

    def updateNumericBlocks(self):
        for y in range(self.height):
            for x in range(self.width):
                for i, obj in enumerate(self.grid[y][x]):
                    if isinstance(obj, NumericBlock):
                        self.grid[y][x][i] = obj.decrease()

    def draw(self, screen):
        board_pixel_width = self.width * Board.tile_size
        board_pixel_height = self.height * Board.tile_size

        offset_x = (screen.get_width() - board_pixel_width) // 2
        offset_y = (screen.get_height() - board_pixel_height) // 2

        if self.goal:
            self.goal.draw(screen, Board.tile_size, offset=(offset_x, offset_y))


        for y in range(self.height):
            for x in range(self.width):
                cell_layers = self.grid[y][x]
                if cell_layers:
                    sorted_layers = sorted(cell_layers, key=lambda obj: obj.layer)
                    for obj in sorted_layers:
                        obj.draw(screen, Board.tile_size, offset=(offset_x, offset_y))



        if self.player:
            self.player.draw(screen, Board.tile_size, offset=(offset_x, offset_y))

    def is_goal_surrounded_by_lava(self):
        gx, gy = self.goal.x, self.goal.y

        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]
        LET=0
        for dx, dy in directions:
            nx, ny = gx + dx, gy + dy

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                LET+=1
                continue

            cell_layers = self.grid[ny][nx]
            if any(isinstance(obj, (Lava,Wall)) for obj in cell_layers):
                LET+=1

        return LET == 4

    # def updatelavandwater(self):
    #     new_grid = [[list(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)]
    #     # first spread the water then lava so that there is 2 loops
    #
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             for obj in self.grid[y][x]:
    #                 if isinstance(obj, Water) :
    #                     for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    #                         nx, ny = x + dx, y + dy
    #                         if 0 <= nx < self.width and 0 <= ny < self.height:
    #                             target_layers = new_grid[ny][nx]
    #
    #                             if any(isinstance(layer, (Wall, Block, NumericBlock)) for layer in target_layers):
    #                                 continue
    #
    #                             if any(isinstance(layer, Lava) for layer in target_layers):
    #                                 new_grid[ny][nx] = [layer for layer in target_layers if not isinstance(layer, Lava)]
    #                                 new_grid[ny][nx].append(Wall(nx, ny))
    #                             elif not any(isinstance(layer, (Water)) for layer in target_layers):
    #                                 new_grid[ny][nx].append(Water(nx, ny))
    #
    #     last_grid = [[list(new_grid[y][x]) for x in range(self.width)] for y in range(self.height)]
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             for obj in new_grid[y][x]:
    #                 if isinstance(obj, Lava) :
    #                     for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    #                         nx, ny = x + dx, y + dy
    #                         if 0 <= nx < self.width and 0 <= ny < self.height:
    #                             target_layers = last_grid[ny][nx]
    #
    #                             if any(isinstance(layer, (Wall, Block, NumericBlock)) for layer in target_layers):
    #                                 continue
    #
    #                             if any(isinstance(layer, Water) for layer in target_layers):
    #                                 last_grid[ny][nx] = [layer for layer in target_layers if
    #                                                      not isinstance(layer, Water)]
    #                                 last_grid[ny][nx].append(Wall(nx, ny))
    #                             elif not any(isinstance(layer, (Lava)) for layer in target_layers):
    #                                 last_grid[ny][nx].append(Lava(nx, ny))
    #
    #     self.grid = last_grid
    def updatelavandwater(self):

        new_grid = [[list(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                for obj in self.grid[y][x]:
                    if isinstance(obj, Water):
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:

                                target_layers = new_grid[ny][nx]

                                if any(isinstance(l, (Wall, Block, NumericBlock)) for l in target_layers):
                                    continue

                                if any(isinstance(l, Lava) for l in target_layers):
                                    new_grid[ny][nx] = [l for l in target_layers if not isinstance(l, Lava)]
                                    new_grid[ny][nx].append(Wall(nx, ny))
                                elif not any(isinstance(l, Water) for l in target_layers):
                                    new_grid[ny][nx].append(Water(nx, ny))

        last_grid = [[list(new_grid[y][x]) for x in range(self.width)] for y in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                for obj in new_grid[y][x]:
                    if isinstance(obj, Lava):
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:

                                target_layers = last_grid[ny][nx]

                                if any(isinstance(l, (Wall, Block, NumericBlock)) for l in target_layers):
                                    continue

                                if any(isinstance(l, Water) for l in target_layers):
                                    last_grid[ny][nx] = [l for l in target_layers if not isinstance(l, Water)]
                                    last_grid[ny][nx].append(Wall(nx, ny))
                                elif not any(isinstance(l, Lava) for l in target_layers):
                                    last_grid[ny][nx].append(Lava(nx, ny))

        self.grid = last_grid

    def check_can_move(self, direction):


        dx, dy =direction
        new_x, new_y = self.player.x + dx, self.player.y + dy

        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return False

        target_layers = self.get_object_at(new_x, new_y)


        if any(isinstance(obj, (Wall, Tube, NumericBlock)) for obj in target_layers):
            return False


        block_to_push = None
        for obj in target_layers:
            if isinstance(obj, Block):
                block_to_push = obj
                break

        if block_to_push:
            push_x = new_x + dx
            push_y = new_y + dy
            if not (0 <= push_x < self.width and 0 <= push_y < self.height):
                return False

            push_target_layers = self.get_object_at(push_x, push_y)
            if any(isinstance(obj, (Wall, Block, Tube, NumericBlock)) for obj in push_target_layers):
                return False

        return True

    def get_available_moves(self):
        moves = []

        directions = {
            (1, 0): "Right",
            (0, -1): "Up",
            (0, 1): "Down",
            (-1, 0): "Left",


        }

        for direction, name in directions.items():
            if self.check_can_move(direction):
                moves.append((direction, name))

        return moves

    type_map = {

        Wall: 0,
        Block: 1,
        Water: 2,
        Lava: 3,
        NumericBlock: 4,
        Key: 5,

    }


    def hashed(self):
        h = xxhash.xxh64()

        for row in self.grid:
            for cell in row:
                cell_value = 0
                for obj in cell:
                    t = type(obj)
                    if t in {Ground, Tube, Player, Goal}:
                        continue
                    type_id = Board.type_map[t]
                    value = getattr(obj, "value", 0)
                    object_code = (type_id << 6) | value
                    cell_value ^= object_code
                h.update(pack_u32(cell_value))
        h.update(pack_u16(self.player.x))
        h.update(pack_u16(self.player.y))

        return h.hexdigest()







