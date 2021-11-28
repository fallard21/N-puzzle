#include "npuzzle.h"

int nodecmp(t_node *node1, t_node *node2)
{
	int i;

	i = 0;
	while (i < node1->size)
	{
		if (node1->state[i] != node2->state[i])
			return (0); // False
		i++;
	}
	return (1); // True
}

t_node	*find_node(t_list *list, t_node *node)
{
	while(list)
	{
		if (nodecmp(list->node, node))
			return list->node; // True
		list = list->next;
	}
	return NULL; // False
}

void	add_list(t_list **list, t_node *node)
{
	t_list *new;

	new = calloc(sizeof(t_list), 1);
	if (new)
	{
		new->node = node;
		new->next = *list;
		*list = new;
	}
}

void	print_list(t_list *lists)
{
	printf("\n|========= NEIGHBORS ===========|\n");
	while(lists)
	{
		print_node(lists->node);
		printf("\n");
		lists = lists->next;
	}
}

void	print_node(t_node *node)
{
	for(int i = 0; i < node->size; i++)
	{
		if (i != 0 && i % node->w == 0)
			printf("\n");
		printf("%3d", node->state[i]);
	}
	printf("\n");
}
