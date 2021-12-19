import pygame
import os
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Homies")

MAIN_FONT = pygame.font.Font(None, 40)
SEC_FONT = pygame.font.Font(None, 35)

ENTITY_WIDTH, ENTITY_HEIGHT = 60, 80

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (71, 95, 119)

# images
BG = pygame.transform.scale(pygame.image.load('assets/background.jpg'), (WIDTH, HEIGHT))

GOPETO = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'gopeto.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))

TOPALSKI = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'topalski.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))

VIKI = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'viki.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))

PITON = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'piton.png')), (ENTITY_WIDTH, ENTITY_HEIGHT))

pygame.display.set_icon(TOPALSKI)


class StartButton:
    def __init__(self, text, width, height, pos, elevation):
        # core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_position = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bot_rect = pygame.Rect(pos, (width, elevation))
        self.bot_color = '#354B5E'

        # text
        self.text_surf = MAIN_FONT.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_position - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bot_rect.midtop = self.top_rect.midtop
        self.bot_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(WIN, self.bot_color, self.bot_rect, border_radius=12)
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius=12)
        WIN.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.dynamic_elevation = 0
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    catch()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'


class ExitButton:
    def __init__(self, text, width, height, pos, elevation):
        # core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_position = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bot_rect = pygame.Rect(pos, (width, elevation))
        self.bot_color = '#354B5E'

        # text
        self.text_surf = MAIN_FONT.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, ):
        # elevation logic
        self.top_rect.y = self.original_y_position - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bot_rect.midtop = self.top_rect.midtop
        self.bot_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(WIN, self.bot_color, self.bot_rect, border_radius=12)
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius=12)
        WIN.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.dynamic_elevation = 0
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    pygame.quit()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'


class Player:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.player_img = GOPETO
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health

    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.player_img.get_height() + 10, self.player_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.player_img.get_height() +
                         10, self.player_img.get_width() * (self.health/self.max_health), 10))

    def get_width(self):
        return self.player_img.get_width()

    def get_height(self):
        return self.player_img.get_height()


class Heal:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.heal_img = HEAL_IMG
        self.mask = pygame.mask.from_surface(self.heal_img)

    def move(self, vel):
        self.y += vel + 4

    def draw(self, window):
        window.blit(self.heal_img, (self.x, self.y))

    def get_width(self):
        return self.heal_img.get_width()

    def get_height(self):
        return self.heal_img.get_height()


class Homie:
    HOMIE_MAP = {
        'topalski': TOPALSKI,
        'viki': VIKI,
        'piton': PITON
    }

    def __init__(self, x, y, homie_type):
        self.x = x
        self.y = y
        self.homie_img = self.HOMIE_MAP[homie_type]
        self.mask = pygame.mask.from_surface(self.homie_img)

    def move(self, vel):
        self.y += vel

    def draw(self, window):
        window.blit(self.homie_img, (self.x, self.y))

    def get_width(self):
        return self.homie_img.get_width()

    def get_height(self):
        return self.homie_img.get_height()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def catch():
    FPS = 60
    run = True
    clock = pygame.time.Clock()

    button1 = ExitButton('Exit', 120, 40, (10, 550), 6)

    player_vel = 5
    homie_vel = 1
    level = 0
    homies = []
    wave_length = 5
    points = 0

    lost = False
    lost_count = 0

    player = Player(270, 402)

    def redraw_catch():
        WIN.blit(BG, (0, 0))

        points_label = SEC_FONT.render(
            f"Homies Catched: {points}", 1, WHITE)
        level_label = SEC_FONT.render(
            f"Level: {level}", 1, WHITE)

        WIN.blit(points_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for homie in homies:
            homie.draw(WIN)

        player.draw(WIN)

        button1.draw()

        if lost:
            lost_label = MAIN_FONT.render("You Lost!", 1, WHITE)
            WIN.blit(lost_label, (WIDTH/2 -
                     lost_label.get_width()/2, HEIGHT/2 - 50))

        pygame.display.update()

    def player_movement():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel

        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel

    while run:
        clock.tick(FPS)

        if len(homies) == 0:
            level += 1
            wave_length += 3

            for i in range(wave_length):
                homie = Homie(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                            random.choice(["topalski", "viki", "piton"]))
                homies.append(homie)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        redraw_catch()

        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        player_movement()

        for homie in homies[:]:
            homie.move(homie_vel)

            if collide(homie, player):
                points += 1
                homies.remove(homie)

                if points % 10 == 0 and player.health <= 99:
                    player.health += 10

                if points % 25 == 0:
                    FPS += 5

            elif homie.y + homie.get_height() > HEIGHT - 115:
                player.health -= 10
                homies.remove(homie)


def main_menu():
    FPS = 60
    run = True
    clock = pygame.time.Clock()

    homie1 = Homie(40, 402, random.choice(["topalski", "viki", "piton"]))
    homie2 = Homie(500, 402, random.choice(["topalski", "viki", "piton"]))
    homie3 = Homie(270, 402, random.choice(["topalski", "viki", "piton"]))

    title_label = MAIN_FONT.render('CATCH THE HOMIES!', 1, WHITE)

    # buttons
    button1 = StartButton('Start the game', WIDTH/2,
                          40, (WIDTH/2 - 150, 250), 6)
    button2 = ExitButton('Exit the game', WIDTH/2,
                         40, (WIDTH/2 - 150, 300), 6)

    def redraw_main_menu():
        WIN.blit(BG, (0, 0))

        pygame.draw.rect(WIN, GREY, pygame.Rect(WIDTH/2 - title_label.get_width()/2 - 10,
                         190, title_label.get_width() + 20, title_label.get_height() + 20), border_radius=12)

        WIN.blit(title_label, (
            WIDTH/2 - title_label.get_width()/2, 200))

        button1.draw()
        button2.draw()

        homie1.draw(WIN)
        homie2.draw(WIN)
        homie3.draw(WIN)

        pygame.display.update()

    # main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        redraw_main_menu()

        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
