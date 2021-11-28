from heapq import *
from math import sqrt
from sys import exit
from parser import get_board
from argparse import ArgumentParser
from gui_puzzle import *

class Node():
	def __init__(self, new_state):
		self.state = tuple(new_state)
		self.size = len(self.state)
		self.w = int(sqrt(self.size))
		self.h = manhattan(self.state, self.size, self.w)
		self.g = 0
		self.f = self.g + self.h
		self.parent = 0

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
			node.parent = self
			neighbors.append(node)
		return neighbors


class Solver():
	def __init__(self, start, goal):
		self.queue = []
		self.start = Node(start)
		self.goal = Node(goal)
		self.closed = {self.start : None}

	def Astar(self):
		heappush(self.queue, self.start)
		while self.queue:
			current_node = heappop(self.queue)
			if current_node == self.goal:
				print('SOLVED')
				break
			next_nodes = current_node.neighbors()
			for node in next_nodes:
				if node not in self.closed:
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


def manhattan(arr : list, size, w):
	h = 0
	for i in range(size):
		if arr[i] != i + 1 and arr[i] != 0:
			h += abs(i % w - (arr[i] - 1) % w) + abs(i // w - (arr[i] - 1) // w)
	return h


def make_goal(size):
	arr = [i + 1 for i in range(size)]
	arr[-1] = 0
	return arr


def is_solvable(start : list, goal : list, size : int):
	res = 0
	for i in range(size):
		vi = start[i]
		for j in range(i, size):
			vj = start[j]
			if goal.index(vi) > goal.index(vj):
				res += 1
	
	w = int(sqrt(size))
	start_x = start.index(0) % w
	start_y = start.index(0) // w
	goal_x = goal.index(0) % w
	goal_y = goal.index(0) // w
	h = abs(start_x - goal_x) + abs(start_y - goal_y)
	#print('2 res:', res, ' h:', h)
	return False if (res + h) & 1 else True


if __name__ == "__main__":
	parser = ArgumentParser()

	parser.add_argument("filename", type=str, help="File with puzzle")
	parser.add_argument("-heruistic", type=int, default=1, 
		help="Select heuristic (1 - manhattan, 2 - text1, 3 - text2)")
	parser.add_argument("-v", action='store_true', help="Run program with GUI")
	args = parser.parse_args()
	start = get_board(args.filename)
	goal = make_goal(len(start))

	if not is_solvable(start, goal, len(start)):
		print('Error. Puzzle not solvable')
		exit()

	s = Solver(start, goal)
	s.Astar()
	path = s.get_path()

	if args.v:
		game(path, start, int(sqrt(len(start))))

# Если -u и size - нечетное -> РЕШАЕТСЯ
# Если -s и size - четное -> НЕ РЕШАЕТСЯ