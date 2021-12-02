from gui_puzzle import N_SIZES
from common import PuzzleError


def load_puzzle(args) -> tuple:
	size = -1
	array = []
	try:
		with open(args.filename, 'r') as f:
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
		raise PuzzleError(msg=f"can't open file: {args.filename}")
	if args.v and size not in N_SIZES:
		raise PuzzleError(msg=f'GUI support only {N_SIZES} sizes')
	check = [n < size * size and n >= 0 for n in array]
	if size < 1 or len(array) != size ** 2 or False in check or len(array) != len(set(array)):
		raise PuzzleError(msg='invalid puzzle input')
	goal = make_goal(size)
	return size, array, goal


def is_solvable(start : list, goal : list, size : int):
	res = 0
	for i in range(size * size):
		vi = start[i]
		for j in range(i, size * size):
			vj = start[j]
			if goal.index(vi) > goal.index(vj):
				res += 1
	start_x = start.index(0) % size
	start_y = start.index(0) // size
	goal_x = goal.index(0) % size
	goal_y = goal.index(0) // size
	h = abs(start_x - goal_x) + abs(start_y - goal_y)
	if (res + h) & 1:
		raise PuzzleError(msg="Puzzle not solvable")


def make_goal(size):
	arr = [[0] * size for _ in range(size)]
	dx, dy = [0, 1, 0, -1], [1, 0, -1, 0]
	x, y, c = 0, -1, 1
	for i in range(size + size - 1):
		for _ in range((size + size - i) // 2):
			x += dx[i % 4]
			y += dy[i % 4]
			arr[x][y] = c
			c += 1
	res = []
	for k in arr:
		res.extend(k)
	res[res.index(size * size)] = 0
	return res
