from heapq import *
from math import sqrt


class Node():
	def __init__(self, new_state : list) -> None:
		self.state = tuple(new_state)
		self.h = 0
		self.g = 0
		#self.f = 0
		self.parent = 0
		self.size = len(self.state)
		self.w = int(sqrt(self.size))

	# def set_g(self, new_g):
	# 	self.g = new_g
	# 	self.f = self.g + self.h

	# def set_h(self, new_h):
	# 	self.h = manhattan(self.state, self.size, self.w)
	# 	self.f = self.g + self.h

	#def set_f(self, new_f):
	#	self.f = new_f

	def set_parent(self, new_parent):
		self.parent = new_parent

	def manhattan(self):
		arr = self.state
		w = self.w
		for i in range(self.size):
			if arr[i] != i + 1 and arr[i] != 0:
				self.h += abs(i % w - (arr[i] - 1) % w) + abs(i // w - (arr[i] - 1) // w)
		return self.h

	
	@property
	def f(self):
		return self.h + self.g

	def __repr__(self) -> str:
		return str(self.state)

	def __str__(self) -> str:
		#size = len(self.state)
		#w = int(sqrt(size))
		s = ''
		for i in range(size):
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
			neighbors.append(node)
		return neighbors


class Solver():
	def __init__(self) -> None:
		#self.size = len(board)
		#self.w = sqrt(board)
		self.queue = []

	def Astar(self, start : 'Node', goal : 'Node'):
		start.manhattan()
		heappush(self.queue, start)
		cost_visited = {start : 0}
		visited = {start : None}
		opened = []
		closed = []

		while self.queue:
			current = heappop(self.queue)
			if current == goal:
				print('SOLVED')
				break
			next_nodes = current.neighbors()
			for node in next_nodes:
				new_cost = 1 + cost_visited[current]
				if node not in visited or new_cost < cost_visited[node]:
					node.manhattan()
					heappush(self.queue, node)
					cost_visited[node] = new_cost
					visited[node] = current
		return visited


def manhattan(arr : list, size, w):
	h = 0
	size = len(arr)
	w = int(sqrt(arr))
	for i in range(size):
		if arr[i] != i + 1 and arr[i] != 0:
			h += abs(i % w - (arr[i] - 1) % w) + abs(i // w - (arr[i] - 1) // w)
	return h


def make_goal(size):
	arr = [i + 1 for i in range(size)]
	arr[-1] = 0
	return arr


def get_board() -> tuple:
	size = 0
	array = []
	with open('board.txt', 'r') as f:
		for line in f:
			if line[0] == '#':
				continue
			elif len(line.split()) == 1:
				size = int(line)
			else:
				array.extend(list(map(int, line.split())))
	return (size, array)


if __name__ == "__main__":
	size, board = get_board()
	board = [
			17, 16, 2, 6, 19,
			1, 0, 3, 18, 5,
			15, 24, 21, 7, 4,
			14, 23, 20, 9, 8,
			13, 12, 11, 22, 10
			]
	
	# board = [
	# 		1, 2, 4, 0,
	# 		12, 13, 3, 5,
	# 		11, 9, 14, 6,
	# 		10, 8, 15, 7
	# 		]
	
	# board = [
	# 		1, 2, 7, 
	# 		3, 4, 6, 
	# 		0, 8, 5
	# 		]

	
	goal = Node(make_goal(len(board)))
	start = Node(board)
	
	s = Solver()
	end = s.Astar(start, goal)
	
	#end = solver(start, goal, board)
	#print(len(end))
	# PATH
	# cur_node = goal
	# while cur_node != start:
	# 	cur_node = end[cur_node]
	# 	print(cur_node)
