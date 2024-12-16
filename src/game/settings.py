import os
import pygame
from os.path import join, abspath, dirname
from pygame.image import load
# Üldised värvid ja seaded mida mängus kasutatakse.

# Ekraani seaded
WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_DURATION = 60  # Mäng kestab 60 sekundit

# Värvid
DARK_BROWN = (101, 67, 33)
BLUE = (0, 0, 255)
OFF_WHITE = (180, 213, 187)
GREEN = (130, 218, 112)
BLACK = (26, 35, 29)
DARK_GRAY = (99, 102, 106)
DARK_GREEN = (16, 72, 36)
LIGHT_GREEN = (91, 139, 102)
RED = (255, 0, 0)

# Mängija seaded
PLAYER_SIZE = 50
PLAYER_SPEED = 5

base_path = abspath(join(dirname(__file__), "..", "..", "assets", "designs"))

background_image = load(join(base_path, "background", "floor.png"))
table_image = load(join(base_path, "table", "table2.png"))
bar_image = load(join(base_path, "background", "baar2.png"))
player_image = load(join(base_path, "character", "mees", "idle.png"))
enemy_image = load(join(base_path, "customer", "klient1.png"))

predefined_table_positions = [
            (466, 536), (272, 226), (272, 381), (466, 381), (272, 536),
            (466, 226), (80, 472), (80, 322), (80, 170), (664, 320)
        ]

predefined_enemy_positions = [
            (144, 162), (144, 304), (596, 440), (726, 246)
        ]

glass_types = [
            {"image": load(join(base_path, "glass", "uusshot.png")),"points": 1},
            {"image": load(join(base_path, "glass", "uusklaas.png")),"points": 2},
            {"image": load(join(base_path, "glass", "uusmartini.png")),"points": 3}
        ]

buttons = ["Continue.png", "Pause.png", "Play_again.png", "Quit.png", "Start.png", "Try_again.png"]
buttons_pressed = ["Continue_pressed.png", "Pause_pressed.png", "Play_again_pressed.png", "Quit_pressed.png", "Start_pressed.png", "Try_again_pressed.png"]
button_path = abspath(join(dirname(__file__), "..", "..", "assets", "designs", "buttons"))