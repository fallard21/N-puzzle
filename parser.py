class PuzzleError(Exception):
	err_msg = ""

	def __init__(self, msg):
		self.err_msg = f"Error: {msg}"


def load_puzzle(filename : str) -> tuple:
	size = -1
	array = []
	try:
		with open(filename, 'r') as f:
			for line in f:
				line = line.strip(' \n').partition('#')
				split_line = line[0].split()
				try:
					if len(split_line) == 1 and split_line[0].isdigit() and size < 0:
						size = int(split_line[0])
					elif len(split_line) == size:
						array.extend(list(map(int, split_line)))
					elif len(split_line) > 0:
						raise PuzzleError(msg='invalid puzzle input')
				except ValueError:
					raise PuzzleError(msg='invalid puzzle input')
	except OSError:
		raise PuzzleError(msg=f"can't open file: {filename}")
	check = [n < size * size and n >= 0 for n in array]
	if size < 1 or len(array) != size ** 2 or False in check or len(array) != len(set(array)):
		raise PuzzleError(msg='invalid puzzle input')
	return size, array


def is_solvable(start : list, goal : list, size : int):
	res = 0
	for i in range(size * size):
		vi = start[i]
		for j in range(i, size * size):
			vj = start[j]
			if goal.index(vi) > goal.index(vj):
				res += 1
	#w = int(sqrt(size))
	start_x = start.index(0) % size
	start_y = start.index(0) // size
	goal_x = goal.index(0) % size
	goal_y = goal.index(0) // size
	h = abs(start_x - goal_x) + abs(start_y - goal_y)
	#print('2 res:', res, ' h:', h)
	if (res + h) & 1:
		raise PuzzleError(msg="Puzzle not solvable")
