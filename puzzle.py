from collections import deque

class PriorityQueue():
	def __init__(self):
		self.elements = deque()
	
	def empty(self):
		return len(self.elements) == 0

	def put(self, node):
		self.elements.append(node)
		self.elements = deque(sorted(self.elements))
	
	def get(self):
		return self.elements.popleft()


class Board():
	def __init__(self, new_board, new_parent=None, new_action=None):
		self.board = self.copy_board(new_board) # Копирование игрового поля
		self.size = len(self.board) # размер
		self.parent = new_parent
		self.action = False
		self.h = 0
		self.g = 0 if not new_parent else new_parent.g + 1
		self.zero_x = -1 if not new_parent else new_parent.zero_x # координата пустой клетки по x
		self.zero_y = -1 if not new_parent else new_parent.zero_y # координата пустой клетки по y
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

	# Возвращаем игровое поле как новый объект
	def copy_board(self, copy_board):
		new_copy = []
		for row in copy_board:
			new_copy.append(list(row))
		return new_copy
	
	def heuristic(self, x1, y1, x2, y2):
		return abs(x1 - x2) + abs(y1 - y2)

	def calculate_h(self):
		for i in range(self.size):
			for j in range(self.size):
				if (self.board[i][j] != i * self.size + j + 1) and (self.board[i][j] != 0):
					self.h += self.heuristic(j, i, (self.board[i][j] - 1) % 3, (self.board[i][j] - 1) // 3)
		# if self.board[self.size - 1][self.size - 1] != 0:
		# 	self.h += 1

	def find_zero(self,):
		if self.zero_x < 0 or self.zero_y < 0:
			for i in range(self.size):
				for j in range(self.size):
					if not self.board[i][j]:
						self.zero_x = j
						self.zero_y = i
	
	def do_action(self, action):
		board = self.board
		x, y = self.zero_x, self.zero_y
		if action == 'right' and x < self.size - 1: # right
			board[y][x + 1], board[y][x] = board[y][x], board[y][x + 1]
			self.zero_x, self.zero_y = self.zero_x + 1, self.zero_y
			self.action = True
		elif action == 'left' and x > 0: # left
			board[y][x - 1], board[y][x] = board[y][x], board[y][x - 1]
			self.zero_x, self.zero_y = self.zero_x - 1, self.zero_y
			self.action = True
		elif action == 'up' and y > 0: # up
			board[y - 1][x], board[y][x] = board[y][x], board[y - 1][x]
			self.zero_x, self.zero_y = self.zero_x, self.zero_y - 1
			self.action = True
		elif action == 'down' and y < self.size - 1: # down
			board[y + 1][x], board[y][x] = board[y][x], board[y + 1][x]
			self.zero_x, self.zero_y = self.zero_x, self.zero_y + 1
			self.action = True
		return False

	def action_happen(self):
		return self.action

	def __eq__(self, eq_board) -> bool:
		return self.board == eq_board

	def __str__(self) -> str:
		return '\n'.join(map(str, self.board)) + f'\tg = {self.g}, h = {self.h}, f = {self.get_f()}'
	
	def __lt__(self, eq_board):
		return self.get_f() < eq_board.get_f()


def print_queue(nodes, text):
	print('[', text, *[node.get_f() for node in nodes], ']', sep=' ')

def solver(start):
	queue = PriorityQueue()
	closed = []
	neighbors = []
	path = []
	her = []
	queue.put(start)
	print(start) # Печать первой ноды
	while not queue.empty():
		current_node = queue.get()
		print(current_node)
		# Если решение найдено - завершить цикл
		if current_node.get_h() == 0:
			print('end:', current_node)
			break
		
		# Передвижения в 4 стороны
		for action in ('right', 'left', 'up', 'down'):
			node = Board(current_node.get_board(), current_node, action)
			if node not in closed and node.action_happen():
				neighbors.append(node)
		neighbors = sorted(neighbors)

		#neighbors = sorted(neighbors, key=lambda n : n.get_f())
		if len(neighbors) > 0:
			#queue.put(neighbors[0])
			neighbors.clear() # очистка ноды
			path.append(current_node)
		closed.append(current_node)
		
		input()
		#her.append(current_node.get_h())
	
	#print("len:", len(queue))

	# Просто сортируем путь по эвристике
	#her = sorted(path, key=lambda n : n.get_h())
	# print('PATH:')
	# for p in path:
	# 	print(p)
	# 	print()

	#print('d', her[0])

		
if __name__ == "__main__":
	
	board1 = [
			[1, 2, 4, 0],
			[12, 13, 3, 5],
			[11, 9, 14, 6],
			[10, 8, 15, 7]
			]
	board = [
			[1, 2, 7],
			[3, 4, 6],
			[0, 8, 5]
			]
	solver(Board(board))
	