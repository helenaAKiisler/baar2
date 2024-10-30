import pygame
import sys
from pygame.locals import *

# Pygame’i alustamine ja seadistamine
pygame.init()
EKRAANI_LAIUS, EKRAANI_KÕRGUS = 800, 800
ekraan = pygame.display.set_mode((EKRAANI_LAIUS, EKRAANI_KÕRGUS), pygame.RESIZABLE)
pygame.display.set_caption("Baar2")

# Värvid ja muud konstandid. lähevad muutmisele.
TAUSTA_VÄRV = (45, 45, 45)
KAADRIKIIRUS = 60

# Mängu olek. ei ole nähtav hetkel.
kell = pygame.time.Clock()
mäng_pausil = False

# Mängu põhifunktsioonid
def alusta_mäng():
    """Funktsioon mängu alustamiseks ja lähtestamiseks."""
    global mäng_pausil
    mäng_pausil = False

def pane_pausile():
    """Lülitab mängu pausile ja pausilt tagasi."""
    global mäng_pausil
    mäng_pausil = not mäng_pausil

def kuva_mäng_läbi():
    """Kuvab mängu lõpetamise sõnumi ja ootab mängija sisendit. Kuvatav tekst uuel kihil."""
    kiht = pygame.Surface((EKRAANI_LAIUS, EKRAANI_KÕRGUS))
    kiht.set_alpha(200)
    kiht.fill((0, 0, 0))
    ekraan.blit(kiht, (0, 0))

    suur_font = pygame.font.Font(None, 64)
    väike_font = pygame.font.Font(None, 36)
    sõnum_tekst = suur_font.render("Mäng läbi!", True, (255, 0, 0))
    välju_tekst = väike_font.render("Lahku mängust (Q)", True, (255, 255, 255))

    ekraan.blit(sõnum_tekst, (EKRAANI_LAIUS // 2 - sõnum_tekst.get_width() // 2, EKRAANI_KÕRGUS // 3))
    ekraan.blit(välju_tekst, (EKRAANI_LAIUS // 2 - välju_tekst.get_width() // 2, EKRAANI_KÕRGUS // 2 + 50))

    pygame.display.flip()

    # Ootab, kuni mängija vajutab "Q" mängust lahkumiseks
    oota_sisendit = True
    while oota_sisendit:
        for sündmus in pygame.event.get():
            if sündmus.type == QUIT:
                pygame.quit()
                sys.exit()
            elif sündmus.type == KEYDOWN:
                if sündmus.key == K_q:
                    pygame.quit()
                    sys.exit()
        kell.tick(KAADRIKIIRUS)

# Peamine mängu tsükkel
alusta_mäng()

while True:
    ekraan.fill(TAUSTA_VÄRV)

    # Ürituste töötlemine
    for sündmus in pygame.event.get():
        if sündmus.type == QUIT:
            pygame.quit()
            sys.exit()
        elif sündmus.type == KEYDOWN:
            if sündmus.key == K_p:
                pane_pausile()
            elif sündmus.key == K_q:
                kuva_mäng_läbi()

    pygame.display.flip()
    kell.tick(KAADRIKIIRUS)
