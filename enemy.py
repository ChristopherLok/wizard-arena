import pygame
import math
from abilities import Fireball, Snowflake, Lightning


class Blob:
    def __init__(
        self, x, y, settings, size=(100, 100), speed=2, health=50, damage=1
    ):  # Size, speed, health and damage of blob
        self.settings = settings

        self.points = 10  # Points
        self.coin_value = 1  # Coins

        self.blob_hit_sound = pygame.mixer.Sound("assets/sounds/blob_hit.mp3")
        self.alive = True
        self.size = size
        self.speed = speed
        self.health = health
        self.damage = damage
        self.pos = pygame.Vector2(x, y)

        # Load animation frames
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/blob{i}.png").convert_alpha(),
                self.size,
            )
            for i in range(1, 5)
        ]

        # Load hit frames
        self.hit_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/blob{i}_d.png").convert_alpha(),
                self.size,
            )
            for i in range(1, 5)
        ]

        self.frame_index = 0
        self.animation_counter = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(center=self.pos)

        # Hitbox size
        self.hitbox = self.rect.inflate(-25, -40)

        self.hit_timer = 0
        self.hit_duration = 150

        self.frozen = False
        self.freeze_timer = 0
        self.freeze_duration = 0
        self.frozen_image = pygame.transform.scale(
            pygame.image.load("assets/images/blob_f.png").convert_alpha(), self.size
        )

    def update(self, player_pos):
        current_time = pygame.time.get_ticks()

        # Skip movement if frozen
        if self.frozen:
            if current_time - self.freeze_timer > self.freeze_duration:
                self.frozen = False
            self.image = self.frozen_image
            return

        # Normal movement
        direction = player_pos - self.pos
        if direction.length() != 0:
            self.pos += direction.normalize() * self.speed
            self.rect.center = self.pos
            self.hitbox.center = self.pos

        # Animate
        self.animation_counter = (self.animation_counter + 1) % 15
        if self.animation_counter == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        # Hit flicker
        if current_time - self.hit_timer < self.hit_duration:
            self.image = self.hit_frames[self.frame_index]
        else:
            self.image = self.frames[self.frame_index]

    def draw(self, surface, camera_offset):
        # Draw current frame
        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(self.image, screen_pos)

        # Draw hitbox for debugging
        # pygame.draw.rect(surface, (0, 255, 0), self.hitbox.move(-camera_offset[0], -camera_offset[1]), 2)

    def take_damage(self, amount):
        self.health -= amount
        self.hit_timer = pygame.time.get_ticks()
        if self.health <= 0:
            self.alive = False

    def check_collision(self, abilities):
        for ability in abilities[:]:
            if self.hitbox.colliderect(ability.rect):
                if isinstance(ability, Snowflake):
                    self.take_damage(ability.damage)
                    self.freeze_timer = pygame.time.get_ticks()
                    self.freeze_duration = ability.freeze_time
                    self.frozen = True
                    abilities.remove(ability)  # Snowflake removed after hitting
                elif isinstance(ability, Lightning):
                    self.take_damage(ability.damage)  # Lightning passes through enemy
                else:  # Fireball
                    self.take_damage(ability.damage)
                    abilities.remove(ability)  # Fireball removed after hitting

                # Play hit sound
                if self.settings.sound_on:
                    self.blob_hit_sound.set_volume(self.settings.sfx_volume)
                    self.blob_hit_sound.play()


class Goblin:
    def __init__(self, x, y, settings, size=(80, 80), speed=5, health=20, damage=2):
        self.settings = settings

        self.points = 20
        self.coin_value = 1

        self.goblin_hit_sound = pygame.mixer.Sound("assets/sounds/goblin_hit.mp3")
        self.alive = True
        self.size = size
        self.speed = speed
        self.health = health
        self.damage = damage
        self.pos = pygame.Vector2(x, y)

        # Load animation frames
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/gob{i}.png").convert_alpha(),
                self.size,
            )
            for i in range(1, 3)
        ]

        # Load hit frames
        self.hit_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/gob{i}_d.png").convert_alpha(),
                self.size,
            )
            for i in range(1, 3)
        ]

        self.frame_index = 0
        self.animation_counter = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.rect.inflate(-20, -30)

        self.hit_timer = 0
        self.hit_duration = 150

        self.frozen = False
        self.freeze_timer = 0
        self.freeze_duration = 0
        self.frozen_image = pygame.transform.scale(
            pygame.image.load("assets/images/gob_f.png").convert_alpha(), self.size
        )

    def update(self, player_pos):
        current_time = pygame.time.get_ticks()

        # Skip movement if frozen
        if self.frozen:
            if current_time - self.freeze_timer > self.freeze_duration:
                self.frozen = False
            self.image = self.frozen_image
            return

        direction = player_pos - self.pos
        if direction.length() != 0:
            self.pos += direction.normalize() * self.speed
            self.rect.center = self.pos
            self.hitbox.center = self.pos

        self.animation_counter = (self.animation_counter + 1) % 10
        if self.animation_counter == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        current_time = pygame.time.get_ticks()
        if current_time - self.hit_timer < self.hit_duration:
            self.image = self.hit_frames[self.frame_index]
        else:
            self.image = self.frames[self.frame_index]

    def draw(self, surface, camera_offset):
        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(self.image, screen_pos)

        # pygame.draw.rect(surface, (255, 0, 0), self.hitbox.move(-camera_offset[0], -camera_offset[1]), 2)

    def take_damage(self, amount):
        self.health -= amount
        self.hit_timer = pygame.time.get_ticks()
        if self.health <= 0:
            self.alive = False

    def check_collision(self, abilities):
        for ability in abilities[:]:
            if self.hitbox.colliderect(ability.rect):
                if isinstance(ability, Snowflake):
                    self.take_damage(ability.damage)
                    self.freeze_timer = pygame.time.get_ticks()
                    self.freeze_duration = ability.freeze_time
                    self.frozen = True
                    abilities.remove(ability)

                elif isinstance(ability, Lightning):
                    self.take_damage(ability.damage)

                else:
                    self.take_damage(ability.damage)
                    abilities.remove(ability)

                if self.settings.sound_on:
                    self.goblin_hit_sound.set_volume(self.settings.sfx_volume)
                    self.goblin_hit_sound.play()


class Golem:
    def __init__(
        self, x, y, settings, size=(250, 250), speed=1.5, health=100, damage=4
    ):
        self.settings = settings

        self.points = 50
        self.coin_value = 5

        self.golem_hit_sound = pygame.mixer.Sound("assets/sounds/golem_hit.mp3")
        self.alive = True
        self.size = size
        self.speed = speed
        self.health = health
        self.damage = damage
        self.pos = pygame.Vector2(x, y)

        # Load animation frames
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/golem{i}.png").convert_alpha(),
                self.size,
            )
            for i in range(1, 4)
        ]

        # Load hit frames
        self.hit_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/golem{i}_d.png").convert_alpha(),
                self.size,
            )
            for i in range(1, 4)
        ]

        self.frame_index = 0
        self.animation_counter = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.rect.inflate(-30, -50)

        self.hit_timer = 0
        self.hit_duration = 150

        self.frozen = False
        self.freeze_timer = 0
        self.freeze_duration = 0
        self.frozen_image = pygame.transform.scale(
            pygame.image.load("assets/images/Golem_f.png").convert_alpha(), self.size
        )

    def update(self, player_pos):
        current_time = pygame.time.get_ticks()

        # Skip movement if frozen
        if self.frozen:
            if current_time - self.freeze_timer > self.freeze_duration:
                self.frozen = False
            self.image = self.frozen_image
            return

        direction = player_pos - self.pos
        if direction.length() != 0:
            self.pos += direction.normalize() * self.speed
            self.rect.center = self.pos
            self.hitbox.center = self.pos

        self.animation_counter = (self.animation_counter + 1) % 20  # slower animation
        if self.animation_counter == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        current_time = pygame.time.get_ticks()
        if current_time - self.hit_timer < self.hit_duration:
            self.image = self.hit_frames[self.frame_index]
        else:
            self.image = self.frames[self.frame_index]

    def draw(self, surface, camera_offset):
        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(self.image, screen_pos)

        # pygame.draw.rect(surface, (0, 0, 255), self.hitbox.move(-camera_offset[0], -camera_offset[1]), 2)

    def take_damage(self, amount):
        self.health -= amount
        self.hit_timer = pygame.time.get_ticks()
        if self.health <= 0:
            self.alive = False

    def check_collision(self, abilities):
        for ability in abilities[:]:
            if self.hitbox.colliderect(ability.rect):
                if isinstance(ability, Snowflake):
                    self.take_damage(ability.damage)
                    self.freeze_timer = pygame.time.get_ticks()
                    self.freeze_duration = ability.freeze_time
                    self.frozen = True
                    abilities.remove(ability)

                elif isinstance(ability, Lightning):
                    self.take_damage(ability.damage)

                else:
                    self.take_damage(ability.damage)
                    abilities.remove(ability)

                if self.settings.sound_on:
                    self.golem_hit_sound.set_volume(self.settings.sfx_volume)
                    self.golem_hit_sound.play()
