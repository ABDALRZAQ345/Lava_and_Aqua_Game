import pygame

from Pygame.GameObject import GameObject
from Pygame.Resource import Resource


class Player(GameObject):
    image =None
    dead_image =None
    layer = 6
    def __init__(self, x, y):
        super().__init__(x, y)
        if Player.image is None:
            Player.image =pygame.image.load(Resource.path("images/player.png")).convert_alpha()
            Player.dead_image = pygame.image.load(Resource.path("images/dead_player.png")).convert_alpha()

    def draw(self, screen, tile_size,offset=(0,0),dead=False):
        offset_x, offset_y = offset
        screen_x = offset_x + self.x * tile_size
        screen_y = offset_y + self.y * tile_size
        if not dead:
            image_scaled = pygame.transform.scale(Player.image, (tile_size, tile_size))
        else:
            image_scaled = pygame.transform.scale(Player.dead_image, (tile_size, tile_size))
        screen.blit(image_scaled,(screen_x, screen_y))


