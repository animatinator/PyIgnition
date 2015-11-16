## Keyframing test

import keyframes, interpolate, pygame


screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


class Circle:
	def __init__(self, pos, colour, radius, screen):
		self.x = pos[0]
		self.y = pos[1]
		self.r = colour[0]
		self.g = colour[1]
		self.b = colour[2]
		self.rad = radius
		self.screen = screen
		self.variables = {"x":self.x, "y":self.y, "r":self.r, "g":self.g, "b":self.b, "rad":self.rad}
		self.keyframes = []
		self.keyframes.append(keyframes.Keyframe(1, self.variables))
		self.keyframes.append(keyframes.Keyframe(200, {"x":800, "y":600}))
		self.keyframes.append(keyframes.Keyframe(300, {"r":255, "g":0, "b":100}))
		self.keyframes.append(keyframes.Keyframe(350, {"r":0, "y":0}))
		self.keyframes.append(keyframes.Keyframe(400, {"x":400, "y":300, "rad":500}))
		self.curframe = 1
	
	def Update(self):
		self.variables = interpolate.InterpolateKeyframes(self.curframe, self.variables, self.keyframes)
		self.curframe = self.curframe + 1
	
	def Draw(self):
		pygame.draw.circle(self.screen, (self.variables["r"], self.variables["g"], self.variables["b"]), (self.variables["x"], self.variables["y"]), self.variables["rad"])


circle = Circle((0, 0), (0, 255, 0), 10, screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	
	screen.fill((0, 0, 0))
	circle.Update()
	circle.Draw()
	
	pygame.display.update()
	clock.tick(30)