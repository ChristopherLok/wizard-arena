import pygame


class ResolutionManager:
    def __init__(self, screen, base_width=1920, base_height=1080):
        self.screen = screen
        self.base_width = base_width
        self.base_height = base_height
        self.scale_x = screen.get_width() / base_width
        self.scale_y = screen.get_height() / base_height

    def scale_pos(self, x, y):
        return int(x * self.scale_x), int(y * self.scale_y)

    def scale_size(self, w, h):
        return int(w * self.scale_x), int(h * self.scale_y)

    def scale_rect(self, rect):
        x, y = self.scale_pos(rect.x, rect.y)
        w, h = self.scale_size(rect.width, rect.height)
        return pygame.Rect(x, y, w, h)

    def unscale_mouse(self, pos):
        return int(pos[0] / self.scale_x), int(pos[1] / self.scale_y)

    def update_screen(self, screen):
        self.screen = screen
        self.scale_x = screen.get_width() / self.base_width
        self.scale_y = screen.get_height() / self.base_height
