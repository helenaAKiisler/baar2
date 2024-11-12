import pygame
import sys
import ui
from settings import WIDTH, HEIGHT, LIGHT_GREEN  # IMPORTIGE WIDTH, HEIGHT ja LIGHT_GREEN
from game_level import GameLevel
from scene import Scene

class MainMenu(Scene):
    BACKGROUND_COLOR = pygame.Color(LIGHT_GREEN)

    def __init__(self, scene_switcher, game_title, screen=None):
        super().__init__(scene_switcher)
        self.game_title = game_title
        self.screen = screen
        # Start nupp
        self.start_button = ui.Button("Start", on_pressed=lambda: self.scene_switcher("GameLevel", screen))
        # Quit nupp
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_game)  # Quit nupp, mis sulgeb mängu

    def handle_events(self, event):
        """Siin töötleme sündmusi (ka nuppude vajutamist)."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Kui vajutatakse P nuppu
                self.toggle_pause()  # Lülitame pausi sisse või välja
            elif event.key == pygame.K_q:  # Kui vajutatakse Q nuppu
                pygame.quit()  # Väljuge mängust
                sys.exit()

        # Kontrollige nuppe
        self.start_button.handle_events(event)
        self.quit_button.handle_events(event)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.start_button.render(screen, (WIDTH // 2 - 100, HEIGHT // 2 - 30))  # Paigutame Start nupu
        self.quit_button.render(screen, (WIDTH // 2 - 100, HEIGHT // 2 + 30))  # Paigutame Quit nupu
        title_text = pygame.font.Font(None, 48).render(self.game_title, True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))


    def quit_game(self):
        """Kui nupp Quit vajutatakse, siis lõpetame mängu."""
        pygame.quit()
        sys.exit()