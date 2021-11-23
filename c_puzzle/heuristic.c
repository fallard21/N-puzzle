#include "npuzzle.h"

size_t	manhattan(t_node *node)
{
	size_t h;
	size_t i;

	h = 0;
	i = 0;
	while(i < node->size)
	{
		if (node->state[i] != i + 1 && node->state[i] != 0)
			h += abs(i % node->w - (node->state[i] - 1) % node->w) +
				abs(i / node->w - (node->state[i] - 1) / node->w);
		i++;
	}
	return h;
}
