# Mängus olevate objektide klassid mis määravad ära lauad, baari, klaasid ja vastase.
import pygame
from settings import GRAY,WIDTH


class Bar(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        new_image = pygame.transform.scale(image, (width, height))
        self.image = new_image
        self.rect = self.image.get_rect()

        # Paigutame baari ekraani ülaosas keskele
        self.rect.x = (WIDTH - self.rect.width) // 2  # Baar on keskendatud horisontaalselt
        self.rect.y = 50 # Baar asub ekraani ülaservas, kuid natuke allpool

class Table(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        new_image = pygame.transform.scale(image, (64, 64))
        self.image = new_image  # Määrame laua suuruse
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)


class Glass(pygame.sprite.Sprite):
    def __init__(self, x, y, image, points):
        super().__init__()
        new_image = pygame.transform.scale(image, (20, 20))
        self.image = new_image  # Klaasi pilt
        self.rect = self.image.get_rect(topleft=(x, y))  # Määrame klaasi positsiooni ja suuruse, et see oleks sama suur kui pilt
        self.points = points  # Klaasi punktiväärtus

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Joonistame klaasi ekraanile

    def check_pickup(self, player, score):
        # laiendan klaasi üleskorjamis/kokkupõrke ala
        pickup_area = self.rect.inflate(80, 80)

        if pickup_area.colliderect(player.rect):
            score += self.points
            return True, score  # Tagastame True, et klaas saaks eemaldada
        return False, score


class Enemy(pygame.sprite.Sprite):
    BASE_SPEED = 2  # Muudame kiiruselõigu, et liikumine oleks sujuvam

    def __init__(self, x, y, image, tables):
        super().__init__()
        self.new_image = pygame.transform.scale(image, (64, 64))
        self.image = self.new_image
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y
        self.paused = False  # Lisame pausiseisundi atribuudi
        self.direction2 = "right"

        # Liikumise algsuund (paremale)
        self.direction = 1  # 1 tähendab paremale, -1 vasakule
        self.tables = tables  # Lauad, millega vaenlane võib kokkupõrked teha

    def update(self):
        """Vaenlase liikumine ühesuunaliselt (näiteks paremale või vasakule)."""
        if self.paused:
            return  # Peatame liikumise, kui mäng on pausil

        # Uus positsioon enne liikumist
        new_rect = self.rect.move(self.BASE_SPEED * self.direction, 0)

        # Kontrolli, kas uus positsioon on ekraani sees
        if new_rect.right >= WIDTH or new_rect.left <= 0:
            self.direction *= -1  # Muuda suunda

        self.rect = new_rect

        # Kui vaenlane jõuab ekraani äärde, muudame liikumissuunda
        if self.rect.right >= pygame.display.get_surface().get_width():
            self.direction = -1  # Muudame suunda vasakule
            self.update_direction("left")
        elif self.rect.left <= 0:
            self.direction = 1  # Muudame suunda paremale
            self.update_direction("right")

    def update_direction(self, direction):
        if self.direction2 != direction:
            self.direction2 = direction
            flip_x = direction == "left"
            self.image = pygame.transform.flip(self.new_image, flip_x, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

