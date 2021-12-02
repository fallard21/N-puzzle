def manhattan(state : list, goal : list, size):
	h = 0
	for i in range(size * size):
		if state[i] and state[i] != goal[i]:
			k = goal.index(state[i])
			#gx, gy = k % size, k // size
			#x, y = k % size, k // size
			h += abs(i % size - k % size) + abs(i // size - k // size)
	return h