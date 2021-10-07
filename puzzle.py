row = 0
col = 0

class Board():
	def __init__(self, new_board, new_parent=None):
		self.board = new_board
		self.parent = new_parent
		self.h = 0
		self.g = 0 if not new_parent else self.parent.g + 1
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
				
	def print_board(self):
		for row in self.board:
			print(*row)

	def print_stats(self):
		self.print_board()
		print("\nh =", self.h)
		print("g =", self.g)
		print("h =", self.h)
		print("f =", self.f)
		print("zero_x =", self.zero_x)
		print("zero_y =", self.zero_y)
		print(f"row = {row}, col = {col}")
		print('parent =', self.parent)

if __name__ == "__main__":
	board = [[1, 2, 7],
			[3, 4, 6],
			[0, 8, 5]]
	row = 3
	col = 3
	kek = Board(board)
	kek.print_stats()
