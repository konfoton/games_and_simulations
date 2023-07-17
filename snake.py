import pygame
import sys
import random

pygame.init()
WINDOW = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
grid = pygame.rect.Rect((0, 0), (40, 40))
list_of_rectangles = []
game_active = False


class Player(pygame.sprite.Sprite):
    changer = 1
    body = []
    temporary = True
    counter = 1

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill('green')

        self.rect = self.image.get_rect(topleft=(0, 0))
        Player.body.append(self.rect)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            Player.changer = 2
        elif keys[pygame.K_d]:
            Player.changer = 1
        elif keys[pygame.K_w]:
            Player.changer = 3
        elif keys[pygame.K_a]:
            Player.changer = 4
        if Player.changer == 1:
            self.rect.x += 40
        elif Player.changer == 2:
            self.rect.y += 40
        elif Player.changer == 3:
            self.rect.y -= 40
        elif Player.changer == 4:
            self.rect.x -= 40

    def collide_rect(self, collider):
        if self.rect.colliderect(collider):
            Player.body.append(self.rect.copy())
            Player.counter += 1
            return None
        else:
            return collider

    def collide_border(self, file):
        if self.rect.x < 0 or self.rect.x == 600 or self.rect.y < 0 or self.rect.y == 600:
            with open(file, 'a') as f:
                f.write(str(f"{Player.counter}\n"))
            return False
        else:
            return True

    def collide_body(self, file):
        for body in Player.body:
            if body is self.rect:
                continue
            if self.rect.colliderect(body):
                with open(file, 'a') as f:
                    f.write(str(f"{Player.counter}\n"))
                return False
        return True

    @staticmethod
    def draw_body(window, surface):
        for index, body in enumerate(Player.body):
            if index == 0:
                continue
            window.blit(surface, body)
        store_x = [x_value.x for x_value in Player.body]
        store_y = [y_value.y for y_value in Player.body]
        for index, body in enumerate(Player.body):
            if index == 0:
                continue
            Player.body[index].x = store_x[index - 1]
            Player.body[index].y = store_y[index - 1]

    def update(self):
        self.movement()


player_object = Player()
player = pygame.sprite.GroupSingle()
player.add(player_object)

surface_for_display = pygame.image.load('pixil-frame-0.png').convert_alpha()
current_surface = None

body_for_display = pygame.Surface((40, 40))
body_for_display.fill('Green')

background_music = pygame.mixer.Sound('eastern-hip-hop-music-light-meditative-vlog-music-for-video-oasis-153257.mp3')
background_music.play(-1)

test_font = pygame.font.Font(None, 50)
test_font_1 = pygame.font.Font(None, 100)
text_surface = test_font_1.render('START', True, "black")
rectangle_test = text_surface.get_rect(center=(300, 250))
text_surface_1 = test_font.render("CLICK SPACE TO START", True, "black")
rectangle_1 = text_surface_1.get_rect(center=(300, 400))
highest_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player.counter = 1
                game_active = True
                Player.body.clear()
                Player.changer = 1
                player_object.rect.x = 0
                player_object.rect.y = 0
                Player.body.append(player_object.rect)
    if game_active:
        WINDOW.fill((0, 0, 0))
        for x in range(0, 561, 40):
            for y in range(0, 561, 40):
                grid = pygame.rect.Rect((x, y), (40, 40))
                pygame.draw.rect(WINDOW, 'White', grid, 1)
                list_of_rectangles.append(grid)
        if current_surface is None:
            current_surface = random.choice(list_of_rectangles)
        WINDOW.blit(surface_for_display, current_surface)

        current_surface = player_object.collide_rect(current_surface)
        game_active = player_object.collide_border("highscore_game.txt")
        if game_active:
            player.update()
            game_active = player_object.collide_body("highscore_game.txt")
            player.draw(WINDOW)
            player_object.draw_body(WINDOW, body_for_display)
    else:
        highscore = test_font.render(f"Highscore: {highest_score}", True, "black")
        rectangle_2 = highscore.get_rect(center=(300, 500))
        with open('highscore_game.txt', "r") as f:
            for x in f:
                if int(x.strip()) > highest_score:
                    highest_score = int(x)
        WINDOW.fill((100, 100, 100))
        WINDOW.blit(text_surface, rectangle_test)
        WINDOW.blit(text_surface_1, rectangle_1)
        WINDOW.blit(highscore, rectangle_2)
    pygame.display.update()
    clock.tick(10)
