import pygame

BASE_WIDTH = 1920
BASE_HEIGHT = 1080


class PauseScreen:
    def __init__(self, res, settings):
        self.settings = settings

        # Load click sound
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

        self.res = res

        # Load images
        self.image = pygame.image.load("assets/images/pause_b.png").convert_alpha()
        raw_resume = pygame.image.load("assets/images/resume.png").convert_alpha()
        raw_settings = pygame.image.load("assets/images/settings.png").convert_alpha()
        raw_menu = pygame.image.load("assets/images/menu.png").convert_alpha()

        # Base button size
        base_button_size = (800, 150)
        scaled_button_size = (
            int(base_button_size[0] * self.res.scale_x),
            int(base_button_size[1] * self.res.scale_y),
        )

        # Scale buttons
        self.resume_img = pygame.transform.smoothscale(raw_resume, scaled_button_size)
        self.settings_img = pygame.transform.smoothscale(
            raw_settings, scaled_button_size
        )
        self.menu_img = pygame.transform.smoothscale(raw_menu, scaled_button_size)

        # Position buttons
        self.resume_rect = self.resume_img.get_rect(
            center=(BASE_WIDTH // 2, BASE_HEIGHT // 2 - 150)
        )
        self.settings_rect = self.settings_img.get_rect(
            center=(BASE_WIDTH // 2, BASE_HEIGHT // 2 + 0)
        )
        self.menu_rect = self.menu_img.get_rect(
            center=(BASE_WIDTH // 2, BASE_HEIGHT // 2 + 150)
        )

    def draw(self, surface):
        pause_rect = self.image.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT // 2))
        surface.blit(self.image, pause_rect)
        surface.blit(self.resume_img, self.resume_rect)
        surface.blit(self.settings_img, self.settings_rect)
        surface.blit(self.menu_img, self.menu_rect)

    def handle_click(self, mouse_pos):
        logical_pos = self.res.unscale_mouse(mouse_pos)
        if self.resume_rect.collidepoint(logical_pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "resume"
        elif self.settings_rect.collidepoint(logical_pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "settings"
        elif self.menu_rect.collidepoint(logical_pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "menu"
        return None
