import sys, random, math, pygame
from pygame.locals import *
import time

pygame.init()
pygame.fastevent.init()
screen = pygame.display.set_mode((1200,800))


screen.fill((204, 232, 207))

s = []
s.append( pygame.image.load("quarter-note-isolated.png").convert_alpha())
s.append( pygame.image.load("8thNote.svg.png").convert_alpha())
s.append( pygame.image.load("half-note-isolated.png").convert_alpha())
s.append( pygame.image.load("isolated-eight-note.png").convert_alpha())
s.append( pygame.image.load("whole-note-music-by-vexels.png").convert_alpha())

help(pygame.time.set_timer)

for i in range(len(s)):

    screen.blit( pygame.transform.smoothscale(s[i], (200, 200)), (200*i, 0))


#_fclef = pygame.image.load("fclef.png").convert_alpha()

#gclef = pygame.transform.smoothscale(_gclef, (int(95*0.9), int(264*0.9)))
#fclef = pygame.transform.smoothscale(_fclef, (int(78*1.2), int(90*1.2)))



pygame.display.update()

while True:
    time.sleep(10)


