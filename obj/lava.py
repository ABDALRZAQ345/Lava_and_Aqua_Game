import pygame

from Pygame.GameObject import GameObject


class Lava(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.layer=1
        self.color = (255, 0, 0)

    def draw(self, screen, tile_size, offset=(0, 0)):
        offset_x, offset_y = offset

        screen_x = offset_x + self.x * tile_size
        screen_y = offset_y + self.y * tile_size

        rect = pygame.Rect(screen_x, screen_y, tile_size, tile_size)
        pygame.draw.rect(screen, self.color, rect)
