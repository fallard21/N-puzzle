from heapq import *
from math import sqrt


class Node:
	def __init__(self, new_state : list):
		self.state = new_state.copy()
		self.h = 0
		self.f = 0

	def move_board(self, zero, move):
		self.state[zero], self.state[move] = self.state[move], self.state[zero]

	def get_heuristic(self):
		array = self.state
		size = len(array)
		w = int(sqrt(size))
		if not self.h:
			for i in range(size):
				if array[i] != i + 1 and array[i] != 0:
					self.h += heuristic((i % w, (board[i] - 1) % w), (i // w, (board[i] - 1) // w))
		return self.h

	def set_priority(self, new_f):
		self.f = new_f

	def get_state(self):
		return self.state

	def __eq__(self, eq) -> bool:
		return self.state == eq

	def __hash__(self) -> int:
		return hash(tuple(self.state))

	def __lt__(self, eq : 'Node'):
		return self.f < eq.f
	
	def __repr__(self) -> str:
		return str(self.state)
	
	def __str__(self) -> str:
		size = len(self.state)
		w = int(sqrt(size))
		s = ''
		for i in range(size):
			if i % w == 0 and i != 0:
				s += '\n'
			s += str(self.state[i]) + ' '
		return s + '\n'

class Solver:
	def __init__(self, start):
		#self.start = start
		self.size = len(start)
		self.width = int(sqrt(self.size))
		self.queue = []

	def Astar(self):
		pass
	
	def get_neighbors(self):
		pass


def heuristic(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


# board = [
# 1, 2, 7, 
# 3, 4, 6, 
# 0, 8, 5
# ]
def get_neighbors(node : 'Node', size, width):
	state = node.get_state()
	zero = state.index(0)
	neighbors = []
	moves = [-1,		# left   [-1]
			-width,		# up     [-3]
			1,			# right   [1]
			width]		# down     [3]

	for m in moves:
		pos = zero + m
		if ((pos % width > zero % width and pos // width < zero // width) or
			(pos % width < zero % width and pos // width > zero // width) or
			(pos < 0) or
			(pos > size - 1)):
			continue
		node = Node(state)
		node.move_board(zero, pos)
		neighbors.append((1, node))
	return neighbors



def solver(start, goal, board):
	size = len(board)
	width = int(sqrt(size))
	queue = []
	heappush(queue, (0, start))
	cost_visited = {start : 0}
	visited = {start : None}

	while queue:
		cur_node = heappop(queue)
		if cur_node[1] == goal:
			print('SOLVED:')
			print(cur_node[1])
			break
			
		next_nodes = get_neighbors(cur_node[1], size, width)
		for next_node in next_nodes:
			neigh_cost, neigh_node = next_node
			new_cost = neigh_cost + cost_visited[cur_node[1]]
			if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
				priority = new_cost + neigh_node.get_heuristic()
				neigh_node.set_priority(priority)
				heappush(queue, (priority, neigh_node))
				cost_visited[neigh_node] = new_cost
				visited[neigh_node] = cur_node[1]
	
	return visited



def make_goal(size):
	arr = [i + 1 for i in range(size)]
	arr[-1] = 0
	return arr


if __name__ == "__main__":
	
	board = [
			1, 2, 4, 0,
			12, 13, 3, 5,
			11, 9, 14, 6,
			10, 8, 15, 7
			]
	
	
	# board = [
	# 		1, 2, 7, 
	# 		3, 4, 6, 
	# 		0, 8, 5
	# 		]

	
	goal = Node(make_goal(len(board)))
	start = Node(board)
	end = solver(start, goal, board)
	
	# PATH
	cur_node = goal
	while cur_node != start:
		cur_node = end[cur_node]
		print(cur_node)
