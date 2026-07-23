import pygame
import math


class Player:
    def __init__(self, x, y, map_width, map_height, settings, max_health=5):
        self.settings = settings

        self.hit_sound = pygame.mixer.Sound("assets/sounds/wizard_hit.mp3")

        self.size = (200, 200)
        self.rect = pygame.Rect(x, y, *self.size)

        self.hitbox_offset = pygame.Vector2(50, 10)
        self.hitbox_size = (90, 185)

        self.map_width = map_width
        self.map_height = map_height

        self.speed = 5
        self.fireball_damage = 20

        self.snowflake_damage = 5
        self.freeze_time = 2000

        self.lightning_damage = 1
        self.lightning_max_distance = 300

        self.animation_count = 0
        self.moving_left = False
        self.moving_right = False
        self.moving_up_down = False

        # Health
        self.max_health = max_health
        self.health = max_health
        self.heart_image = pygame.transform.scale(
            pygame.image.load("assets/images/heart.png").convert_alpha(), (60, 50)
        )
        self.heart_empty_image = pygame.transform.scale(
            pygame.image.load("assets/images/heart_e.png").convert_alpha(), (60, 50)
        )

        # Shop changes
        self.coins = 0

        # Hit timer
        self.hit_timer = 0
        self.invincible_duration = 1000  # milliseconds
        self.hit_flash_duration = 200

        # Normal frames
        self.idle = pygame.transform.scale(
            pygame.image.load("assets/images/Wiz1.png").convert_alpha(), self.size
        )

        self.walk = [
            pygame.transform.scale(
                pygame.image.load("assets/images/Wiz2.png").convert_alpha(), self.size
            ),
            pygame.transform.scale(
                pygame.image.load("assets/images/Wiz3.png").convert_alpha(), self.size
            ),
        ]

        # Hit frames
        self.idle_hit = pygame.transform.scale(
            pygame.image.load("assets/images/Wiz1_d.png").convert_alpha(), self.size
        )

        self.walk_hit = [
            pygame.transform.scale(
                pygame.image.load("assets/images/Wiz2_d.png").convert_alpha(), self.size
            ),
            pygame.transform.scale(
                pygame.image.load("assets/images/Wiz3_d.png").convert_alpha(), self.size
            ),
        ]

        # Staff
        self.staff = pygame.transform.scale(
            pygame.image.load("assets/images/StaffG.png").convert_alpha(), (200, 250)
        )

        self.selected_ability = "fireball"  # Default ability

        # Active ability image
        self.ability_icons = {
            "fireball": pygame.transform.scale(
                pygame.image.load("assets/images/fireball.png").convert_alpha(),
                (60, 60),
            ),
            "snowflake": pygame.transform.scale(
                pygame.image.load("assets/images/snowflake.png").convert_alpha(),
                (60, 60),
            ),
            "lightning": pygame.transform.scale(
                pygame.image.load("assets/images/lightning.png").convert_alpha(),
                (60, 60),
            ),
        }

        # Ability list and index for cycling
        self.abilities = ["fireball", "snowflake", "lightning"]
        self.selected_index = 0
        self.selected_ability = self.abilities[self.selected_index]

    # Update hitbox size
    def update_hitbox(self):
        self.hitbox = pygame.Rect(
            self.rect.x + self.hitbox_offset.x,
            self.rect.y + self.hitbox_offset.y,
            self.hitbox_size[0],
            self.hitbox_size[1],
        )

    def handle_input(self, events):
        keys = pygame.key.get_pressed()

        self.moving_left = self.moving_right = self.moving_up_down = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.moving_left = True

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.moving_right = True

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.moving_up_down = True

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.moving_up_down = True

        # Ability cycling with scroll wheel
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.selected_index = (self.selected_index - 1) % len(
                        self.abilities
                    )
                elif event.button == 5:  # Scroll down
                    self.selected_index = (self.selected_index + 1) % len(
                        self.abilities
                    )

        # Update selected ability
        self.selected_ability = self.abilities[self.selected_index]

        self.update_hitbox()

        # Clamp player inside map
        self.rect.x = max(0, min(self.rect.x, self.map_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.map_height - self.rect.height))

    def draw_staff(self, surface, camera_offset, native_mouse_pos):
        native_mouse_x, native_mouse_y = native_mouse_pos

        world_mouse_x = native_mouse_x + camera_offset[0]
        world_mouse_y = native_mouse_y + camera_offset[1]

        dx = world_mouse_x - self.rect.centerx
        dy = world_mouse_y - self.rect.centery
        angle = -math.degrees(math.atan2(dy, dx))

        rotated = pygame.transform.rotate(self.staff, angle)

        pos = (
            self.rect.centerx - camera_offset[0],
            self.rect.centery - camera_offset[1],
        )
        rect = rotated.get_rect(center=pos)
        surface.blit(rotated, rect)

    def draw(self, surface, camera_offset, native_mouse_pos):
        self.animation_count = (self.animation_count + 1) % 16
        frame = self.animation_count // 10  # switch every 10 ticks

        if self.moving_left:
            img_index = frame
            normal_frame = self.walk[img_index]
            hit_frame = self.walk_hit[img_index]
            img = pygame.transform.flip(
                hit_frame if self.is_flash() else normal_frame, True, False
            )

        elif self.moving_right:
            img_index = frame
            normal_frame = self.walk[img_index]
            hit_frame = self.walk_hit[img_index]
            img = hit_frame if self.is_flash() else normal_frame

        elif self.moving_up_down:
            img_index = frame
            normal_frame = self.walk[img_index]
            hit_frame = self.walk_hit[img_index]
            img = hit_frame if self.is_flash() else normal_frame

        else:
            img = self.idle_hit if self.is_flash() else self.idle

        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(img, (screen_pos.x, screen_pos.y))

        self.draw_staff(
            surface, camera_offset, native_mouse_pos
        )  # Pass the unscaled mouse pos

        # Draw hitbox for debugging
        # pygame.draw.rect(surface, (255, 0, 0), self.hitbox.move(-camera_offset[0], -camera_offset[1]), 2)

    def draw_health(self, surface):
        for i in range(self.max_health):
            x = 10 + i * (self.heart_image.get_width() + 5)
            y = 10

            if i < self.health:
                surface.blit(self.heart_image, (x, y))
            else:
                surface.blit(self.heart_empty_image, (x, y))

    def draw_active_ability(self, surface):
        ability_icon = self.ability_icons.get(self.selected_ability)
        if not ability_icon:
            return

        icon_x = 20
        icon_y = 125

        surface.blit(ability_icon, (icon_x, icon_y))

    def take_damage(self, amount):
        if self.is_hit():
            return

        self.health -= amount
        self.hit_timer = pygame.time.get_ticks()

        # Play hit sound
        if self.settings.sound_on:
            self.hit_sound.set_volume(self.settings.sfx_volume)
            self.hit_sound.play()

        if self.health <= 0:
            print("Player dead!")

    def is_hit(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.hit_timer < self.invincible_duration

    def is_flash(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.hit_timer < self.hit_flash_duration
