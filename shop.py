import pygame
import random
import math

# Define native resolution
NATIVE_WIDTH = 1920
NATIVE_HEIGHT = 1080


class Shop:
    def __init__(self, res_manager, settings):
        self.settings = settings

        # Load sounds
        self.buy_sound = pygame.mixer.Sound("assets/sounds/buy.mp3")
        self.error_sound = pygame.mixer.Sound("assets/sounds/error.mp3")

        font_path = "assets/fonts/PressStart2P-Regular.ttf"

        self.font_small = pygame.font.Font(font_path, 16)
        self.font_medium = pygame.font.Font(font_path, 24)
        self.font_large = pygame.font.Font(font_path, 32)
        self.font_heading = pygame.font.Font(font_path, 64)

        self.res = res_manager

        self.BG_NATIVE_WIDTH = 1600
        self.BG_NATIVE_HEIGHT = 1300

        # Load and scale background image to native size
        self.background_orig = pygame.image.load(
            "assets/images/paper.png"
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background_orig, (self.BG_NATIVE_WIDTH, self.BG_NATIVE_HEIGHT)
        )

        # Calculate native center and background rect position
        self.NATIVE_CENTER_X = NATIVE_WIDTH // 2
        self.NATIVE_CENTER_Y = NATIVE_HEIGHT // 2
        self.bg_rect_native = self.background.get_rect(
            center=(self.NATIVE_CENTER_X, self.NATIVE_CENTER_Y)
        )

        # Item and button sizes
        self.ITEM_IMAGE_SIZE = (200, 200)
        self.EXIT_BUTTON_SIZE = (300, 150)

        # Load and scale all necessary images
        self.exit_image = pygame.transform.scale(
            pygame.image.load("assets/images/exit.png"), self.EXIT_BUTTON_SIZE
        )
        self.potion_image = pygame.transform.scale(
            pygame.image.load("assets/images/potion.png"), self.ITEM_IMAGE_SIZE
        )
        self.shield_image = pygame.transform.scale(
            pygame.image.load("assets/images/shield.png"), self.ITEM_IMAGE_SIZE
        )
        self.boots_image = pygame.transform.scale(
            pygame.image.load("assets/images/boots.png"), self.ITEM_IMAGE_SIZE
        )
        self.fire_potion_image = pygame.transform.scale(
            pygame.image.load("assets/images/fire_potion.png"), self.ITEM_IMAGE_SIZE
        )
        self.freeze_image = pygame.transform.scale(
            pygame.image.load("assets/images/freeze_potion.png"), self.ITEM_IMAGE_SIZE
        )
        self.lightning_potion_image = pygame.transform.scale(
            pygame.image.load("assets/images/lightning_potion.png"),
            self.ITEM_IMAGE_SIZE,
        )

        # Exit button rect
        exit_x_center = self.bg_rect_native.centerx
        exit_y_center = self.bg_rect_native.bottom - 400
        self.exit_rect_native = self.exit_image.get_rect(
            center=(exit_x_center, exit_y_center)
        )

        # Font and feedback state
        self.font = self.font_medium
        self.feedback_message = ""
        self.feedback_timer = 0
        self.feedback_duration = 1500
        self.opened = False

        # List of all available items
        self.all_items = [
            {"name": "Heal +1", "action": "heal", "cost": 3},
            {"name": "Max Health +1", "action": "max_health", "cost": 5},
            {"name": "Boots of Speed", "action": "speed", "cost": 6},
            {"name": "Fire Potion", "action": "fire_damage", "cost": 10},
            {"name": "Freeze Potion", "action": "freeze_upgrade", "cost": 8},
            {"name": "Lightning Potion", "action": "lightning_upgrade", "cost": 10},
        ]
        self.active_items = []

    class TextWrapper:
        def __init__(self, font, max_width):
            self.font = font
            self.max_width = max_width

        def wrap(self, text):
            words = text.split(" ")
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] <= self.max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip())
            return lines

    def open(self):
        self.opened = True

        self.active_items = random.sample(self.all_items, 3)

        item_y = self.bg_rect_native.top + 400
        ITEM_WIDTH = self.ITEM_IMAGE_SIZE[0]

        total_item_width = 3 * ITEM_WIDTH
        spacing = (self.BG_NATIVE_WIDTH - total_item_width) // 4
        start_x = self.bg_rect_native.left + spacing

        for i, item in enumerate(self.active_items):
            item_rect_x = start_x + i * (ITEM_WIDTH + spacing)

            item["rect"] = pygame.Rect(item_rect_x, item_y, ITEM_WIDTH, ITEM_WIDTH)

    def close(self):
        self.opened = False
        self.feedback_message = ""

    def draw(self, native_surface):
        if not self.opened:
            return

        native_surface.blit(self.background, self.bg_rect_native)
        native_surface.blit(self.exit_image, self.exit_rect_native)

        heading_text = self.font_heading.render("Item Shop", True, (0, 0, 0))

        heading_x = self.bg_rect_native.centerx
        heading_y = self.bg_rect_native.top + 350  # adjust as needed

        heading_rect = heading_text.get_rect(center=(heading_x, heading_y))
        native_surface.blit(heading_text, heading_rect)

        # pygame.draw.rect(native_surface, (255, 0, 0), self.exit_rect_native, 3)

        for item in self.active_items:
            item_rect = item["rect"]

            image_to_draw = self.potion_image
            if item["action"] == "max_health":
                image_to_draw = self.shield_image
            elif item["action"] == "speed":
                image_to_draw = self.boots_image
            elif item["action"] == "fire_damage":
                image_to_draw = self.fire_potion_image
            elif item["action"] == "freeze_upgrade":
                image_to_draw = self.freeze_image
            elif item["action"] == "lightning_upgrade":
                image_to_draw = self.lightning_potion_image

            native_surface.blit(image_to_draw, item_rect.topleft)

            # pygame.draw.rect(native_surface, (255, 0, 0), item_rect, 3)

            max_text_width = 240
            wrapper = self.TextWrapper(self.font_medium, max_text_width)
            wrapped_lines = wrapper.wrap(item["name"])

            # Calculate starting Y position for first line
            line_height = self.font_medium.get_linesize()
            start_y = item_rect.bottom + 10

            extra_spacing = 10

            for i, line in enumerate(wrapped_lines):
                line_surface = self.font_medium.render(line, True, (0, 0, 0))
                line_rect = line_surface.get_rect(
                    center=(
                        item_rect.centerx,
                        start_y + i * (line_height + extra_spacing),
                    )
                )
                native_surface.blit(line_surface, line_rect)

            cost_str = f"{item['cost']} coins"
            outline_color = (0, 0, 0)
            text_color = (255, 223, 0)

            cost_text = self.font_large.render(cost_str, True, text_color)
            cost_rect = cost_text.get_rect(
                center=(item_rect.centerx, item_rect.bottom + 100)
            )

            for dx, dy in [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
                (-2, 0),
                (2, 0),
                (0, -2),
                (0, 2),
            ]:
                outline = self.font_large.render(cost_str, True, outline_color)
                native_surface.blit(outline, (cost_rect.x + dx, cost_rect.y + dy))

            native_surface.blit(cost_text, cost_rect)

        if self.feedback_message:
            current_time = pygame.time.get_ticks()
            if current_time - self.feedback_timer < self.feedback_duration:
                feedback_font = self.font_large
                text = feedback_font.render(self.feedback_message, True, (255, 0, 0))
                text_rect = text.get_rect(
                    center=(self.NATIVE_CENTER_X, self.bg_rect_native.centery + 135)
                )
                native_surface.blit(text, text_rect)
            else:
                self.feedback_message = ""

    def handle_click(self, pos, player):
        if not self.opened or not self.res:
            return False

        logical_pos = self.res.unscale_mouse(pos)

        if self.exit_rect_native.collidepoint(logical_pos):
            self.close()
            return True

        for item in self.active_items:
            if item["rect"].collidepoint(logical_pos):
                cost = item["cost"]
                action = item["action"]

                if action == "heal":
                    if player.health < player.max_health:
                        if player.coins >= cost:
                            player.coins -= cost
                            player.health = min(player.health + 1, player.max_health)
                            self.feedback_message = "Health restored!"

                            if self.settings.sound_on:
                                self.buy_sound.set_volume(self.settings.sfx_volume)
                                self.buy_sound.play()
                        else:
                            self.feedback_message = "Not enough coins!"

                            if self.settings.sound_on:
                                self.error_sound.set_volume(self.settings.sfx_volume)
                                self.error_sound.play()
                    else:
                        self.feedback_message = "You're already at full health!"

                        if self.settings.sound_on:
                            self.error_sound.set_volume(self.settings.sfx_volume)
                            self.error_sound.play()

                elif player.coins >= cost:
                    player.coins -= cost

                    if action == "max_health":
                        player.max_health += 1
                        self.feedback_message = "Max Health Increased!"
                    elif action == "speed":
                        player.speed += 1
                        self.feedback_message = "Speed Increased!"
                    elif action == "fire_damage":
                        player.fireball_damage += 5
                        self.feedback_message = "Fireball Damage Increased!"
                    elif action == "freeze_upgrade":
                        player.snowflake_damage += 2
                        player.freeze_time += 300
                        self.feedback_message = "Freeze power increased!"
                    elif action == "lightning_upgrade":
                        player.lightning_damage += 1
                        player.lightning_max_distance += 100
                        self.feedback_message = "Lightning Power Increased!"

                    if self.settings.sound_on:
                        self.buy_sound.set_volume(self.settings.sfx_volume)
                        self.buy_sound.play()

                else:
                    self.feedback_message = "Not enough coins!"

                    if self.settings.sound_on:
                        self.error_sound.set_volume(self.settings.sfx_volume)
                        self.error_sound.play()

                self.feedback_timer = pygame.time.get_ticks()
                print(f"[SHOP FEEDBACK] {self.feedback_message}")

                break

        return False
