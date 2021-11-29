import os

from pygame.image import load
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame as pg
#from time import sleep
from parser import PuzzleError

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
FPS = 30
SPEED = 5

N_SIZES = (3, 4, 5, 6, 7)
TILES = (180, 140, 110, 100, 90)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_IMG = 'resources/bg_2.jpg'
LOGO = 'resources/logo.png'
BG_TILE_IMG = 'resources/quad_5_r.png'
FONT = 'arial'


class GuiPuzzle():
	screen = None
	bg = None
	logo = None
	bg_tile = None
	tile = 0
	font_size = 0
	start_x = 0
	start_y = 0
	w = 0

	path = []
	current_state = None
	step = 0

	def _init_gui(self, path : list, w : int):
		pg.init()
		if w not in (N_SIZES):
			raise PuzzleError(msg=f'GUI support only {N_SIZES} sizes')
		self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pg.display.set_caption("N-puzzle")
		self.w = w
		self.path = path
		self.tile = TILES[N_SIZES.index(self.w)]
		self.font_size = self.tile // 2
		self.start_x = (SCREEN_WIDTH - ((self.tile - 5) * self.w + (self.w - 1) * 5)) // 2
		self.start_y = int((SCREEN_HEIGHT - ((self.tile - 5) * self.w + (self.w - 1) * 5)) // 1.6)
		#self.font = font = pg.font.SysFont(FONT, self.font_size)
		self.logo = pg.image.load(LOGO)
		self.logo = pg.transform.scale(self.logo, (self.logo.get_width() // 3.1, self.logo.get_height() // 3.1))
		self.bg = pg.image.load(BG_IMG)
		self.bg = pg.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.bg_tile = pg.image.load(BG_TILE_IMG)
		self.bg_tile = pg.transform.scale(self.bg_tile, (self.tile - 5, self.tile - 5))

	def run(self, path, w):
		self._init_gui(path, w)
		clock = pg.time.Clock()
		running = True
		while running:
			clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				elif event.type == pg.KEYDOWN:
					keys = pg.key.get_pressed()
					if event.key == pg.K_RIGHT and keys[pg.K_RIGHT]:
						if self.step < len(path) - 1:
							self.step += 1
					elif event.key == pg.K_LEFT and keys[pg.K_LEFT]:
						if self.step > 0:
							self.step -= 1
					elif keys[pg.K_ESCAPE]:
						running = False
			self.current_state = self.path[self.step].state
			self._updateWin()
		pg.quit()

	def _get_rect(self, x, y):
		return x * self.tile + self.start_x, y * self.tile + self.start_y, self.tile - 5, self.tile - 5

	def _draw_text(self, text, fname, fsize, color, rect : tuple):
		font = pg.font.SysFont(fname, fsize)
		#if fsize == 90: print(font.get_height(), font.get_linesize()) # TMP
		text_surface = font.render(text, True, pg.Color(color))
		self.screen.blit(text_surface, rect)

	def _get_click_mouse_pos(self):
		x, y = pg.mouse.get_pos()
		grid_x, grid_y = (x - self.start_x) // self.tile, (y - self.start_y) // self.tile
		click = pg.mouse.get_pressed()
		if grid_x < 0 or grid_x > self.w - 1 or grid_y > self.w - 1 or grid_y < 0:
			return False
		return (grid_x, grid_y) if click[0] else False

	def _updateWin(self):
		self.screen.blit(self.bg, (0, 0))
		self.screen.blit(self.logo, (SCREEN_WIDTH // 2 - self.logo.get_width() // 2, SCREEN_HEIGHT * 0.01))
		#self._draw_text('N-Puzzle',
			#'arial', 90, 'black', (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT * 0.0001))
		self._draw_text(f'{self.step} / {len(self.path) - 1}',
			'times new roman', 30, 'red', (SCREEN_WIDTH * 0.02, SCREEN_HEIGHT * 0.9)) # off in free mode
		[[self.screen.blit(self.bg_tile, self._get_rect(x, y)) for x in range(self.w)] for y in range(self.w)]
		[[pg.draw.rect(self.screen, pg.Color('black'), self._get_rect(x, y), 5, border_radius=self.tile // 10) 
			for x in range(self.w)] for y in range(self.w)]

		for n, value in enumerate(self.current_state):
			if value:
				x, y, w, h = self._get_rect(n % self.w, n // self.w)
				x = x + self.tile // 3 if value < 10 else x + self.tile // 5
				if value:
					self._draw_text(
						str(value), 
						'arial', 
						self.font_size, 
						'black', 
						(x, y + self.tile // 5, w, h))
					
		pos = self._get_click_mouse_pos()
		if pos:
			s = pg.Surface((self.tile - 15, self.tile - 15))
			s.set_alpha(180)
			s.fill(BLACK)
			#pg.draw.rect(screen, pg.Color('black'), get_rect(pos[0], pos[1]), border_radius=TILE//10)
			x, y, w, h = self._get_rect(pos[0], pos[1])
			self.screen.blit(s, (x + 5, y + 5, w, h))
		pg.display.flip()
