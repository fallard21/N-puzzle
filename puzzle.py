from collections import deque

class Board():
	def __init__(self, new_board, new_parent=None, new_action=None):
		self.board = self.copy_board(new_board) # Копирование игрового поля
		self.height = len(self.board) # высота
		self.width = len(self.board[0]) # ширина
		self.parent = new_parent
		# self.action = new_action
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
		return self.h

	# def get_g(self):
	# 	return self.g
	
	def get_f(self):
		return self.g + self.h

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

	def calculate_h(self):
		for i in range(self.height):
			for j in range(self.width):
				if (self.board[i][j] != i * self.height + j + 1) and (self.board[i][j] != 0):
					self.h += 1
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


	# def print_stats(self):
	# 	self.print_board()
	# 	print('\n\033[31m=================\033[0m')
	# 	print("h =", self.h)
	# 	print("g =", self.g)
	# 	print("h =", self.h)
	# 	print("f =", self.f)
	# 	print("zero_x =", self.zero_x)
	# 	print("zero_y =", self.zero_y)
	# 	print(f"row = {row}, col = {col}")
	# 	print('parent =', self.parent)
	# 	print('\033[31m=================\033[0m')

	def __eq__(self, eq_board) -> bool:
		return self.board == eq_board

	def __str__(self) -> str:
		return '\n'.join(map(str, self.board)) + f'\tg = {self.g}, h = {self.h}, f = {self.get_f()}'

def get_best_f(nodes : list):
	min_node = nodes[0]
	min = nodes[0].get_f()
	for node in nodes:
		if node.get_f() < min:
			min_node = node
			min = node.get_f()
	return min_node

def solver(board):
	queue = deque()
	closed = []
	opened = []
	queue.append(Board(board))
	while len(queue) > 0:
		current_node = queue.pop()
		# print(current_node)
		if current_node.get_h() == 0:
			break
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
		

		print(current_node, end='\n\n')
		for o in opened:
			print(o)
			print()
		print('======================')
		
		
		best_node = get_best_f(opened) # Поиск эффективной ноды
		queue.append(best_node) # Добавил в очередь эффективную ноду
		closed.append(current_node) # добавил текущую ноду
		closed.append(opened) # добавил плохие ноды
		opened.clear() # очистка ноды
		input()
	

		
if __name__ == "__main__":
	
	board = [
			[1, 2, 7],
			[3, 4, 6],
			[0, 8, 5]
			]
	solver(board)
	