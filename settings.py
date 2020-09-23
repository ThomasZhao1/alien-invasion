class Settings():
	#Stores all settings for Alien Invasion

	def __init__(self):
		"""Initialize settings"""

		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)

		#Ship settings
		self.ship_limit = 3

		#Alien settings
		self.fleet_drop_speed = 10
		self.speedup_scale = 1.1
		self.score_scale = 1.5


		#Bullet settings
		self.bullet_width = 800
		self.bullet_height = 15
		self.bullet_color = (138,43,226)
		self.bullets_allowed = 10

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed = 40
		self.bullet_speed = 60
		self.alien_speed = 20

		 #fleet_direction 1 = right, -1 = left
		self.fleet_direction = 1

		#Scoring
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed and point values"""
		self.ship_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
