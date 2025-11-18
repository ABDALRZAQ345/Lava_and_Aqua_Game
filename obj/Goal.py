import pygame

from Pygame.GameObject import GameObject
from Pygame.Resource import Resource


class Goal(GameObject):
    image = None
    keys_left=None
    def __init__(self, x, y,keys=0):
        super().__init__(x, y)
        self.layer=3
        self.keys_left= keys!=0
        if Goal.image is None:
            Goal.image = pygame.image.load(Resource.path("images/goal.png")).convert_alpha()
            Goal.keys_left = pygame.image.load(Resource.path("images/goal_keys_left.png")).convert_alpha()

    def draw(self, screen, tile_size,offset=(0,0)):
        if self.keys_left:
            image_scaled = pygame.transform.scale(Goal.keys_left, (tile_size, tile_size))
        else:
            image_scaled = pygame.transform.scale(Goal.image, (tile_size, tile_size))
        offset_x, offset_y = offset
        screen_x = offset_x + self.x * tile_size
        screen_y = offset_y + self.y * tile_size
        screen.blit(image_scaled, (screen_x, screen_y))
    def updateKeysLeft(self, keys):
        if keys == 0:
            self.keys_left = False
        else:
            self.keys_left = True
