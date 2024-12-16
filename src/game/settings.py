import os
import pygame
# Üldised värvid ja seaded mida mängus kasutatakse.

# Ekraani seaded
WIDTH, HEIGHT = 800, 600
FPS = 60
GAME_DURATION = 60  # Mäng kestab 60 sekundit

# Värvid
DARK_BROWN = (101, 67, 33)
BLUE = (0, 0, 255)
OFF_WHITE = (180, 213, 187)
GRAY = (169, 169, 169)  # Laudade värv
GREEN = (130, 218, 112)
BLACK = (0, 0, 0)
DARK_GRAY = (99, 102, 106)
DARK_GREEN = (16, 72, 36)
LIGHT_GREEN = (91, 139, 102)
RED = (255, 0, 0)

# Mängija seaded
PLAYER_SIZE = 50
PLAYER_SPEED = 5

# Klaaside seaded
GLASS_SIZE = 30
TABLE_SIZE = 60

# Juhuslikud laua positsioonid (kindlad kohad)
PRESET_TABLE_POSITIONS = [
    (100, 150), (300, 150), (500, 150), (200, 350), (400, 350)
]
