# Start menüü kuvamine ekraanile ja nuppude seaded.
import pygame
import sys
import ui
from settings import WIDTH, HEIGHT
from scene import Scene

class MainMenu(Scene):
    BACKGROUND_COLOR = pygame.Color(16, 72, 36)

    def __init__(self, scene_switcher, game_title, screen=None):
        super().__init__(scene_switcher)
        self.game_title = game_title
        self.screen = screen
        # Start nupp
        self.start_button = ui.Button("Start", on_pressed=lambda: self.scene_switcher("GameLevel", screen))
        # Quit nupp
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_game)  # Quit nupp, mis viib tagasi MainMenu

    # Siin töötleme sündmusi (ka nuppude vajutamist).
    def handle_events(self, event):

        # Kontrollige nuppe
        self.start_button.handle_events(event)
        self.quit_button.handle_events(event)
    # Nuppude paigutamine ekraanile
    def render(self, screen):
        screen.fill(self.BACKGROUND_COLOR)
        self.start_button.render(screen, (
            (screen.get_width() - self.start_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - self.start_button.get_height() - 120))  # Paigutame Start nupu
        self.quit_button.render(screen, (
            (screen.get_width() - self.quit_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - 110)) # Paigutame Quit nupu
        title_text = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 48).render(self.game_title, True, (152, 191, 161))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def toggle_pause(self):
        pass

class WinMenu(Scene):
    BACKGROUND_COLOR = pygame.Color(16, 72, 36)

    def __init__(self, scene_switcher, text, screen=None):
        super().__init__(scene_switcher)
        self.screen = screen
        self.text = text
        self.restart_button = ui.Button("Play again", on_pressed=lambda: self.scene_switcher("GameLevel", screen))
        self.quit_button = ui.Button("Quit", on_pressed=self.quit_game)  # Quit nupp, mis viib tagasi MainMenu

    # Siin töötleme sündmusi (ka nuppude vajutamist).
    def handle_events(self, event):

        # Kontrollige nuppe
        self.restart_button.handle_events(event)
        self.quit_button.handle_events(event)
    # Nuppude paigutamine ekraanile
    def render(self, screen):
        screen.fill(self.BACKGROUND_COLOR)
        self.restart_button.render(screen, (
            (screen.get_width() - self.restart_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - self.restart_button.get_height() - 120))  # Paigutame Restart nupu
        self.quit_button.render(screen, (
            (screen.get_width() - self.quit_button.get_width()) / 2,
            screen.get_height() - self.quit_button.get_height() - 110))  # Paigutame Quit nupu
        win_text = pygame.font.Font("../../assets/font/InknutAntiqua-Regular.ttf", 48).render(self.text, True, (152, 191, 161))
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 4))

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def toggle_pause(self):
        pass