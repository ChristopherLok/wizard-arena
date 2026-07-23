import pygame

# Base Resolution
BASE_WIDTH = 1920
BASE_HEIGHT = 1080


class Tutorial:
    def __init__(self, settings):
        self.settings = settings

        # Load click sound
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

        # Fonts
        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        self.font_small = pygame.font.Font(font_path, 16)
        self.font_medium = pygame.font.Font(font_path, 24)
        self.font_large = pygame.font.Font(font_path, 32)
        self.font_heading = pygame.font.Font(font_path, 48)

        # Background
        self.bg_image = pygame.image.load("assets/images/tutorial_b.png").convert()
        self.bg_rect_native = self.bg_image.get_rect(
            center=(BASE_WIDTH // 2, BASE_HEIGHT // 2)
        )

        # Buttons - Back
        base_back_size = (200, 100)
        base_back_center = (1920 // 2 - 800, 1080 // 2 - 450)

        self.back_image = pygame.image.load(
            "assets/images/settings_back.png"
        ).convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, base_back_size)
        self.back_rect = self.back_image.get_rect(center=base_back_center)

        # Controls
        self.wasd_image = pygame.image.load("assets/images/wasd.png").convert_alpha()
        self.mouse_image = pygame.image.load("assets/images/mouse.png").convert_alpha()

    def draw(self, surface):
        # Background
        surface.blit(self.bg_image, self.bg_rect_native)

        # Heading
        heading_text = self.font_heading.render("Controls", True, (0, 0, 0))
        heading_rect = heading_text.get_rect(
            center=(BASE_WIDTH // 2, BASE_HEIGHT // 2 - 475)
        )
        surface.blit(heading_text, heading_rect)

        wasd_rect = self.wasd_image.get_rect(
            center=(BASE_WIDTH // 2 - 400, BASE_HEIGHT // 2)
        )
        surface.blit(self.wasd_image, wasd_rect)

        mouse_rect = self.mouse_image.get_rect(
            center=(BASE_WIDTH // 2 + 400, BASE_HEIGHT // 2)
        )
        surface.blit(self.mouse_image, mouse_rect)

        # Buttons
        surface.blit(self.back_image, self.back_rect)

    def handle_click(self, pos):
        if self.back_rect.collidepoint(pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "menu"
