import pygame

from Pygame.GameObject import GameObject
from obj.Ground import Ground


class NumericBlock(GameObject):
    def __init__(self, x, y,value):
        super().__init__(x, y)
        self.layer=2
        self.value = value

    def draw(self, screen, tile_size, offset=(0, 0)):
        offset_x, offset_y = offset
        rect = pygame.Rect(
            offset_x + self.x * tile_size,
            offset_y + self.y * tile_size,
            tile_size,
            tile_size
        )

        pygame.draw.rect(screen, (0, 255, 0), rect)

        font = pygame.font.SysFont(None, int(tile_size * 0.6))
        text_surface = font.render(str(self.value), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)

        screen.blit(text_surface, text_rect)

    def decrease(self):
        self.value -= 1
        if self.value <= 0:
            return Ground(self.x, self.y)
        return self