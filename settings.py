import pygame

# Base Resolution
BASE_WIDTH = 1920
BASE_HEIGHT = 1080


class Settings:
    def __init__(self, res_manager):
        self.res = res_manager

        # Load click sound
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

        # Fonts
        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        self.font_small = pygame.font.Font(font_path, 16)
        self.font_medium = pygame.font.Font(font_path, 24)
        self.font_large = pygame.font.Font(font_path, 32)
        self.font_heading = pygame.font.Font(font_path, 48)

        # Background
        self.bg_image = pygame.image.load("assets/images/settings_b.png").convert()
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

        # Sound Toggle
        self.sound_on = True  # Default toggle state

        self.toggle_on_image = pygame.image.load(
            "assets/images/toggle_on.png"
        ).convert_alpha()
        self.toggle_off_image = pygame.image.load(
            "assets/images/toggle_off.png"
        ).convert_alpha()

        base_toggle_center = (1920 // 2 + 100, 1080 // 2 - 350)
        base_toggle_size = (120, 60)

        self.toggle_rect = pygame.Rect(0, 0, *base_toggle_size)
        self.toggle_rect.center = base_toggle_center

        # SFX Volume
        self.sfx_volume = 1.0  # Range: 0.0 to 1.0

        # Scaling based on display
        screen_width, screen_height = pygame.display.get_surface().get_size()
        scale_x = screen_width / BASE_WIDTH
        scale_y = screen_height / BASE_HEIGHT

        # Buttons
        base_button_size = (80, 80)
        scaled_button_size = (
            int(base_button_size[0] * scale_x),
            int(base_button_size[1] * scale_y),
        )
        self.button_y = int(BASE_HEIGHT // 2 + 50 * scale_y)

        self.plus_image = pygame.image.load("assets/images/plus.png").convert_alpha()
        self.minus_image = pygame.image.load("assets/images/minus.png").convert_alpha()

        self.plus_image = pygame.transform.scale(self.plus_image, scaled_button_size)
        self.minus_image = pygame.transform.scale(self.minus_image, scaled_button_size)

        self.minus_rect = self.minus_image.get_rect()
        self.plus_rect = self.plus_image.get_rect()

        # Volume segments
        segment_path = "assets/images/volume_segment.png"
        self.segment_image = pygame.image.load(segment_path).convert_alpha()

        base_segment_size = (50, 100)
        scaled_segment_size = (
            int(base_segment_size[0] * scale_x),
            int(base_segment_size[1] * scale_y),
        )
        self.segment_image = pygame.transform.scale(
            self.segment_image, scaled_segment_size
        )

        self.segment_width = scaled_segment_size[0]
        self.segment_height = scaled_segment_size[1]
        self.segment_spacing = int(10 * scale_x)

        # Music Volume
        self.music_volume = 0.4  # Range: 0.0 to 1.0
        self.music_button_y = int(BASE_HEIGHT // 2 - 200 * scale_y)

        self.music_minus_rect = self.minus_image.get_rect()
        self.music_plus_rect = self.plus_image.get_rect()

        # Volume Bar Background
        self.volume_bg_image = pygame.image.load(
            "assets/images/volume_background.png"
        ).convert_alpha()

        bg_width = int((self.segment_width * 10 + self.segment_spacing * 9) * 1.1)
        bg_height = int(self.segment_height * 1.08)
        self.volume_bg_image = pygame.transform.scale(
            self.volume_bg_image, (bg_width, bg_height)
        )

        # Fullscreen Toggle
        self.fullscreen = False  # Default to windowed

        self.checkbox_checked = pygame.image.load(
            "assets/images/checkbox_checked.png"
        ).convert_alpha()
        self.checkbox_unchecked = pygame.image.load(
            "assets/images/checkbox_unchecked.png"
        ).convert_alpha()

        base_checkbox_size = (60, 60)
        scaled_checkbox_size = (
            int(base_checkbox_size[0] * scale_x),
            int(base_checkbox_size[1] * scale_y),
        )
        self.checkbox_checked = pygame.transform.scale(
            self.checkbox_checked, scaled_checkbox_size
        )
        self.checkbox_unchecked = pygame.transform.scale(
            self.checkbox_unchecked, scaled_checkbox_size
        )

        checkbox_center = (1920 // 2 + 175, 1080 // 2 + 150)
        self.checkbox_rect = pygame.Rect(0, 0, *scaled_checkbox_size)
        self.checkbox_rect.center = checkbox_center

        # Resolution Options
        self.resolutions = [
            (1280, 720),
            (1600, 900),
            (1920, 1080),
            (2560, 1440),
        ]
        self.selected_resolution_index = 0  # default to 1280, 720

        self.combo_width = 300
        self.combo_height = 60
        combo_center = (1920 // 2 + 100, 1080 // 2 + 250)

        self.combo_rect = pygame.Rect(0, 0, self.combo_width, self.combo_height)
        self.combo_rect.center = combo_center
        self.combo_open = False

    # DRAW
    def draw(self, surface):
        # Background
        surface.blit(self.bg_image, self.bg_rect_native)

        # Heading
        heading_text = self.font_heading.render("Settings", True, (0, 0, 0))
        heading_rect = heading_text.get_rect(
            center=(BASE_WIDTH // 2, BASE_HEIGHT // 2 - 475)
        )
        surface.blit(heading_text, heading_rect)

        # Buttons
        surface.blit(self.back_image, self.back_rect)

        # Sound Toggle
        label = self.font_medium.render("Sound:", True, (0, 0, 0))
        label_rect = label.get_rect(
            midright=(self.toggle_rect.left - 100, self.toggle_rect.centery)
        )
        surface.blit(label, label_rect)

        toggle_image = self.toggle_on_image if self.sound_on else self.toggle_off_image
        scaled_toggle = pygame.transform.scale(toggle_image, self.toggle_rect.size)
        surface.blit(scaled_toggle, self.toggle_rect.topleft)

        # SFX Volume
        anchor_x = self.bg_rect_native.left + 790
        bar_y = self.bg_rect_native.top + 1000

        label = self.font_medium.render("SFX Volume:", True, (0, 0, 0))
        label_rect = label.get_rect(midright=(anchor_x + 350, bar_y - 45))
        surface.blit(label, label_rect)

        bg_width = self.volume_bg_image.get_width()
        bg_height = self.volume_bg_image.get_height()
        bg_x = anchor_x
        surface.blit(self.volume_bg_image, (bg_x, bar_y - 3))

        arrow_offset_y = bar_y + bg_height // 2
        arrow_offset_x = int(60 * self.res.scale_x)

        self.minus_rect.center = (bg_x - arrow_offset_x, arrow_offset_y)
        self.plus_rect.center = (bg_x + bg_width + arrow_offset_x, arrow_offset_y)

        surface.blit(self.minus_image, self.minus_rect)
        surface.blit(self.plus_image, self.plus_rect)

        segment_count = int(self.sfx_volume * 10)
        start_x = bg_x + 10

        for i in range(segment_count):
            segment_x = start_x + i * (self.segment_width + self.segment_spacing)
            segment_rect = pygame.Rect(
                segment_x, bar_y, self.segment_width, self.segment_height
            )
            surface.blit(self.segment_image, segment_rect)

        # Music Volume
        anchor_x = self.bg_rect_native.left + 790
        bar_y = self.bg_rect_native.top + 800

        label = self.font_medium.render("Music Volume:", True, (0, 0, 0))
        label_rect = label.get_rect(midright=(anchor_x + 350, bar_y - 45))
        surface.blit(label, label_rect)

        bg_width = self.volume_bg_image.get_width()
        bg_height = self.volume_bg_image.get_height()
        bg_x = anchor_x
        surface.blit(self.volume_bg_image, (bg_x, bar_y))

        arrow_offset_y = bar_y + bg_height // 2
        arrow_offset_x = int(60 * self.res.scale_x)

        self.music_minus_rect.center = (bg_x - arrow_offset_x, arrow_offset_y)
        self.music_plus_rect.center = (bg_x + bg_width + arrow_offset_x, arrow_offset_y)

        surface.blit(self.minus_image, self.music_minus_rect)
        surface.blit(self.plus_image, self.music_plus_rect)

        segment_count = int(self.music_volume * 10)
        start_x = bg_x + 10

        for i in range(segment_count):
            segment_x = start_x + i * (self.segment_width + self.segment_spacing)
            segment_rect = pygame.Rect(
                segment_x, bar_y, self.segment_width, self.segment_height
            )
            surface.blit(self.segment_image, segment_rect)

        # Fullscreen
        label = self.font_medium.render("Fullscreen:", True, (0, 0, 0))
        label_rect = label.get_rect(
            midright=(self.checkbox_rect.left - 100, self.checkbox_rect.centery)
        )
        surface.blit(label, label_rect)

        checkbox_image = (
            self.checkbox_checked if self.fullscreen else self.checkbox_unchecked
        )
        surface.blit(checkbox_image, self.checkbox_rect.topleft)

        # Resolution
        label = self.font_medium.render("Resolution:", True, (0, 0, 0))
        label_rect = label.get_rect(
            midright=(self.combo_rect.left - 100, self.combo_rect.centery)
        )
        surface.blit(label, label_rect)

        pygame.draw.rect(surface, (200, 200, 200), self.combo_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.combo_rect, 2)

        res_text = f"{self.resolutions[self.selected_resolution_index][0]} x {self.resolutions[self.selected_resolution_index][1]}"
        text_surface = self.font_small.render(res_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.combo_rect.center)
        surface.blit(text_surface, text_rect)

        if self.combo_open:
            for i, res in enumerate(self.resolutions):
                option_rect = pygame.Rect(
                    self.combo_rect.left,
                    self.combo_rect.bottom + i * self.combo_height,
                    self.combo_width,
                    self.combo_height,
                )
                pygame.draw.rect(surface, (220, 220, 220), option_rect)
                pygame.draw.rect(surface, (0, 0, 0), option_rect, 1)

                option_text = f"{res[0]} x {res[1]}"
                option_surface = self.font_small.render(option_text, True, (0, 0, 0))
                option_text_rect = option_surface.get_rect(center=option_rect.center)
                surface.blit(option_surface, option_text_rect)

    # HANDLE CLICK
    def handle_click(self, pos):
        if self.back_rect.collidepoint(pos):
            if self.sound_on:
                self.click_sound.play()
            return "menu"

        if self.toggle_rect.collidepoint(pos):
            self.sound_on = not self.sound_on

            if not self.sound_on:
                self.sfx_volume = 0.0
                self.music_volume = 0.0
            else:
                self.sfx_volume = 0.5
                self.music_volume = 0.5

            pygame.mixer.music.set_volume(self.music_volume)

        if self.minus_rect.collidepoint(pos):
            if self.sound_on:
                self.click_sound.play()
            self.sfx_volume = max(0.0, round(self.sfx_volume - 0.1, 2))
            return None

        if self.plus_rect.collidepoint(pos):
            if self.sound_on:
                self.click_sound.play()
            self.sfx_volume = min(1.0, round(self.sfx_volume + 0.1, 2))

            if not self.sound_on and self.sfx_volume > 0.0:
                self.click_sound.play()
                self.sound_on = True

            return None

        if self.music_minus_rect.collidepoint(pos):
            if self.sound_on:
                self.click_sound.play()
            self.music_volume = max(0.0, round(self.music_volume - 0.1, 2))
            pygame.mixer.music.set_volume(self.music_volume)
            return None

        if self.music_plus_rect.collidepoint(pos):
            if self.sound_on:
                self.click_sound.play()
            self.music_volume = min(1.0, round(self.music_volume + 0.1, 2))

            if not self.sound_on and self.music_volume > 0.0:
                self.click_sound.play()
                self.sound_on = True

            pygame.mixer.music.set_volume(self.music_volume)
            return None

        if self.checkbox_rect.collidepoint(pos):
            if self.sound_on:
                self.click_sound.play()
            self.fullscreen = not self.fullscreen

            flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
            screen_width, screen_height = pygame.display.get_surface().get_size()
            pygame.display.set_mode((screen_width, screen_height), flags)

        if self.combo_rect.collidepoint(pos):
            self.combo_open = not self.combo_open
            return None

        if self.combo_open:
            for i, res in enumerate(self.resolutions):
                option_rect = pygame.Rect(
                    self.combo_rect.left,
                    self.combo_rect.bottom + i * self.combo_height,
                    self.combo_width,
                    self.combo_height,
                )
                if option_rect.collidepoint(pos):
                    if self.sound_on:
                        self.click_sound.play()
                    self.selected_resolution_index = i
                    self.combo_open = False

                    flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
                    pygame.display.set_mode(res, flags)
                    self.res.update_screen(pygame.display.get_surface())
                    return None

        return None
