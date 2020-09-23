import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	"""Fires bullet from Ship"""

	def __init__(self, ai_settings, screen, ship):
		"""Create a bullet at ship position"""
		super(Bullet, self).__init__()
		self.screen = screen

		#Create a bullet rect at (0,0), then set to correct position
		self.rect = pygame.Rect(0,0, ai_settings.bullet_width, ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		#Store bullet position (y-coordinate) as decimal
		self.y = float(self.rect.y)

		self.color = ai_settings.bullet_color
		self.bullet_speed = ai_settings.bullet_speed

	def update(self):
		"""Move bullet up screen"""
		
		#Update self.y
		self.y -= self.bullet_speed

		#Update rect position
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw bullets to screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)

