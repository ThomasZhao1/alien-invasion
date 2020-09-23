import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
	#Initializes pygame, settings, screen
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	#Make button
	play_button = Button(ai_settings, screen, "Play")

	#Initialize stats and score
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	#Make a ship
	ship = Ship(ai_settings, screen)

	#Make a group for aliens and bullets
	aliens = Group()
	bullets = Group()

	#Create alien fleet
	gf.create_fleet(ai_settings, screen, ship, aliens)

	#Start main loop for game
	while True:
		#Check these conditions only if game is active
		if stats.game_active:
			bullets.update()
			ship.update()
			gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
		#Check these conditions all the time
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

		
run_game()
