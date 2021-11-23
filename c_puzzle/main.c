#include "npuzzle.h"
#include <math.h>

t_node	*make_goal(uint16_t size)
{
	t_node	*goal;
	int16_t	i;

	goal = calloc(sizeof(t_node), 1);
	if (goal)
	{
		goal->size = size;
		goal->weight = 1;
		goal->w = (uint16_t)sqrt(size);
		goal->state = calloc(sizeof(int16_t), size);
		if (goal->state)
		{
			i = 0;
			while (i < size - 1)
				goal->state[i++] = i;
			return (goal);
		}
		free (goal);
	}
	return (NULL);
}

t_node *make_node(int16_t *state, size_t g, uint16_t size)
{
	t_node *node;

	node = calloc(sizeof(t_node), 1);
	if (node)
	{
		node->state = calloc(sizeof(uint16_t), size);
		if (node->state)
		{
			memcpy(node->state, state, sizeof(uint16_t) * size);
			node->g = g;
			node->cost = 0;
			node->size = size;
			node->weight = 1;
			node->w = (int16_t)sqrt(size);
			return (node);
		}
		free(node);
	}
	return (NULL);
}

t_list *neighbors(t_node *node)
{
	t_list	*res = NULL;
	t_node	*new = NULL;
	int		moves[4] = {-1, -node->w, 1, node->w};
	int		zero = 0;

	for (int i = 0; i < node->size; i++)
	{
		if (!node->state[i])
		{
			zero = i;
			break;
		}
	}
	for(int i = 0; i < 4; i++)
	{
		int pos = zero + moves[i];
		if ((pos % node->w > zero % node->w && pos / node->w < zero / node->w) ||
			(pos % node->w < zero % node->w && pos / node->w > zero / node->w) ||
			(pos < 0) ||
			(pos > node->size - 1))
			continue;
		new = make_node(node->state, node->g + 1, node->size);
		if (new)
		{
			int tmp = new->state[zero];
			new->state[zero] = new->state[pos];
			new->state[pos] = tmp;
			new->parent = node;
			add_list(&res, new);
		}
	}
	return res;
}

t_list	*a_star(t_node *start, t_node *goal)
{
	t_queue	*queue = NULL;
	t_list	*closed = NULL;
	t_list	*tmp = NULL;
	t_node	*find = NULL;

	queue_push(&queue, start, 0);
	add_list(&closed, start);
	while(!is_empty(&queue))
	{
		//print_queue(&queue);
		//getchar();
		//printf("AGAIN\n");
		t_node *current = queue_pop(&queue)->node;
		if (nodecmp(current, goal))
			break ;
		t_list *next_nodes = neighbors(current);
		//print_list(next_nodes);
		tmp = next_nodes;
		while (tmp)
		{
			//printf("AGAIN2\n");
			int16_t new_cost = tmp->node->weight + find_node(closed, current)->cost; // ?
			//printf("AGAIN3\n");
			find = find_node(closed, tmp->node);
			if (!find || new_cost < find->cost) // ?
			{
				tmp->node->cost = new_cost;
				size_t priority = new_cost + manhattan(tmp->node);
				if (!find)
				{
					add_list(&closed, tmp->node); // ?
					queue_push(&queue, tmp->node, priority);
				}
				else
					find->cost = new_cost;
			}
			tmp = tmp->next;
		}
	}
	printf("END\n");
	return closed;
}

int		main()
{
	// int16_t	st[] = {1, 2, 7,
	// 				3, 4, 6,
	// 				0, 8, 5};
	// int size = 9;

	int16_t	st[] = {1, 2, 4, 0,
					12, 13, 3, 5,
					11, 9, 14, 6,
					10, 8, 15, 7};
	int size = 16;

	t_node	*start = make_node(st, 0, size);
	t_node	*goal = make_goal(size);
	
	printf("Start\n");
	t_list *end = a_star(start, goal);

	t_node *n = find_node(end, goal);
	while (n)
	{
		print_node(n);
		printf("\n");
		n = n->parent;
	}

	return (0);
}