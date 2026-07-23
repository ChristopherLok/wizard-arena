import pygame


class Coin:
    def __init__(self, x, y, value, settings):
        self.settings = settings

        # Load coin sound
        self.coin_sound = pygame.mixer.Sound("assets/sounds/coin_pickup.mp3")

        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/coin.png"), (40, 40)
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.value = value

    def draw(self, surface, camera_offset):
        screen_pos = self.rect.move(-camera_offset[0], -camera_offset[1])
        surface.blit(self.image, screen_pos)

    def check_pickup(self, player):
        if self.rect.colliderect(player.hitbox):
            if self.settings.sound_on:
                self.coin_sound.set_volume(self.settings.sfx_volume)
                self.coin_sound.play()
            player.coins += self.value
            return True
        return False
