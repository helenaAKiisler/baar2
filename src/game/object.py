# Mängus olevate objektide klassid mis määravad ära lauad, baari, klaasid ja vastase.
import pygame
from settings import GRAY,WIDTH


class Bar(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image = pygame.Surface((width, 50))  # Baar on laiem, kõrgus 50px
        self.image.fill((99, 102, 106))  # Baaril pruun värv
        self.rect = self.image.get_rect()

        # Paigutame baari ekraani ülaosas keskele
        self.rect.x = (WIDTH - width) // 2  # Baar on keskendatud horisontaalselt
        self.rect.y = 50  # Baar asub ekraani ülaservas, kuid natuke allpool

class Table(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image  # Määrame laua suuruse
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)


class Glass(pygame.sprite.Sprite):
    def __init__(self, x, y, image, points):
        super().__init__()
        self.image = image  # Klaasi pilt
        self.rect = self.image.get_rect(topleft=(x, y))  # Määrame klaasi positsiooni
        self.points = points  # Klaasi punktiväärtus

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Joonistame klaasi ekraanile

    def check_pickup(self, player, score):
        # laiendan klaasi üleskorjamis/kokkupõrke ala
        pickup_area = self.rect.inflate(100, 100)

        if pickup_area.colliderect(player.rect):
            score += self.points
            return True, score  # Tagastame True, et klaas saaks eemaldada
        return False, score


class Enemy(pygame.sprite.Sprite):
    BASE_SPEED = 2  # Muudame kiiruselõigu, et liikumine oleks sujuvam

    def __init__(self, x, y, image, tables):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y

        # Liikumise algsuund (paremale)
        self.direction = 1  # 1 tähendab paremale, -1 vasakule
        self.tables = tables  # Lauad, millega vaenlane võib kokkupõrked teha

    def update(self):
        """Vaenlase liikumine ühesuunaliselt (näiteks paremale või vasakule)."""
        # Uus positsioon enne liikumist
        new_rect = self.rect.move(self.BASE_SPEED * self.direction, 0)

        # Kontrollime, kas uus positsioon ei kattu laudadega
        if not any(new_rect.colliderect(table.rect) for table in self.tables):
            self.rect = new_rect  # Lubame liikumise ainult siis, kui ei kattu laudadega
        else:
            # Kui vaenlane puutub kokku lauaga, muudame liikumissuunda
            self.direction *= -1  # Keerame ümber (liikumine vastassuunas)

        # Kui vaenlane jõuab ekraani äärde, muudame liikumissuunda
        if self.rect.right >= pygame.display.get_surface().get_width():
            self.direction = -1  # Muudame suunda vasakule
        elif self.rect.left <= 0:
            self.direction = 1  # Muudame suunda paremale

    def draw(self, surface):
        surface.blit(self.image, self.rect)
