import pygame
import sys

# Pygame'i algväärtustamine
pygame.init()

# Ekraani suurus ja tausta värv
ekraani_laius, ekraani_kõrgus = 800, 600
ekraan = pygame.display.set_mode((ekraani_laius, ekraani_kõrgus), pygame.RESIZABLE)
pygame.display.set_caption("Baar2")
tausta_värv = ('sienna')

# Mängu muutujad
kell = pygame.time.Clock()
mäng_käib = False  # Kontrollib, kas mäng on käima pandud
mäng_pausil = False  # Kontrollib, kas mäng on pausil

def alusta_mäng():
    """Käivitab mängu."""
    global mäng_käib, mäng_pausil
    mäng_käib = True
    mäng_pausil = False

def pane_pausile():
    """Lülitab mängu pausile ja pausilt tagasi."""
    global mäng_pausil
    if mäng_käib:  # Ainult juhul, kui mäng käib
        mäng_pausil = not mäng_pausil

def lõpeta_mäng():
    """Lõpetab mängu ja sulgeb programmi."""
    pygame.quit()
    sys.exit()

def kuva_pausi_tekst():
    """Kuvab pausiteate ekraanile."""
    font = pygame.font.Font(None, 48)
    pausitekst = font.render("Mäng on pausil. Jätkamiseks vajuta 'C'", True, ('white'))
    ekraan.blit(pausitekst, (ekraani_laius // 2 - pausitekst.get_width() // 2, ekraani_kõrgus // 2 - pausitekst.get_height() // 2))

def kuva_algus_tekst():
    """Kuvab mängu alguse ja juhiste teksti ekraanile."""
    font = pygame.font.Font(None, 48)
    alusta_teksti = font.render("Mängu alustamiseks vajuta 'A'", True, ('white'))
    ekraan.blit(alusta_teksti, (ekraani_laius // 2 - alusta_teksti.get_width() // 2, ekraani_kõrgus // 2 - alusta_teksti.get_height() // 2))

# Mängu tsükkel
while True:
    # Ürituste kontroll
    for sündmus in pygame.event.get():
        if sündmus.type == pygame.QUIT:
            lõpeta_mäng()
        elif sündmus.type == pygame.KEYDOWN:
            if sündmus.key == pygame.K_a:  # Kui vajutatakse 'A', käivitatakse mäng
                alusta_mäng()
            elif sündmus.key == pygame.K_p:  # Kui vajutatakse 'P', lülitatakse paus sisse või välja
                pane_pausile()
            elif sündmus.key == pygame.K_q:  # 'Q' lõpetamiseks
                lõpeta_mäng()
            elif sündmus.key == pygame.K_c and mäng_pausil:  # 'C' jätkamiseks, kui mäng on pausil
                pane_pausile()

    # Tausta värvimine
    ekraan.fill(tausta_värv)

    # Kontroll, kas mäng on käivitatud ja pausil
    if mäng_käib:
        if mäng_pausil:
            kuva_pausi_tekst()
        else:
            # Joonistame mängu sisu siin, kui mäng pole pausil
            font = pygame.font.Font(None, 36)
            mängutekst = font.render("Mäng töötab...", True, ('white'))
            ekraan.blit(mängutekst, (ekraani_laius // 2 - mängutekst.get_width() // 2, ekraani_kõrgus // 2))
    else:
        kuva_algus_tekst()  # Kuvab juhise mängu alustamiseks

    pygame.display.flip()
    kell.tick(30)  # 30 FPS
