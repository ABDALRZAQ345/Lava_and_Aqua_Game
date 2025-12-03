import pygame
from Pygame.GameObject import GameObject
from Pygame.Resource import Resource


class Wall(GameObject):
    image = None
    layer=5
    def __init__(self, x, y):
        super().__init__(x, y)

        if Wall.image is None:
            Wall.image = pygame.image.load(Resource.path("images/wall.png")).convert_alpha()

    def draw(self, screen, tile_size,offset=(0,0)):
        offset_x, offset_y = offset
        screen_x = offset_x + self.x * tile_size
        screen_y = offset_y + self.y * tile_size
        image_scaled = pygame.transform.scale(Wall.image, (tile_size, tile_size))
        screen.blit(image_scaled, (screen_x, screen_y))