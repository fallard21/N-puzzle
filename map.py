from heapq import *

def find_childrens(board, curent, goal):
	childrens = []
	moves = [
		[-1, 0], # left
		[0, -1], # up
		[1, 0], # right
		[0, 1] # down
		]
	state = curent[1]
	for m in moves:
		pos = (state[0] + m[0], state[1] + m[1])
		if (pos[0] > (len(board) - 1) or
			pos[0] < 0 or
			pos[1] < 0 or
			pos[1] > (len(board[0]) - 1)):
			continue
		if board[pos[0]][pos[1]] == 0:
			continue
		childrens.append((1, pos))
	return childrens


def heuristic(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dijkstra(start, goal, graph):
	counter = 0
	queue = []
	heappush(queue, (0, start))
	cost_visited = {start : 0}
	visited = {start : None}
    
	while queue:
		cur_node = heappop(queue)
		if cur_node[1] == goal:
			break
        
		next_nodes = find_childrens(graph, cur_node, goal)
		#print(cur_node, '->', next_nodes)
		#input()
		for next_node in next_nodes:
			neigh_cost, neigh_node = next_node
			new_cost = neigh_cost + cost_visited[cur_node[1]]
			#print(new_cost)
			if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
				priority = new_cost + heuristic(neigh_node, goal) # with A*
				heappush(queue, (priority, neigh_node)) # with A*
				#heappush(queue, (new_cost, neigh_node)) # without A*
				cost_visited[neigh_node] = new_cost
				visited[neigh_node] = cur_node[1]
		counter += 1
		print([q[0] for q in queue])
	print(counter)
	#print(cost_visited)
	return visited


# НАЧАЛО
if __name__ == "__main__":
	start = (1, 1)
	goal = (1, 14)
	graph = [
			[-1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1],
			[-1, -1,  0,  0, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1],
			[-1, -1, -1,  0, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1],
			[-1, -1, -1,  0, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1],
			[-1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0,  0, -1, -1, -1],
			[-1, -1, -1, -1, -1, -1, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1],
			[-1, -1, -1, -1, -1,  0,  0,  0, -1,  0, -1, -1, -1, -1, -1, -1],
			[-1,  0,  0,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
			[-1, -1, -1,  0, -1, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1, -1],
			[-1, -1, -1,  0, -1,  0, -1,  0, -1, -1, -1,  0,  0,  0, -1, -1],
			[-1, -1, -1,  0, -1,  0, -1,  0, -1, -1, -1, -1,  0, -1, -1, -1],
			[-1, -1, -1, -1, -1,  0, -1, -1,  0, -1,  0,  0,  0, -1, -1, -1],
			[-1, -1, -1, -1, -1,  0, -1, -1,  0, -1, -1, -1, -1, -1, -1, -1],
			[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
			]

	# start = (2, 1)
	# goal = (2, 5)
	# graph = [
	# 		[-1, -1, -1, -1, -1, -1, -1],
	# 		[-1, -1,  0,  0, -1, -1, -1],
	# 		[-1, -1, -1,  0, -1, -1, -1],
	# 		[-1, -1, -1, -1, -1, -1, -1],
	# 		[-1, -1, -1, -1, -1, -1, -1]
	# 		]

	path = dijkstra(start, goal, graph)
	
	# Output graph version 1
	# cur_node = goal
	# print(goal, end= '')
	# while cur_node != start:
	# 	cur_node = s[cur_node]
	# 	print(f' --> {cur_node} ', end='')


	# Output graph version 2
	cur_node = goal
	graph[goal[0]][goal[1]] = 1
	step = 2
	while cur_node != start:
		cur_node = path[cur_node]
		graph[cur_node[0]][cur_node[1]] = step
		step = step + 1

	for i in range(len(graph)):
		for j in range(len(graph[0])):
			if graph[i][j] == -1:
				if (i, j) in path: # Если клетка посещена, то окрашиваем в зеленый, иначе - в красный
					print('\033[32m%3d\033[0m' % graph[i][j], end='')
				else:
					print('\033[31m%3d\033[0m' % graph[i][j], end='')
			elif graph[i][j] > 0:
				print('\033[33m%3d\033[0m' % graph[i][j], end='')
			else:
				print('%3d' % graph[i][j], end='')
		print()