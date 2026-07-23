import pygame


class MainMenu:
    def __init__(self, native_surface, resolution_manager, settings):
        self.settings = settings

        self.screen = native_surface
        self.res = resolution_manager

        # Background
        raw_bg = pygame.image.load("assets/images/menu_b.png").convert()
        self.background = pygame.transform.scale(raw_bg, self.screen.get_size())
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        # Play button
        base_play_size = (450, 100)
        base_play_center = (1920 // 2, 1080 // 2 - 50)

        self.play_image = pygame.image.load("assets/images/play.png").convert_alpha()
        self.play_image = pygame.transform.scale(self.play_image, base_play_size)
        self.play_rect = self.play_image.get_rect(center=base_play_center)

        # Leaderboard button
        base_score_size = (450, 100)
        base_score_center = (1920 // 2, 1080 // 2 + 75)

        self.score_image = pygame.image.load("assets/images/score.png").convert_alpha()
        self.score_image = pygame.transform.scale(self.score_image, base_score_size)
        self.score_rect = self.score_image.get_rect(center=base_score_center)

        # Tutorial button
        base_tutorial_size = (450, 100)
        base_tutorial_center = (1920 // 2, 1080 // 2 + 200)

        self.tutorial_image = pygame.image.load(
            "assets/images/tutorial.png"
        ).convert_alpha()
        self.tutorial_image = pygame.transform.scale(
            self.tutorial_image, base_tutorial_size
        )
        self.tutorial_rect = self.tutorial_image.get_rect(center=base_tutorial_center)

        # Settings button
        base_settings_size = (450, 100)
        base_settings_center = (1920 // 2, 1080 // 2 + +325)

        self.settings_image = pygame.image.load(
            "assets/images/settings.png"
        ).convert_alpha()
        self.settings_image = pygame.transform.scale(
            self.settings_image, base_settings_size
        )
        self.settings_rect = self.settings_image.get_rect(center=base_settings_center)

        # Quit button
        base_quit_size = (450, 100)
        base_quit_center = (1920 // 2, 1080 // 2 + 450)

        self.quit_image = pygame.image.load("assets/images/quit.png").convert_alpha()
        self.quit_image = pygame.transform.scale(self.quit_image, base_quit_size)
        self.quit_rect = self.quit_image.get_rect(center=base_quit_center)

        pygame.mixer.music.set_volume(
            self.settings.music_volume if self.settings.sound_on else 0.0
        )

        # Load click sound
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.play_image, self.play_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.tutorial_image, self.tutorial_rect)
        self.screen.blit(self.settings_image, self.settings_rect)
        self.screen.blit(self.quit_image, self.quit_rect)

        # Draw hitbox for debugging
        # pygame.draw.rect(self.screen, (255, 0, 0), self.play_rect, 2)
        # pygame.draw.rect(self.screen, (0, 255, 0), self.score_rect, 2)
        # pygame.draw.rect(self.screen, (255, 255, 255), self.settings_rect, 2)
        # pygame.draw.rect(self.screen, (255, 255, 255), self.quit_rect, 2)
        # pygame.draw.rect(self.screen, (0, 0, 255), self.tutorial_rect, 2)

    def handle_click(self, pos):
        logical_pos = self.res.unscale_mouse(pos)

        if self.play_rect.collidepoint(logical_pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "start"
        if self.score_rect.collidepoint(logical_pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "score"
        if self.tutorial_rect.collidepoint(logical_pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "tutorial"

        if self.settings_rect.collidepoint(logical_pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return "settings"

        if self.quit_rect.collidepoint(logical_pos):
            pygame.quit()
            exit()
