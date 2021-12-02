from heapq import heappop, heappush
from math import sqrt
from heruistics import *

class PuzzleError(Exception):
	err_msg = ""

	def __init__(self, msg):
		self.err_msg = f"Error: {msg}"


class Node():
	def __init__(self, new_state):
		self.state = tuple(new_state)
		self.size = len(self.state)
		self.w = int(sqrt(self.size))
		self.h = 0
		self.g = 0
		self.f = self.g + self.h

	def set_h(self, goal):
		self.h = manhattan(self.state, goal, self.w)
		self.f = self.g + self.h

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

	def neighbors(self, goal):
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
			node.set_h(goal)
			node.g = self.g + 1
			neighbors.append(node)
		return neighbors


class PuzzleSolver():
	def __init__(self, start, goal):
		self.queue = []
		self.start = Node(start)
		self.goal = Node(goal)
		self.closed = {self.start : None}

	def run_Astar(self):
		#self.start.set_h(self.goal.state)
		heappush(self.queue, self.start)
		while self.queue:
			current_node = heappop(self.queue)
			if current_node == self.goal:
				print('SOLVED') # TMP
				break
			next_nodes = current_node.neighbors(self.goal.state)
			for node in next_nodes:
				if node not in self.closed:
					heappush(self.queue, node)
					self.closed[node] = current_node
			#print([q.f for q in self.queue])
			#input()

	def get_path(self):
		path = []
		cur_node = self.goal
		path.append(self.goal)
		while cur_node != self.start:
			cur_node = self.closed[cur_node]
			path.append(cur_node)
		return path[::-1]
