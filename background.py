import pygame


class Background:
    def __init__(self, image_path, map_width, map_height):
        raw_image = pygame.image.load(image_path).convert()

        self.image = pygame.transform.scale(raw_image, (map_width, map_height))

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect(topleft=(0, 0))

    def draw(self, surface, camera_offset):
        surface.blit(self.image, (-camera_offset[0], -camera_offset[1]))
