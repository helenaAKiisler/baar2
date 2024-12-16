# Mängus olevate objektide klassid mis määravad ära lauad, baari, klaasid ja vastase.
import pygame
from settings import WIDTH

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (self.width, self.height))

class Bar(Object):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.rect = self.image.get_rect()

        # Paigutame baari ekraani ülaosas keskele
        self.rect.x = x
        self.rect.y = y

class Table(Object):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Glass(Object):
    def __init__(self, x, y, width, height, image, points):
        super().__init__(x, y, width, height, image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.points = points  # Klaasi punktiväärtus


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

        for table in self.tables:
            if self.rect.colliderect(table.rect):
                self.direction = 1
                self.update_direction("right")

    def update_direction(self, direction):
        if self.direction2 != direction:
            self.direction2 = direction
            flip_x = direction == "left"
            self.image = pygame.transform.flip(self.new_image, flip_x, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

