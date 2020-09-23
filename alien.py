import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""Class to represent a single alien in a fleet"""

	def __init__(self, ai_settings, screen):
		#Initialize alien and its starting position
		super(Alien, self).__init__()
		self.ai_settings = ai_settings
		self.screen = screen

		#Load the image and set its rect attribute
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		#Start new alien at  top left of screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Store alien's exact position
		self.x = float(self.rect.x)

	def update(self):
		"""Move alien to right"""
		self.x += (self.ai_settings.alien_speed * self.ai_settings.fleet_direction)
		self.rect.x = self.x

	def blitme(self):
		#Draw alien at current location
		self.screen.blit(self.image, self.rect)

	def check_edges(self):
		"""Return True if alien hits edge"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True
