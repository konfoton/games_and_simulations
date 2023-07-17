import pygame
import sys
import time
import math
import matplotlib.pyplot as plt
time_since_start = 0
length_of_fly = 5
pygame.init()
screen = pygame.display.set_mode((1650, 1000))
pygame.display.set_caption("projectile-simulation")
clock = pygame.time.Clock()
projectile = pygame.Rect((0, 0), (50, 50))
check = 0.5
gravity = 0.5
vertical_velocity = gravity
background = pygame.image.load("552685.png")
game_state = pygame.image.load("ae7a43df1e16b9710694002bbd2b2f5763b20e4a.jpeg")
game_state_scaled = pygame.transform.scale(game_state, (1650, 1000))
captions = pygame.font.Font(None, 50)
text_surface = captions.render(f"Time: {length_of_fly}", True, (255, 255, 255))
game_active = False
text_surface_two = pygame.font.Font(None, 100).render("START", True, (255, 255, 255))
text_surface_three = pygame.font.Font(None, 100).render("MENU", True, (255, 255, 255))
text_rectangle_three = text_surface_three.get_rect(midbottom=(1650 / 2, 600))
text_rectangle = text_surface_two.get_rect(midbottom=(1650 / 2, 500))
time_value = []
velocity_value = []


def determine_velocity(vertical, horizontal):
    return round(math.sqrt((vertical ** 2 + horizontal ** 2)), 2)


def wow():
    while True:
        yield True
        yield False


current_generator = wow()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(time_value) != 0:
                    plt.plot(time_value, velocity_value)
                    plt.title("V(t) i.e. vkurwienie od czasu")
                    plt.xlabel("time")
                    plt.ylabel("velocity")

                    plt.show()
                time_value.clear()
                velocity_value.clear()
                projectile.x = 0
                projectile.y = 0
                vertical_velocity = 0.5
                game_active = next(current_generator)
    if game_active:
        if projectile.centery < 30:
            time_since_start = time.time()
        length_of_fly = round(time.time() - time_since_start, 2)
        text_surface = captions.render(f"Time: {length_of_fly}", True, (255, 255, 255))
        text_surface_one = captions.render(f"Velocity: {determine_velocity(vertical_velocity, 5)}", True,
                                           (255, 255, 255))
        vertical_velocity += 0.04
        time_value.append(length_of_fly)
        velocity_value.append(determine_velocity(vertical_velocity, 5))
        if projectile.centery > 1100:
            time_value.clear()
            velocity_value.clear()
            length_of_fly = 0
            projectile.x = 0
            projectile.y = 0
            vertical_velocity = 0.5
        screen.blit(background, (0, 0))
        screen.blit(text_surface, (1200, 40))
        screen.blit(text_surface_one, (1200, 100))
        pygame.draw.line(screen, (0, 255, 0), (projectile.centerx, projectile.centery),
                         (projectile.centerx + 200, projectile.centery))
        pygame.draw.line(screen, (255, 0, 0), (projectile.centerx, projectile.centery),
                         (projectile.centerx, projectile.centery + 100))
        pygame.draw.rect(screen, (255, 255, 255), projectile)
        projectile.x += 5
        projectile.y += vertical_velocity

    else:
        screen.fill((0, 0, 0))
        screen.blit(text_surface_two, text_rectangle)
        screen.blit(text_surface_three, text_rectangle_three)
        mouse = pygame.mouse.get_pos()

        if text_rectangle.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            game_active = True
        if text_rectangle_three.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            pass

    pygame.display.update()
    clock.tick(60)
