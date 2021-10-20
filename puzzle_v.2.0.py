from heapq import *

class Node:
	def __init__(self, new_state):
		state = new_state
		self.f = 0
		self.g = 0
		self.h = 0

	def kek(self):
		pass




def heuristic(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solver(board, goal):
	queue = []
	heappush(queue, (0, 1))

	while queue:
		pass




def make_goal(size):
	arr = []
	step = 1
	for i in range(size):
		arr.append([])
		for _ in range(size):
			arr[i].append(step)
			step += 1
	arr[-1][-1] = 0
	return arr


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
	
	goal = make_goal(len(board))
	solver(board, goal)
