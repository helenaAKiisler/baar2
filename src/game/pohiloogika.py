import pygame
import sys
from settings import DARK_BROWN
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()

        # Ekraani seaded
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Baar2")

        # Mängu muutujad
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.is_paused = False
        self.bg_color = DARK_BROWN

    def start_game(self):
        """Käivitab mängu."""
        self.is_running = True
        self.is_paused = False

    def toggle_pause(self):
        """Lülitab mängu pausile ja pausilt tagasi."""
        if self.is_running:
            self.is_paused = not self.is_paused

    def quit_game(self):
        """Lõpetab mängu ja sulgeb programmi."""
        pygame.quit()
        sys.exit()

    def display_pause_text(self):
        """Kuvab pausiteate ekraanile."""
        font = pygame.font.Font(None, 48)
        pause_text = font.render("Mäng on pausil. Jätkamiseks vajuta 'C'", True, 'white')
        self.screen.blit(pause_text, (
        self.screen_width // 2 - pause_text.get_width() // 2, self.screen_height // 2 - pause_text.get_height() // 2))

    def display_start_text(self):
        """Kuvab mängu alguse ja juhiste teksti ekraanile."""
        font = pygame.font.Font(None, 48)
        start_text = font.render("Mängu alustamiseks vajuta 'A'", True, 'white')
        self.screen.blit(start_text, (
        self.screen_width // 2 - start_text.get_width() // 2, self.screen_height // 2 - start_text.get_height() // 2))

    def display_game_text(self):
        """Kuvab mängu käigus kuvatava teksti."""
        font = pygame.font.Font(None, 36)
        game_text = font.render("Mäng töötab...", True, 'white')
        self.screen.blit(game_text, (self.screen_width // 2 - game_text.get_width() // 2, self.screen_height // 2))

    def handle_events(self):
        """Käsitleb kasutaja sisendit ja sündmusi."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Kui vajutatakse 'A', käivitatakse mäng
                    self.start_game()
                elif event.key == pygame.K_p:  # Kui vajutatakse 'P', lülitatakse paus sisse või välja
                    self.toggle_pause()
                elif event.key == pygame.K_q:  # 'Q' lõpetamiseks
                    self.quit_game()
                elif event.key == pygame.K_c and self.is_paused:  # 'C' jätkamiseks, kui mäng on pausil
                    self.toggle_pause()

    def update_screen(self):
        """Uuendab ekraani, kuvades vastava mängu oleku teksti."""
        self.screen.fill(self.bg_color)

        # Kuvame vastava teksti olenevalt mängu olekust
        if self.is_running:
            if self.is_paused:
                self.display_pause_text()
            else:
                self.display_game_text()
        else:
            self.display_start_text()

        pygame.display.flip()

    def run(self):
        """Käivitatakse mängu põhitsükkel."""
        while True:
            self.handle_events()
            self.update_screen()
            self.clock.tick(30)  # 30 FPS


# Käivitame mängu
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.display.flip()
    clock.tick(30)  # 30 FPS
