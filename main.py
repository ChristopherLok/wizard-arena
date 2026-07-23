import pygame
from background import Background
from player import Player
from abilities import Fireball, Snowflake, Lightning
from enemy import Blob
from wave import WaveManager
from shop import Shop
from coin import Coin
from menu import MainMenu
from leaderboard import Leaderboard
from resolution import ResolutionManager
from settings import Settings
from pause import PauseScreen
from resource_manager import ResourceManager
from tutorial import Tutorial


pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
NATIVE_WIDTH, NATIVE_HEIGHT = 1920, 1080
MAP_WIDTH, MAP_HEIGHT = 2000, 2000
FPS = 60
font_path = "assets/fonts/PressStart2P-Regular.ttf"


class AppContext:
    def __init__(self, screen, res, settings, native_surface, resources):
        self.screen = screen
        self.res = res
        self.settings = settings
        self.native_surface = native_surface
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.running = True
        self.game = None
        self.initials = ""
        self.score_to_save = 0
        self.paused = False
        self.previous_state = None

        # Load title
        self.title = pygame.image.load("assets/images/Title.png").convert_alpha()

        # Fonts
        self.font_small = pygame.font.Font(font_path, 16)
        self.font_medium = pygame.font.Font(font_path, 24)
        self.font_large = pygame.font.Font(font_path, 32)

        # Backgrounds
        self.death_bg = pygame.transform.scale(
            pygame.image.load("assets/images/death.png").convert(),
            (NATIVE_WIDTH, NATIVE_HEIGHT),
        )

        # Screens
        self.menu = MainMenu(native_surface, res, settings)
        self.leaderboard = Leaderboard(settings)

        self.resources = resources


class Game:
    def __init__(self, native_surface, resolution_manager, settings):
        self.settings = settings

        font_path = "assets/fonts/PressStart2P-Regular.ttf"

        self.font_small = pygame.font.Font(font_path, 16)
        self.font_medium = pygame.font.Font(font_path, 24)
        self.font_large = pygame.font.Font(font_path, 32)

        self.surface = native_surface
        self.score = 0
        self.running = True

        self.background = Background(
            "assets/images/background1.png", MAP_WIDTH, MAP_HEIGHT
        )

        self.player = Player(
            MAP_WIDTH // 2, MAP_HEIGHT // 2, MAP_WIDTH, MAP_HEIGHT, settings
        )

        self.camera_offset = [0, 0]

        self.wave_manager = WaveManager(settings)
        self.wave_manager.start_next_wave()

        # Shop
        self.shop = Shop(res_manager=res, settings=settings)
        self.shop_shown = False

        # List of active abilities
        self.abilities = []

        # List of dropped coins
        self.dropped_coins = []

        self.coin_icon = pygame.transform.scale(
            pygame.image.load("assets/images/coin.png"), (50, 50)
        )

        pygame.mixer.music.set_volume(
            self.settings.music_volume if self.settings.sound_on else 0.0
        )

    def handle_events(self, event):
        if (
            self.shop.opened
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            shop_closed = self.shop.handle_click(event.pos, self.player)

            if shop_closed:
                self.shop_shown = False
                self.wave_manager.start_next_wave()
            return

        # Left mouse click cast ability
        if (
            not self.shop.opened
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            mouse_x, mouse_y = pygame.mouse.get_pos()

            logical_mouse_x, logical_mouse_y = res.unscale_mouse((mouse_x, mouse_y))

            cam_x = self.camera_offset[0]
            cam_y = self.camera_offset[1]

            world_x = logical_mouse_x + cam_x
            world_y = logical_mouse_y + cam_y

            if self.player.selected_ability == "fireball":
                self.abilities.append(
                    Fireball(
                        self.player.hitbox.centerx,
                        self.player.hitbox.centery,
                        world_x,
                        world_y,
                        settings,
                        context.resources,
                        damage=self.player.fireball_damage,
                    )
                )

            elif self.player.selected_ability == "snowflake":
                self.abilities.append(
                    Snowflake(
                        self.player.hitbox.centerx,
                        self.player.hitbox.centery,
                        world_x,
                        world_y,
                        settings,
                        context.resources,
                        damage=self.player.snowflake_damage,
                        freeze_time=self.player.freeze_time,
                    )
                )

            elif self.player.selected_ability == "lightning":
                self.abilities.append(
                    Lightning(
                        self.player.hitbox.centerx,
                        self.player.hitbox.centery,
                        world_x,
                        world_y,
                        settings,
                        context.resources,
                        damage=self.player.lightning_damage,
                        max_distance=self.player.lightning_max_distance,
                    )
                )

    def update(self, events):
        if not self.shop.opened:
            self.player.handle_input(events)

        # Camera follows player
        self.camera_offset[0] = self.player.hitbox.centerx - NATIVE_WIDTH // 2
        self.camera_offset[1] = self.player.hitbox.centery - NATIVE_HEIGHT // 2

        # Clamp to map
        self.camera_offset[0] = max(
            0, min(self.camera_offset[0], MAP_WIDTH - NATIVE_WIDTH)
        )
        self.camera_offset[1] = max(
            0, min(self.camera_offset[1], MAP_HEIGHT - NATIVE_HEIGHT)
        )

        # Update abilities
        for ability in self.abilities[:]:
            ability.update()
            if ability.off_map(MAP_WIDTH, MAP_HEIGHT):
                self.abilities.remove(ability)

        # Update enemies
        for enemy in self.wave_manager.enemies[:]:
            enemy.update(pygame.Vector2(self.player.hitbox.center))

            enemy.check_collision(self.abilities)

            if not enemy.alive:
                self.score += getattr(enemy, "points", 0)

                coin_value = getattr(enemy, "coin_value", 1)
                self.dropped_coins.append(
                    Coin(enemy.rect.centerx, enemy.rect.centery, coin_value, settings)
                )

                self.wave_manager.enemies.remove(enemy)
                continue

            if enemy.hitbox.colliderect(self.player.hitbox):
                self.player.take_damage(enemy.damage)

            if self.player.health <= 0:
                self.running = False  # Stop the game loop

        # Coin pickup
        for coin in self.dropped_coins[:]:
            if coin.check_pickup(self.player):
                self.dropped_coins.remove(coin)

        # Shop
        if (
            len(self.wave_manager.enemies) == 0
            and not self.shop.opened
            and not self.shop_shown
        ):
            self.shop.open()
            self.shop_shown = True

    def draw_score(self, surface):
        color = (255, 215, 0)  # Gold colour
        text = self.font_medium.render(f"Score: {self.score}", True, color)

        NATIVE_WIDTH = surface.get_width()

        # Top right corner
        surface.blit(text, (NATIVE_WIDTH - text.get_width() - 10, 10))

    def draw_coin_count(self, surface):
        # Position below health bar
        x = 20
        y = 65

        # Draw coin icon
        surface.blit(self.coin_icon, (x, y))

        color = (255, 223, 0)  # gold
        text = self.font_large.render(f"x{self.player.coins}", True, color)

        surface.blit(text, (75, y + 12))  # offset to the right of the icon

        self.player.draw_active_ability(surface)

    def draw(self, res_manager):
        self.background.draw(self.surface, self.camera_offset)

        scaled_mouse_pos = pygame.mouse.get_pos()
        native_mouse_pos = res_manager.unscale_mouse(scaled_mouse_pos)

        self.player.draw(self.surface, self.camera_offset, native_mouse_pos)

        for ability in self.abilities:
            ability.draw(self.surface, self.camera_offset)

        for enemy in self.wave_manager.enemies:
            enemy.draw(self.surface, self.camera_offset)

        self.draw_score(self.surface)

        for coin in self.dropped_coins:
            coin.draw(self.surface, self.camera_offset)

        self.player.draw_health(self.surface)

        if self.shop.opened:
            self.shop.draw(self.surface)

        self.draw_coin_count(self.surface)


if __name__ == "__main__":
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 1280, 720
    NATIVE_WIDTH, NATIVE_HEIGHT = 1920, 1080
    FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"
    FPS = 60

    # Resolution setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    native_surface = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT))
    res = ResolutionManager(screen, base_width=NATIVE_WIDTH, base_height=NATIVE_HEIGHT)

    # Initialize mixer and load music BEFORE creating Settings
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/background_song.mp3")

    # Create settings
    settings = Settings(res_manager=res)

    # Resource manager
    resources = ResourceManager()

    # Centralized context
    context = AppContext(screen, res, settings, native_surface, resources)
    context.pause_screen = PauseScreen(context.res, settings)

    # Apply correct volume BEFORE playing
    pygame.mixer.music.set_volume(
        context.settings.music_volume if context.settings.sound_on else 0.0
    )
    pygame.mixer.music.play(-1)  # Start looping

    while context.running:
        context.clock.tick(FPS)
        events = pygame.event.get()

        current_fps = context.clock.get_fps()
        print(f"Current FPS: {current_fps:.1f}")

        for event in events:
            if event.type == pygame.QUIT:
                context.running = False

            elif event.type == pygame.VIDEORESIZE:
                current_w, current_h = event.size
                flags = (
                    pygame.FULLSCREEN
                    if context.settings.fullscreen
                    else pygame.RESIZABLE
                )
                context.screen = pygame.display.set_mode((current_w, current_h), flags)
                context.res.scale_x = current_w / NATIVE_WIDTH
                context.res.scale_y = current_h / NATIVE_HEIGHT

            elif (
                context.state == "menu"
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                action = context.menu.handle_click(event.pos)
                if action == "start":
                    context.game = Game(
                        context.native_surface, context.res, context.settings
                    )
                    context.state = "game"
                elif action == "score":
                    context.state = "score"
                elif action == "settings":
                    context.state = "settings"
                elif action == "tutorial":
                    context.tutorial = Tutorial(context.settings)
                    context.state = "tutorial"

            elif (
                context.state == "score"
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                logical_mouse_pos = context.res.unscale_mouse(event.pos)
                if context.leaderboard.handle_click(logical_mouse_pos):
                    context.state = "menu"

            elif (
                context.state == "tutorial"
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                logical_pos = context.res.unscale_mouse(event.pos)
                if context.tutorial.handle_click(logical_pos):
                    context.state = "menu"

            elif (
                context.state == "settings"
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                logical_mouse_pos = context.res.unscale_mouse(event.pos)
                result = context.settings.handle_click(logical_mouse_pos)
                if result == "menu":
                    if context.previous_state == "pause":
                        context.state = "game"
                        context.paused = True
                    else:
                        context.state = "menu"
                    context.previous_state = None  # Clear after use

            elif context.state == "game" and context.game:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    context.paused = not context.paused

                elif (
                    context.paused
                    and event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    result = context.pause_screen.handle_click(event.pos)
                    if result == "resume":
                        context.paused = False
                    elif result == "settings":
                        context.previous_state = "pause"
                        context.paused = False
                        context.state = "settings"
                    elif result == "menu":
                        context.paused = False
                        context.game = None
                        context.state = "menu"

                elif not context.paused:
                    context.game.handle_events(event)

            elif context.state == "initials_entry":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(context.initials) == 3:
                        context.leaderboard.add_score(
                            context.initials, context.score_to_save
                        )
                        context.state = "menu"
                        context.initials = ""
                    elif event.key == pygame.K_BACKSPACE:
                        context.initials = context.initials[:-1]
                    elif len(context.initials) < 3 and event.unicode.isalpha():
                        context.initials += event.unicode.upper()

        # Drawing
        context.native_surface.fill((0, 0, 0))

        if context.state == "menu":
            context.menu.draw()

            title_width = 800
            title_height = 600

            scaled_title = pygame.transform.scale(
                context.title, (title_width, title_height)
            )
            title_rect = scaled_title.get_rect(center=(NATIVE_WIDTH // 2, 150))
            context.native_surface.blit(scaled_title, title_rect)

        elif context.state == "score":
            context.leaderboard.draw(context.native_surface)

        elif context.state == "tutorial":
            context.tutorial.draw(context.native_surface)

        elif context.state == "settings":
            context.settings.draw(context.native_surface)

        elif context.state == "game" and context.game:
            if context.paused:
                context.pause_screen.draw(context.native_surface)
            else:
                context.game.update(events)
                context.game.draw(context.res)

                if not context.game.running or context.game.player.health <= 0:
                    context.score_to_save = context.game.score
                    context.game = None
                    context.initials = ""
                    context.state = "initials_entry"

        elif context.state == "initials_entry":
            context.native_surface.blit(context.death_bg, (0, 0))
            text = context.font_large.render(
                "Enter Initials (3 letters): " + context.initials, True, (255, 255, 255)
            )
            x_pos = context.native_surface.get_width() // 2 - text.get_width() // 2
            y_pos = context.native_surface.get_height() // 2
            context.native_surface.blit(text, (x_pos, y_pos))

        # Final blit
        current_w, current_h = context.screen.get_size()
        scaled_surface = pygame.transform.scale(
            context.native_surface, (current_w, current_h)
        )
        context.res.scale_x = current_w / NATIVE_WIDTH
        context.res.scale_y = current_h / NATIVE_HEIGHT

        context.screen.fill((0, 0, 0))
        context.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()
