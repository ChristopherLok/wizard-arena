import pygame
import math


class Fireball:
    def __init__(
        self, x, y, target_x, target_y, settings, resources, speed=15, damage=20
    ):
        self.settings = settings

        self.damage = damage

        # Resources
        self.image = pygame.transform.scale(
            resources.load_image("assets/images/fireball.png").convert_alpha(), (40, 40)
        )
        self.fireball_sound = resources.load_sound("assets/sounds/fireball.mp3")

        self.pos = pygame.Vector2(x, y)

        direction = pygame.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            self.velocity = direction.normalize() * speed
        else:
            self.velocity = pygame.Vector2(0, 0)

        self.rect = self.image.get_rect(center=self.pos)

        if self.settings.sound_on:
            self.fireball_sound.set_volume(self.settings.sfx_volume)
            self.fireball_sound.play()

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, surface, camera_offset):
        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(self.image, screen_pos)

        # Draw hitbox for debugging
        # pygame.draw.rect(surface, (255, 0, 0), self.rect.move(-camera_offset[0], -camera_offset[1]), 2)

    def off_map(self, map_width, map_height):
        return (
            self.pos.x < 0
            or self.pos.x > map_width
            or self.pos.y < 0
            or self.pos.y > map_height
        )


class Snowflake:
    def __init__(
        self,
        x,
        y,
        target_x,
        target_y,
        settings,
        resources,
        speed=12,
        damage=5,
        freeze_time=2000,
    ):
        self.settings = settings

        self.damage = damage
        self.freeze_time = freeze_time

        # Resources
        self.image = pygame.transform.scale(
            resources.load_image("assets/images/snowflake.png").convert_alpha(),
            (40, 40),
        )
        self.snowflake_sound = resources.load_sound("assets/sounds/snowflake.mp3")

        self.pos = pygame.Vector2(x, y)

        direction = pygame.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            self.velocity = direction.normalize() * speed
        else:
            self.velocity = pygame.Vector2(0, 0)

        self.rect = self.image.get_rect(center=self.pos)

        if self.settings.sound_on:
            self.snowflake_sound.set_volume(self.settings.sfx_volume)
            self.snowflake_sound.play()

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, surface, camera_offset):
        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(self.image, screen_pos)

        # Draw hitbox for debugging
        # pygame.draw.rect(surface, (0, 0, 255), self.rect.move(-camera_offset[0], -camera_offset[1]), 2)

    def off_map(self, map_width, map_height):
        return (
            self.pos.x < 0
            or self.pos.x > map_width
            or self.pos.y < 0
            or self.pos.y > map_height
        )


class Lightning:
    def __init__(
        self,
        x,
        y,
        target_x,
        target_y,
        settings,
        resources,
        speed=10,
        damage=1,
        max_distance=300,
    ):
        self.settings = settings
        self.damage = damage
        self.max_distance = max_distance

        # Resources
        self.image = pygame.transform.scale(
            resources.load_image("assets/images/lightning.png").convert_alpha(),
            (80, 80),
        )
        self.lightning_sound = resources.load_sound("assets/sounds/lightning.mp3")

        self.pos = pygame.Vector2(x, y)
        self.start_pos = pygame.Vector2(x, y)

        direction = pygame.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            self.velocity = direction.normalize() * speed
        else:
            self.velocity = pygame.Vector2(0, 0)

        self.rect = self.image.get_rect(center=self.pos)

        if self.settings.sound_on:
            self.lightning_sound.set_volume(self.settings.sfx_volume)
            self.lightning_sound.play()

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, surface, camera_offset):
        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(self.image, screen_pos)

        # Draw hitbox for debugging
        # pygame.draw.rect(surface, (255, 255, 0), self.rect.move(-camera_offset[0], -camera_offset[1]), 2)

    def off_map(self, map_width, map_height):
        distance_travelled = (self.pos - self.start_pos).length()
        return (
            self.pos.x < 0
            or self.pos.x > map_width
            or self.pos.y < 0
            or self.pos.y > map_height
            or distance_travelled > self.max_distance
        )

    def check_collision(self, enemies):
        hit_enemies = []
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= self.damage
                hit_enemies.append(enemy)
        return hit_enemies
