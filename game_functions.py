import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	#Key press down
		if event.key == pygame.K_RIGHT:
			#Move ship to right
			ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			#Move ship to left
			ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			#Create new bullet and add to bullet group
			fire_bullet(ai_settings, screen, ship, bullets)
		elif event.key == pygame.K_q:
			sys.exit()
			

def check_keyup_events(event, ship):
	#Key press release
		if event.key == pygame.K_RIGHT:
			ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	"""Responds to keyboard/mouse"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	"""Start game when press Play"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:

		#Hide mouse cursor
		pygame.mouse.set_visible(False)

		#Reset game stats
		stats.reset_stats()
		ai_settings.initialize_dynamic_settings()
		stats.game_active = True

		#Reset scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		#Remove aliens and bullets
		aliens.empty()
		bullets.empty()

		#Create new fleet, center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	else:
		pygame.mouse.set_visible(True)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""Updates images on screen and goes to new screen"""
	#Redraw screen after every loop
	screen.fill(ai_settings.bg_color)

	#Draw score info
	sb.show_score()

	#Redraw all bullets behind ships/aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	#Redraw ship and all aliens
	ship.blitme()
	aliens.draw(screen)

	#Draw play button if game inactive
	if not stats.game_active:
		play_button.draw_button()

	#Make most recent screen visible
	pygame.display.flip()

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine number of aliens fit in 1 row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine number of rows of aliens fit on screen"""
	availabe_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(availabe_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create fleet of aliens"""
	#Create an alien and find how many can fit in 1 row
	#Spacing between alien is 1 alien_width. Therefore fitting 1 alien requires 2 * alien_width
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

	#Create first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			#Create an alien and place it in the row
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to ship being hit by alien"""
	if stats.ships_left > 0:
		stats.ships_left -= 1

		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		#Create a new fleet and center the ship position
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		#Remove ship lives
		sb.prep_ships()

		#Pause
		sleep(0.5)
	else:
		stats.game_active = False

def check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Check if any aliens reach bottom of screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
	"""
	Check if fleet is at an edge
	Update all positions of aliens in fleet 

	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	#Look for ship/alien collision
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

	#Look for alien/bottom collision
	check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Updates position of bullets, gets rid of old bullets"""
	#Get rid of bullets past top screen
	for bullet in bullets.copy():
		if bullet.rect.bottom <= sb.level_rect.top + 15:
			bullets.remove(bullet)
	#Destroy existing bullets and create new fleet
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)

		#Increase level
		stats.level += 1
		sb.prep_level()

	check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to bullet/alien collision"""
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)

def fire_bullet(ai_settings, screen, ship, bullets):
	#Create new bullet and add to bullet group
	if len(bullets) < ai_settings.bullets_allowed:	
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def check_fleet_edges(ai_settings, aliens):
	"""Respond if alien hits edges"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Drop entire fleet and change the direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_high_score(stats, sb):
	"""Check if new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

