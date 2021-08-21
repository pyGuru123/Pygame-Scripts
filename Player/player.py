import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()
		self.x = x
		self.y = y

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.width = 24
		self.height = 24

		for i in range(1,3):
			image = pygame.image.load(f'Player/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (self.width, self.height))
			self.idle_list.append(image)
		for i in range(1,6):
			image = pygame.image.load(f'Player/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (self.width, self.height))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 5):
			image = pygame.image.load(f'Player/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (self.width, self.height))
			self.attack_list.append(image)
		for i in range(1,11):
			image = pygame.image.load(f'Player/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (self.width, self.height))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'Player/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (self.width, self.height))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.fall_index = 0

		self.speed = 3
		self.vel = 15
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False

		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		pass

	def update(self, moving_left, moving_right, world):
		dx = 0
		dy = 0

		if moving_left:
			dx = -self.speed
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.direction = 1
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump:
			F = (1/2) * self.mass * self.vel
			dy -= F
			self.vel -= self.gravity
			print(self.vel)

			if self.vel < -16:
				self.vel = 15
				self.mass = 1
				self.jump = False
		else:
			dy += self.vel

		if self.rect.bottom + dy > 200:
			self.rect.bottom = 200
			dy = 0

		dx, dy = self.check_collision(world, dx, dy)

		self.rect.x += dx
		self.rect.y += dy

		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.direction == -1:
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]

	def draw(self, win):
		win.blit(self.image, self.rect)
