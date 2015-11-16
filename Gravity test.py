# Gravity test

import pygame, sys, gravity, math, numpy


screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("ExeSoft particle engine gravity test")
clock = pygame.time.Clock()


# Magnitude of a vector
def mag(v):
	return math.sqrt(v[0]**2 + v[1]**2)

# Draw the supplied gravitational point sources' fields to the supplied surface
def DrawField(sources, surf):
	surf.fill((0, 0, 0))
	maxforce = sources[0].GetMaxForce()  # Not accurate (should take the largest max force) but bollocks to it
	pixels = pygame.surfarray.pixels3d(surf)
	
	for x in range(0, 600):
		for y in range(0, 480):
			forcemag = 0
			for source in sources:
				forcemag += mag(source.GetForce((x, y)))
			
			# Map force to colour (chopped at 255)
			col = (forcemag * 255.0) / 10.0
			if col > 255.0:
				col = 255.0
			
			pixels[x][y] = [col, col, col]
	
	return surf
	

surf = pygame.Surface((600, 480))
grav = gravity.PointGravity(9.8, (300, 240))
grav2 = gravity.PointGravity(9.8, (400, 300))
surf = DrawField([grav, grav2], surf)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEMOTION:
			pygame.mouse.get_pos()
	
	screen.blit(surf, (0, 0))
	
	a = pygame.mouse.get_pos()
	f = grav.GetForce(a)
	g = grav2.GetForce(a)
	b = [a[0] + f[0] + g[0], a[1] + f[1] + g[1]]
	pygame.draw.aaline(screen, (0, 255, 0), a, b)
	
	pygame.display.update()
	clock.tick(30)
