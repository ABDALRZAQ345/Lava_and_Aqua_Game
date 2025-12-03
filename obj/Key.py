import pygame
from Pygame.GameObject import GameObject

class Key(GameObject):
    layer = 6
    color = (200, 160, 200)

    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, screen, tile_size, offset=(0, 0)):
        offset_x, offset_y = offset

        center_x = offset_x + int(self.x * tile_size + tile_size / 2)
        center_y = offset_y + int(self.y * tile_size + tile_size / 2)

        radius = tile_size // 3
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
