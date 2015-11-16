import pygame, PyIgnition, sys

INFILE = "Water.ppe"
BGCOL = (255, 255, 255)


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition demo: file I/O :: loading from output of \'PyIgnition demo: collisions\' (Water.py)")
clock = pygame.time.Clock()


effect = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
effect.LoadFromFile(INFILE)
effect.sources[0].SetPos(pygame.mouse.get_pos())


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            effect.sources[0].SetPos(pygame.mouse.get_pos())

    screen.fill(BGCOL)
    effect.Update()
    effect.Redraw()
    
    pygame.display.update()
    clock.tick(30)
