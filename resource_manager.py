import pygame


class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, path, scale=None):
        if path not in self.images:
            image = pygame.image.load(path).convert_alpha()
            if scale:
                image = pygame.transform.scale(image, scale)
            self.images[path] = image
        return self.images[path]

    def load_sound(self, path):
        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(path)
        return self.sounds[path]

    def load_font(self, path, size):
        key = (path, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(path, size)
        return self.fonts[key]
