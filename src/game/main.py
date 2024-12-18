################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Baar2 mäng
#
#
# Autorid: Helena Angela Kiisler, Lauri Tõnisson
#
# mõningane eeskuju: Internetist leitavad juba koostatud pygame mängud.
#
# Lisakommentaar (nt käivitusjuhend)
# Mängu käivitamiseks tuleb käivitada main.py. Mängija liikumiseks kasuta klaviatuuril nooleklahve või WASD klahvikombinatsioone.
# Nuppudele vajutamine toimub vasaku hiireklahviga. Vajutades klahvi P läheb mäng pausile.
# Klaase saab korjata vajutades X ja klaase saab maha panna baari juures SPACE klahviga.
##################################################
import pygame
import sys
import os
from settings import WIDTH, HEIGHT
from pohiloogika import Game
from scene import Scene
from main_menu import MainMenu, WinMenu

# Algseaded
pygame.init()
pygame.display.set_caption("Baar2")
clock = pygame.time.Clock()
GAME_TITLE = "Baar2"
score = 0
game = Game()
game.start_game()
current_scene: Scene

# Mängu initseerimine
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Loome screen objekti

#Lisame muusika
pygame.mixer.music.load("../../assets/sfx/menu.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

# Ekraani stseenivahetus funktsioon
def scene_switcher(new_scene_name, screen=None, level=1):
    from game_level import GameLevel, TutorialLevel
    global current_scene
    if new_scene_name == "MainMenu":
        from main_menu import MainMenu
        pygame.mixer.music.load("../../assets/sfx/menu.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        current_scene = MainMenu(scene_switcher, game_title="Baar 2", screen=screen)
    elif new_scene_name == "TutorialLevel":
        current_scene = TutorialLevel(scene_switcher, screen=screen)
        pygame.mixer.music.load("../../assets/sfx/tutorial.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
    elif new_scene_name == "GameLevel":
        pygame.mixer.music.load("../../assets/sfx/background.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        current_scene = GameLevel(scene_switcher, screen=screen, level=level)
    elif new_scene_name == "WinMenu":
        pygame.mixer.music.load("../../assets/sfx/win.mp3")
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.queue("../../assets/sfx/menu.mp3")
        current_scene = WinMenu(scene_switcher, text="You won!", screen=screen)

# Põhifunktsioon
def main():
    global current_scene, score, game_timer

    # Algne stseen
    current_scene = MainMenu(scene_switcher, game_title="Baar 2", screen=screen)

    # Mängutsükkel
    while current_scene.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            current_scene.handle_events(event)  # Kontrollime sündmusi (ka nupu vajutamist)

        current_scene.update()  # Uuendab mänguloogikat, sealhulgas mängija liikumist
        current_scene.render(screen)  # Edastame screen objekti
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()