#include "npuzzle.h"

int		is_empty(t_queue **queue)
{
	if (*queue)
		return (0);
	return (1);
}

void	queue_push(t_queue **queue, t_node *node, size_t priority)
{
	t_queue	*res;
	t_queue	*tmp;

	res = calloc(sizeof(t_queue), 1);
	if (res)
	{
		res->priority = priority;
		res->node = node;
		if (!(*queue))
			*queue = res;
		else
		{
			if ((*queue)->priority >= priority)
			{
				res->next = *queue;
				(*queue) = res;
			}
			else
			{
				tmp = *queue;
				while (tmp && tmp->next)
				{
					if (tmp->next->priority >= priority)
						break;
					tmp = tmp->next;
				}
				res->next = tmp->next;
				tmp->next = res;
			}
		}
	}
}

t_queue	*queue_pop(t_queue **queue)
{
	t_queue	*tmp;

	if (*queue)
	{
		tmp = *queue;
		*queue = tmp->next;
		return tmp;
	}
	return NULL;
}

void	print_queue(t_queue **queue)
{
	t_queue *tmp;

	tmp = *queue;
	while(tmp)
	{
		printf("%lu  ", tmp->priority);
		tmp = tmp->next;
	}
}
