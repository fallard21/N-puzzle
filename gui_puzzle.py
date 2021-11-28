import pygame as pg
from time import sleep

SCREEN = 0
BG = 0
BG_TILE = 0
N = 0
TILE = 0
FONT_SIZE = 0


START_X = 0
START_Y = 0

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

N_SIZES = (3, 4, 5, 6, 7)
TILES = (180, 150, 120, 100, 90)


SPEED = 5

BG_IMG = 'resources/bg_2.jpg'
BG_TILE_IMG = 'resources/quad_5_r.png'
FONT = 'arial'


def init_pygame(size : int):
	pg.init()

	global SCREEN
	global BG
	global BG_TILE
	global TILE
	global N
	global FONT_SIZE
	global START_X
	global START_Y 

	SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pg.display.set_caption("n-puzzle")
	
	N = size
	TILE = TILES[N_SIZES.index(size)]
	FONT_SIZE = TILE // 2

	START_X = (SCREEN_WIDTH - ((TILE - 5) * N + (N - 1) * 5)) // 2
	START_Y = int((SCREEN_HEIGHT - ((TILE - 5) * N + (N - 1) * 5)) // 1.4)

	BG = pg.image.load(BG_IMG)
	BG = pg.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
	BG_TILE = pg.image.load(BG_TILE_IMG)
	BG_TILE = pg.transform.scale(BG_TILE, (TILE - 5, TILE - 5))
	#font = pg.font.SysFont(FONT, FONT_SIZE)


def get_rect(x, y):
	return x * TILE + START_X, y * TILE + START_Y, TILE - 5, TILE - 5


def draw_text(text, font_name, font_size, color, rect : tuple):
	font = pg.font.SysFont(font_name, font_size)
	f = font.render(text, True, pg.Color(color))
	SCREEN.blit(f, rect)


def get_click_mouse_pos():
	x, y = pg.mouse.get_pos()
	grid_x, grid_y = (x - START_X) // TILE, (y - START_Y) // TILE
	print((grid_x, grid_y), START_X, START_Y)
	#pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
	click = pg.mouse.get_pressed()
	print(x, y)
	if grid_x < 0 or grid_x > N - 1 or grid_y > N - 1 or grid_y < 0:
		return False
	return (grid_x, grid_y) if click[0] else False


def updateWin():
	SCREEN.blit(BG, (0, 0))

	draw_text('N-Puzzle', 'arial', 90, 'black', (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT * 0.0001))
	
	[[SCREEN.blit(BG_TILE, get_rect(x, y)) for x in range(N)] for y in range(N)]
	[[pg.draw.rect(SCREEN, pg.Color('black'), get_rect(x, y), 5, border_radius=TILE // 10) for x in range(N)] for y in range(N)]

	for n in range(N * N):
		if n:
			x, y, w, h = get_rect(n % N, n // N)
			if n < 10:
				draw_text(str(n), 'arial', FONT_SIZE, 'black', (x + TILE // 3, y + TILE // 5, w, h))
			else:
				draw_text(str(n), 'arial', FONT_SIZE, 'black', (x + TILE // 5, y + TILE // 5, w, h))

	pos = get_click_mouse_pos()
	if pos:
		s = pg.Surface((TILE - 15, TILE - 15))
		s.set_alpha(180)
		s.fill(BLACK)
		#pg.draw.rect(screen, pg.Color('black'), get_rect(pos[0], pos[1]), border_radius=TILE//10)
		x, y, w, h = get_rect(pos[0], pos[1])
		SCREEN.blit(s, (x + 5, y + 5, w, h))
	pg.display.flip()


def game():
	init_pygame(4)
	clock = pg.time.Clock()
	running = True
	while running:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
		keys = pg.key.get_pressed()
		if keys[pg.K_ESCAPE]:
			running = False
		
		updateWin()

	pg.quit()

