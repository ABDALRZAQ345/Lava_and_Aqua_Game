import pygame

from Pygame.Resource import Resource
from Pygame.GameObject import GameObject


class Block(GameObject):
    img= None
    def __init__(self, x, y):
        super().__init__(x, y)
        self.layer=4
        if Block.img is None:
            Block.img = pygame.image.load(Resource.path("images/block.png")).convert_alpha()
    def draw(self, screen, tile_size,offset=(0,0)):
        image_scaled = pygame.transform.scale(Block.img, (tile_size, tile_size))
        offset_x, offset_y = offset
        screen_x = offset_x + self.x * tile_size
        screen_y = offset_y + self.y * tile_size
        screen.blit(image_scaled,(screen_x, screen_y))

