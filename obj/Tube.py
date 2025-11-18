import pygame

from Pygame.GameObject import GameObject
from Pygame.Resource import Resource


class Tube(GameObject):
    image = None
    def __init__(self, x, y):
        super().__init__(x, y)
        self.layer=2
        if Tube.image is None:
            Tube.image = pygame.image.load(Resource.path("images/tube.png")).convert_alpha()
    def draw(self, screen, tile_size,offset=(0,0)):
        offset_x, offset_y = offset
        screen_x = offset_x + self.x * tile_size
        screen_y = offset_y + self.y * tile_size
        image_scaled = pygame.transform.scale(Tube.image, (tile_size, tile_size))
        screen.blit(image_scaled, (screen_x, screen_y))