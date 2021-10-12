from collections import deque

class Board():
	def __init__(self, new_board, new_parent=None, new_action=None):
		self.board = self.copy_board(new_board) # Копирование игрового поля
		self.height = len(self.board) # высота
		self.width = len(self.board[0]) # ширина
		self.parent = new_parent
		# self.action = new_action
		self.heuristic = 0
		self.h = 0
		self.g = 0 if not new_parent else new_parent.g + 1
		self.zero_x = -1 if not new_parent else new_parent.zero_x # координата пустой клетки по x
		self.zero_y = -1 if not new_parent else new_parent.zero_y # координата пустой клетки по y
		if not new_parent:
			self.find_zero()
		self.do_action(new_action)
		self.calculate_h()

	def get_board(self):
		return self.board

	def get_board_sizes(self) -> tuple:
		return (self.width, self.height)

	def get_h(self):
		return self.heuristic
	

	# def get_g(self):
	# 	return self.g
	
	def get_f(self):
		return self.g + self.heuristic #+ self.h

	def get_zero_x(self):
		return self.zero_x

	def get_zero_y(self):
		return self.zero_y

	def get_zero_coords(self) -> tuple:
		return (self.zero_x, self.zero_y)

	# Возвращаем игровое поле как новый объект
	def copy_board(self, copy_board):
		new_copy = []
		for row in copy_board:
			new_copy.append(list(row))
		return new_copy
	
	def heuristical(self, x1, y1, x2, y2):
		return abs(x1 - x2) + abs(y1 - y2)

	def calculate_h(self):
		for i in range(self.height):
			for j in range(self.width):
				if (self.board[i][j] != i * self.height + j + 1) and (self.board[i][j] != 0):
					self.h += 1 # ?
					self.heuristic += self.heuristical(j, i, (self.board[i][j] - 1) % 3, (self.board[i][j] - 1) // 3)
		if self.board[self.height - 1][self.width - 1] != 0:
			self.h += 1

	

	def find_zero(self,):
		if self.zero_x < 0 or self.zero_y < 0:
			for i in range(self.height):
				for j in range(self.width):
					if not self.board[i][j]:
						self.zero_x = j
						self.zero_y = i
		
	def do_action(self, action):
		board = self.board
		x, y = self.zero_x, self.zero_y
		if action == 'right':
			board[y][x + 1], board[y][x] = board[y][x], board[y][x + 1]
			self.zero_x, self.zero_y = self.zero_x + 1, self.zero_y
		elif action == 'left':
			board[y][x - 1], board[y][x] = board[y][x], board[y][x - 1]
			self.zero_x, self.zero_y = self.zero_x - 1, self.zero_y
		elif action == 'up':
			board[y - 1][x], board[y][x] = board[y][x], board[y - 1][x]
			self.zero_x, self.zero_y = self.zero_x, self.zero_y - 1
		elif action == 'down':
			board[y + 1][x], board[y][x] = board[y][x], board[y + 1][x]
			self.zero_x, self.zero_y = self.zero_x, self.zero_y + 1

	def __eq__(self, eq_board) -> bool:
		return self.board == eq_board

	def __str__(self) -> str:
		return '\n'.join(map(str, self.board)) + f'\tg = {self.g}, her = {self.heuristic}, f = {self.get_f()}'


def print_queue(nodes, text):
	print('[', text, *[node.get_f() for node in nodes], ']', sep=' ')

def solver(board):
	queue = deque()
	closed = []
	opened = []
	path = []
	her = []
	queue.append(Board(board))
	while len(queue) > 0:
		#print_queue(queue, 'before sort:')
		queue = sorted(queue, key=lambda n: n.get_f())
		#print_queue(queue, 'after sort :')
		current_node = queue.pop()
		# print(current_node)
		if current_node.get_h() == 0:
			break
		
		# НИЖНИЙ КУСОК КОДА ВЫНЕСТИ В КЛАСС
		# for action in ('right', 'left', 'up', 'down'):
		# 	node = Board(current_node.get_board(), current_node, action)
		# 	if node not in closed:
		# 		opened.append(node)

		x, y = current_node.get_zero_coords()
		w, h = current_node.get_board_sizes()

		if x < w - 1: # Сдвиг вправо
			node = Board(current_node.get_board(), current_node, 'right')
			if node not in closed:
				opened.append(node)
		if x > 0: # Сдвиг влево
			node = Board(current_node.get_board(), current_node, 'left')
			if node not in closed:
				opened.append(node)
		if y > 0: # Сдвиг вверх
			node = Board(current_node.get_board(), current_node, 'up')
			if node not in closed:
				opened.append(node)
		if y < h - 1: # Сдвиг вниз
			node = Board(current_node.get_board(), current_node, 'down')
			if node not in closed:
				opened.append(node)
		
		#print('CURRENT\n', current_node, end='\n\n')
		# for o in opened:
		# 	print(o)
		# 	print()
		# print('======================')
		if len(path) == 0:
			path.append(current_node) # добавляем самую первую ноду
			print(current_node, '\n')
		opened = sorted(opened, key=lambda n: n.get_f())
		if len(opened) > 0:
			node = opened.pop(0)
			path.append(node) # добавляем в путь эффективную ноду
			queue.append(node) # добавляем в очередь близкую ноду
			#closed.append(opened) # добавил плохие ноды
			opened.clear() # очистка ноды
		closed.append(current_node)
		
		her.append(current_node.get_h())
	
	#print("len:", len(queue))

	# Просто сортируем путь по эвристике
	her = sorted(path, key=lambda n : n.get_h())
	# print('PATH:')
	# for p in path:
	# 	print(p)
	# 	print()
	# input()
	print(her[0])

		
if __name__ == "__main__":
	
	# board = [
	# 		[1, 2, 4, 0],
	# 		[12, 13, 3, 5],
	# 		[11, 9, 14, 6],
	# 		[10, 8, 15, 7]
	# 		]
	board = [
			[1, 2, 7],
			[3, 4, 6],
			[0, 8, 5]
			]
	solver(board)
	