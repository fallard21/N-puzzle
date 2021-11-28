#ifndef NPUZZLE_H
#define NPUZZLE_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

typedef struct s_queue t_queue;
typedef struct s_node t_node;
typedef struct s_list t_list;

struct s_list
{
	t_node *node;
	t_list *next;
};

struct s_queue
{
	size_t	priority;
	t_node	*node;
	t_queue *next;
};

struct s_node
{
	size_t		g;
	size_t		h;
	size_t		f;
	int16_t		weight;
	int16_t		*state;
	uint16_t	size;
	uint16_t	w;
	int16_t		cost;
	t_node		*parent;
};

size_t	manhattan(t_node *node);

int		is_empty(t_queue **queue);
void	queue_push(t_queue **queue, t_node *node, size_t priority);
t_queue *queue_pop(t_queue **queue);
void	print_queue(t_queue **queue);

int		nodecmp(t_node *node1, t_node *node2);
t_node	*find_node(t_list *list, t_node *node);
void	add_list(t_list **list, t_node *node);

void	print_list(t_list *lists);
void	print_node(t_node *node);

#endif