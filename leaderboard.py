import pygame
import json
import os

# Base Resolution
BASE_WIDTH = 1920
BASE_HEIGHT = 1080


class Leaderboard:
    def __init__(self, settings, filename="leaderboard.json"):
        self.settings = settings

        # Load click sound
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

        self.filename = filename
        self.scores = self.load_scores()

        # Load custom Press Start 2P font
        font_path = "assets/fonts/PressStart2P-Regular.ttf"

        self.font_small = pygame.font.Font(font_path, 16)
        self.font_medium = pygame.font.Font(font_path, 24)
        self.font_large = pygame.font.Font(font_path, 32)

        # Load images
        self.bg_image = pygame.image.load("assets/images/leaderboard_b.png").convert()
        self.leaderboard_image_orig = pygame.image.load(
            "assets/images/leaderboard.png"
        ).convert_alpha()
        self.back_image_orig = pygame.image.load(
            "assets/images/back.png"
        ).convert_alpha()

        # Base Resolution
        self.ideal_board_size = (1200, 860)
        self.ideal_back_size = (180, 180)

    def load_scores(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error loading leaderboard.json. File corrupted or empty.")
                return []
        return []

    def save_scores(self):
        with open(self.filename, "w") as f:
            json.dump(self.scores, f, indent=4)

    def add_score(self, initials, score):
        # Append and sort
        self.scores.append({"initials": initials, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[
            :10
        ]  # keep top 10
        self.save_scores()

    def get_top_scores(self):
        return self.scores

    def draw(self, surface):
        current_width, current_height = surface.get_size()

        # Scale and position the Background
        surface.blit(
            pygame.transform.scale(self.bg_image, (current_width, current_height)),
            (0, 0),
        )

        # Scale the Leaderboard Board image proportionally
        scale_x = current_width / BASE_WIDTH
        scale_y = current_height / BASE_HEIGHT

        scaled_board_size = (
            int(self.ideal_board_size[0] * scale_x),
            int(self.ideal_board_size[1] * scale_y),
        )
        scaled_board_image = pygame.transform.scale(
            self.leaderboard_image_orig, scaled_board_size
        )

        board_top_y = int(current_height * (-10 / BASE_HEIGHT))
        self.leaderboard_rect = scaled_board_image.get_rect(
            centerx=current_width // 2, top=board_top_y
        )
        surface.blit(scaled_board_image, self.leaderboard_rect.topleft)

        # Scale and Position the Back Button
        scaled_back_size = (
            int(self.ideal_back_size[0] * scale_x),
            int(self.ideal_back_size[1] * scale_y),
        )
        scaled_back_image = pygame.transform.scale(
            self.back_image_orig, scaled_back_size
        )

        back_top_x = int(current_width * (15 / BASE_WIDTH))
        back_top_y = int(current_height * (-10 / BASE_HEIGHT))
        self.back_rect = scaled_back_image.get_rect(topleft=(back_top_x, back_top_y))
        surface.blit(scaled_back_image, self.back_rect)

        # Calculate relative Y positions for text
        title_y = int(current_height * (155 / BASE_HEIGHT))
        start_y = int(current_height * (200 / BASE_HEIGHT))
        line_spacing = int(current_height * (60 / BASE_HEIGHT))

        # Draw title
        title = self.font_medium.render("Leaderboard - Top 10", True, (255, 223, 0))
        title_rect = title.get_rect(center=(current_width // 2, title_y))
        surface.blit(title, title_rect)

        # Draw scores
        for i, entry in enumerate(self.scores[:10], start=1):
            line = f"{i}. {entry['initials']} - {entry['score']}"
            text = self.font_medium.render(line, True, (0, 0, 0))

            text_y = start_y + i * line_spacing
            text_rect = text.get_rect(center=(current_width // 2, text_y))
            surface.blit(text, text_rect)

        return self.back_rect

    def handle_click(self, pos):
        if self.back_rect.collidepoint(pos):
            if self.settings.sound_on:
                self.click_sound.play()
            return True
        return False
