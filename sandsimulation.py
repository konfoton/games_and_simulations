import pygame
import sys
import random
pygame.init()
WINDOW = pygame.display.set_mode((800, 800))
pygame.display.set_caption("sand simulator")
timer = pygame.time.Clock()

class Grain():
     def __init__(self, surface, pos):
          self.color = surface
          self.recto = surface.get_rect(center=pos)

random_clours = [pygame.Surface((10, 10)) for x in range(100)]
for x in random_clours:
     x.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))

def create_rec(pos, color):
    a = Grain(color, pos)
    allrec.append(a)

allrec = []
removed = []
running = True
deleted = False
mouse_button_held = False
color = random.choice(random_clours)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
             mouse_button_held = True
        elif event.type == pygame.MOUSEBUTTONUP:
             mouse_button_held = False
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:
                  color = random.choice(random_clours)
    if mouse_button_held:
         mouse_pos = pygame.mouse.get_pos()
         create_rec(((mouse_pos[0] // 10 * 10) + 5, (mouse_pos[1] // 10) * 10 + 5), color)
    WINDOW.fill((0, 0, 0))
    for rec in removed:
         WINDOW.blit(rec.color, rec.recto)
    for rec in allrec:
         WINDOW.blit(rec.color, rec.recto)
         for rec1 in removed:
              if rec.recto.y + 10 == rec1.recto.y and rec.recto.x == rec1.recto.x:
                   deleted = True
                   allrec.remove(rec)
                   removed.append(rec)
                   break
         if not deleted:
            if rec.recto.y < 790:
                rec.recto.y += 10
            if rec.recto.y == 790:
                removed.append(rec)
                allrec.remove(rec)
         deleted = False
            

    
    timer.tick(60)
    pygame.display.update()
