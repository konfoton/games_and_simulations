import pygame
import sys
import random
pygame.init()
#game variables

WINDOW = pygame.display.set_mode((800, 500))
pygame.display.set_caption("FlappyBirdAI")
timer = pygame.time.Clock()
rect1 = pygame.rect.Rect(0, -10, 500, 10)
rect2 = pygame.rect.Rect(0, 510, 500, 10)
counter = 299
running = True
game_state = True
level = 0 
#some classes and useful functions


class pipes():
    instances = []
    def __init__(self) -> None:
        radom_length1 = random.randint(10, 250)
        radom_length2 = random.randint(10, 250)
        if radom_length1 > 180 and radom_length2 > 180:
            radom_length2 = 100
        if radom_length1 > 220 and radom_length2 > 150:
            radom_length2 = 100
        if radom_length1 > 150 and radom_length2 > 220:
            radom_length1 = 100
        self.surface1 = pygame.Surface((60, radom_length1))
        self.surface2 = pygame.Surface((60, radom_length2))
        self.surface1.fill((255, 255, 255))
        self.surface2.fill((255, 255, 255))
        self.rect1 = self.surface1.get_rect(topleft=(800, 0))
        self.rect2 = self.surface2.get_rect(bottomleft=(800, 500))

        pipes.instances.append(self)

    @classmethod
    def delete(cls):
        for pipe in cls.instances:
            if pipe.rect1.x < -100:
                cls.instances.remove(pipe)

    @classmethod
    def move(cls):
        for pipe in cls.instances:
            pipe.rect1.x -= 1
            pipe.rect2.x -= 1
    
    @classmethod
    def draw(cls):
        for pipe in cls.instances:
            WINDOW.blit(pipe.surface1, pipe.rect1)
            WINDOW.blit(pipe.surface2, pipe.rect2)

    @classmethod
    def run(cls):
        cls.delete()
        cls.move()
        cls.draw()

def managepipes():
    global counter
    counter += 1
    if counter == 300:
        pipes()
        counter = 0

class Bird:
    def __init__(self, cor):
        self.surface = pygame.Surface((50, 50))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect(center=cor)
        self.velocity = 0
        self.jumpcooldown = 0
        self.level = 0
 
    def apply_gravity(self):
        self.velocity += 0.2
        self.rect.y += self.velocity

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.jumpcooldown <= 0:
            self.jumpcooldown = 30
            self.velocity -= 10

    def cooldown(self):
        self.jumpcooldown -= 1

    def draw(self):
        WINDOW.blit(self.surface, self.rect)

    def check_colision(self, objects):
        global game_state
        if self.rect.colliderect(rect1) or self.rect.colliderect(rect2):
            pipes.instances.clear()
            game_state = False
        for object in objects.instances:
            if self.rect.colliderect(object.rect1) or self.rect.colliderect(object.rect2):
                pipes.instances.clear()
                game_state = False
    def check_level(self, objects):
        for object in objects.instances:
            if self.rect.x == object.rect1.x + 60:
                self.level += 1
                print(self.level)


#initialization        
player = Bird((150, 250))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                level = 0
                game_state = True
                player = Bird((100, 250))
    if game_state:
        WINDOW.fill((0, 0, 0))
        player.apply_gravity()
        player.movement()
        player.cooldown()
        player.draw()
        player.check_colision(pipes)
        player.check_level(pipes)
        managepipes()
        pipes.run()
    else:
        WINDOW.fill((100, 100, 100))
        font = pygame.font.SysFont(None, 40)
        text = font.render('Game Over! Press R to Restart', True, (255, 0, 0))
        WINDOW.blit(text, (50, 250))
    timer.tick(60)
    pygame.display.update()