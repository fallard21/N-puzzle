from collections import deque

row = 0
col = 0

class Board():
	def __init__(self, new_board, new_parent=None, new_action=None):
		self.board = new_board
		self.parent = new_parent
		self.action = new_action
		self.h = 0
		self.g = 0 if not self.parent else self.parent.g + 1
		self.f = 0
		self.zero_x = 0 # ?
		self.zero_y = 0 # ?

		for i in range(row):
			for j in range(col):
				if (self.board[i][j] != i * row + j+ 1) and (self.board[i][j] != 0):
					self.h += 1
				if not self.board[i][j]: # ?
					self.zero_x = i # ?
					self.zero_y = j # ?
		self.f = self.g + self.h

	def get_h(self):
		return self.h

	def get_g(self):
		return self.g
	
	def get_f(self):
		return self.f

	def get_zero(self) -> tuple:
		return (self.zero_y, self.zero_x)

	def print_board(self):
		for row in self.board:
			print(*row)

	def do_action(self, action):
		if action == 'right':
			pass
		elif action == 'left':
			pass
		elif action == 'up':
			pass
		elif action == 'down':
			pass

	def print_stats(self):
		self.print_board()
		print('\n\033[31m=================\033[0m')
		print("h =", self.h)
		print("g =", self.g)
		print("h =", self.h)
		print("f =", self.f)
		print("zero_x =", self.zero_x)
		print("zero_y =", self.zero_y)
		print(f"row = {row}, col = {col}")
		print('parent =', self.parent)
		print('\033[31m=================\033[0m')

	def __eq__(self, eq_board) -> bool:
		return self.board == eq_board

	def __str__(self) -> str:
		return '\n'.join(map(str, self.board)) + f'\th = {self.h}, f = {self.f}'

if __name__ == "__main__":
	queue = deque()
	opened = []
	closed = []
	board = [
			[1, 2, 7],
			[3, 4, 6],
			[0, 8, 5]
			]
	row = 3
	col = 3
	node = Board(board)
	queue.append(node)
	
	while len(queue) > 0:
		current_node = queue.pop()
		# print(current_node)
		if current_node.get_h() == 0:
			break
		# print(current_node.get_zero())
		zero = current_node.get_zero()
		if zero[1] > 0: # Сдвиг пустышки влево
			pass
		if zero[1] < row - 1: # Сдвиг пустышки вправо
			pass
		if zero[0] > 0: # Сдвиг пустышки вверх
			pass
		if zero[0] < col - 1: # Сдвиг пустышки вниз
			pass
