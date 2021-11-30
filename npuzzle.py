from heapq import *
from math import sqrt
from sys import exit
from parser import PuzzleError, load_puzzle, is_solvable
from argparse import ArgumentParser
from gui_puzzle import *

tgoal = None ## TEMP TO DELETE

class Node():
	def __init__(self, new_state):
		self.state = tuple(new_state)
		self.size = len(self.state)
		self.w = int(sqrt(self.size))
		self.h = manhattan(self.state, tgoal, self.w)
		self.g = 0
		self.f = self.g + self.h
		#self.parent = 0

	def __repr__(self) -> str:
		return str(self.state)

	def __str__(self) -> str:
		s = ''
		for i in range(self.size):
			if i % self.w == 0 and i != 0:
				s += '\n'
			s += '%-3d' % self.state[i]
		return s + '\n'

	def __lt__(self, eq : 'Node'):
	 	return self.f < eq.f

	def __hash__(self) -> int:
		return hash(self.state)

	def __eq__(self, eq : 'Node') -> bool:
		return self.state == eq.state

	def neighbors(self):
		neighbors = []
		zero = self.state.index(0)
		moves = [-1,		# left   [-1]
				-self.w,		# up     [-3]
				1,			# right   [1]
				self.w]		# down     [3]

		for m in moves:
			pos = zero + m
			if ((pos % self.w > zero % self.w and pos // self.w < zero // self.w) or
				(pos % self.w < zero % self.w and pos // self.w > zero // self.w) or
				(pos < 0) or
				(pos > self.size - 1)):
				continue
			state = list(self.state)
			state[pos], state[zero] = state[zero], state[pos]
			node = Node(state)
			node.g = self.g + 1
			#node.parent = self
			neighbors.append(node)
		return neighbors


class PuzzleSolver():
	def __init__(self, start, goal):
		self.queue = []
		self.start = Node(start)
		self.goal = Node(goal)
		self.closed = {self.start : None}

	def run_Astar(self):
		#self.start.h = manhattan(self.start.state, self.goal.state, self.start.w)
		heappush(self.queue, self.start)
		while self.queue:
			current_node = heappop(self.queue)
			if current_node == self.goal:
				print('SOLVED') # TMP
				break
			next_nodes = current_node.neighbors()
			for node in next_nodes:
				if node not in self.closed:
					#node.h = manhattan(node.state, self.goal.state, node.w)
					heappush(self.queue, node)
					self.closed[node] = current_node

	def get_path(self):
		path = []
		cur_node = self.goal
		path.append(self.goal)
		#print(self.goal)
		while cur_node != self.start:
			cur_node = self.closed[cur_node]
			#print(cur_node)
			path.append(cur_node)
		return path[::-1]


def manhattan(state : list, goal : list, size):
	h = 0
	for i in range(size * size):
		if state[i] and state[i] != goal[i]:
			k = goal.index(state[i])
			#gx, gy = k % size, k // size
			#x, y = k % size, k // size
			h += abs(i % size - k % size) + abs(i % size - k // size)
	return h


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


if __name__ == "__main__":
	parser = ArgumentParser()

	parser.add_argument("filename", type=str, help="File with puzzle")
	parser.add_argument("-heruistic", type=int, default=1, 
		help="Select heuristic (1 - manhattan, 2 - text1, 3 - text2)")
	parser.add_argument("-v", action='store_true', help="Run program with GUI")
	args = parser.parse_args()


	tgoal = make_goal(4) # NEED FIX THAT !!
	try:
		
		size, start = load_puzzle(args.filename)
		goal = make_goal(size)
		is_solvable(start, goal, size)
	except PuzzleError as pe:
		print(pe.err_msg)
		exit()

	solver = PuzzleSolver(start, goal)
	solver.run_Astar()
	path = solver.get_path()

	if args.v:
		gui = GuiPuzzle()
		gui.run(path, int(sqrt(len(start))))

	# game(path, start, int(sqrt(len(start))))

# Если -u и size - нечетное -> РЕШАЕТСЯ
# Если -s и size - четное -> НЕ РЕШАЕТСЯ