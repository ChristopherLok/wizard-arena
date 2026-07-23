import pygame
from enemy import Blob, Goblin, Golem
import random


class WaveManager:
    def __init__(self, settings):
        self.settings = settings

        self.current_wave = 0
        self.enemies = []
        self.wave_active = False

    def start_next_wave(self):
        self.current_wave += 1
        self.enemies.clear()

        num_enemies = 3 + self.current_wave
        for _ in range(num_enemies):
            x = random.randint(100, 1900)
            y = random.randint(100, 1900)

            # Weighted spawn: Blob 60%, Goblin 30%, Golem 10%
            enemy_type = random.choices([Blob, Goblin, Golem], weights=[60, 30, 10])[0]

            self.enemies.append(enemy_type(x, y, self.settings))

        self.wave_active = True

    def update(self, player_pos):
        for enemy in self.enemies[:]:
            enemy.update(player_pos)
            if enemy.health <= 0:
                self.enemies.remove(enemy)

        # If all enemies are gone wave is over
        if not self.enemies:
            self.wave_active = False

    def draw(self, surface, camera_offset):
        for enemy in self.enemies:
            enemy.draw(surface, camera_offset)
