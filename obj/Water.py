import pygame

from Pygame.GameObject import GameObject
from Pygame.Resource import Resource


class Water(GameObject):
    image =None
    layer = 1
    def __init__(self, x, y):
        super().__init__(x, y)

        if Water.image is None:
            Water.image =  pygame.image.load(Resource.path("images/water.png")).convert_alpha()

    def draw(self, screen, tile_size,offset=(0,0)):
        image_scaled = pygame.transform.scale(Water.image, (tile_size, tile_size))
        offset_x, offset_y = offset
        screen_x = offset_x + self.x * tile_size
        screen_y = offset_y + self.y * tile_size
        screen.blit(image_scaled, (screen_x, screen_y))

