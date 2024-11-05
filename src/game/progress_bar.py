import time

FPS = 60
clock = pygame.time.Clock()


# Mängu kestus (sekundites)
GAME_DURATION = 60  # Mäng kestab 60 sekundit
start_time = time.time()  # Salvestame mängu algusaja



# Põhitsükkel
while True:
    current_time = time.time() - start_time  # Aeg alates mängu algusest

    # Kontrollime, kas mänguaeg on läbi
    if current_time >= GAME_DURATION:
        print("Mängu aeg on läbi! Skoor:", score)
        running = False

    # Kuvame ajakulu progressiriba ülaosas
    time_left = max(0, GAME_DURATION - current_time)  # Järelejäänud aeg
    progress_width = int((time_left / GAME_DURATION) * 200)  # Progressiriba laius
    pygame.draw.rect(screen, VALGE, (200, 10, 200, 20), 2)  # Riba raam
    pygame.draw.rect(screen, (0, 255, 0), (200, 10, progress_width, 20))  # Täituv progressiriba