#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

//#include <cstddef>
struct tnode {                // узел дерева
  int num;                  // указатель на строку (слово)
  int count;                   // число вхождений
  struct tnode* left;          // левый потомок
  struct tnode* right;         // правый потомок
};
// Функция добавления узла к дереву
struct tnode* addtree(struct tnode* p, int w) {
	int cond;
	if (p == NULL) {
		p = (struct tnode*)malloc(sizeof(struct tnode));
		p->num = w;
		p->count = 1;
		p->left = p->right = NULL;
	}
	// else if (w == p->num)
	// 	p->count++;
	else if (w < p->num)
		p->left = addtree(p->left, w);
	else
		p->right = addtree(p->right, w);
	return p;
}
// Функция удаления поддерева
void freemem(struct tnode **tree) {
  if (*tree != NULL) {
    freemem(&(*tree)->left);
    freemem(&(*tree)->right);
    //free(tree->word);
    free(*tree);
    *tree = NULL;
  }
}
// Функция вывода дерева
void treeprint(struct tnode* p) {
  if (p != NULL) {
    treeprint(p->left);
    printf("%d [%d]\n", p->count, p->num);
    treeprint(p->right);
  }
}

void shell_sort(int *array, int size) {
    for (int s = size / 2; s > 0; s /= 2) {
        for (int i = s; i < size; ++i) {
            for (int j = i - s; j >= 0 && array[j] > array[j + s]; j -= s) {
                int temp = array[j];
                array[j] = array[j + s];
                array[j + s] = temp;
            }
        }
    }
}

void bubble_sort(int *num, int size)
{
	// Для всех элементов
	for (int i = 0; i < size - 1; i++)
	{
		for (int j = size - 1; j > i; j--) // для всех элементов после i-ого
		{
			if (num[j - 1] > num[j]) // если текущий элемент меньше предыдущего
			{
				int temp = num[j - 1]; // меняем их местами
				num[j - 1] = num[j];
				num[j] = temp;
			}
		}
	}
}

void quickSort(int *numbers, int left, int right)
{
  int pivot; // разрешающий элемент
  int l_hold = left; //левая граница
  int r_hold = right; // правая граница
  pivot = numbers[left];
  while (left < right) // пока границы не сомкнутся
  {
    while ((numbers[right] >= pivot) && (left < right))
      right--; // сдвигаем правую границу пока элемент [right] больше [pivot]
    if (left != right) // если границы не сомкнулись
    {
      numbers[left] = numbers[right]; // перемещаем элемент [right] на место разрешающего
      left++; // сдвигаем левую границу вправо
    }
    while ((numbers[left] <= pivot) && (left < right))
      left++; // сдвигаем левую границу пока элемент [left] меньше [pivot]
    if (left != right) // если границы не сомкнулись
    {
      numbers[right] = numbers[left]; // перемещаем элемент [left] на место [right]
      right--; // сдвигаем правую границу вправо
    }
  }
  numbers[left] = pivot; // ставим разрешающий элемент на место
  pivot = left;
  left = l_hold;
  right = r_hold;
  if (left < pivot) // Рекурсивно вызываем сортировку для левой и правой части массива
    quickSort(numbers, left, pivot - 1);
  if (right > pivot)
    quickSort(numbers, pivot + 1, right);
}

int randint(int min, int max)
{
	return rand() % (max - min + 1) + min;
}

void tree_test(size_t size)
{
	struct tnode *root;

	root = NULL;
	srand(time(NULL));
	for(int i = 0; i < size; i++)
		root = addtree(root, randint(0, 9999999));
	
	// root = addtree(root, 8);
	// root = addtree(root, 10);
	// root = addtree(root, 2);
	// root = addtree(root, 5);
	// root = addtree(root, 2);
	// root = addtree(root, 1);
	// root = addtree(root, 3);
	// root = addtree(root, 4);
	// root = addtree(root, 5);
	//treeprint(root);
	freemem(&root);
}

void shell_test(size_t size)
{
	int *arr = malloc(sizeof(int) * size);
	for(int i = 0; i < size; i++)
		arr[i] = randint(0, 9999999);
	shell_sort(arr, size);
	free(arr);
}

void bubble_test(size_t size)
{
	int *arr = malloc(sizeof(int) * size);
	for(int i = 0; i < size; i++)
		arr[i] = randint(0, 9999999);
	bubble_sort(arr, size);
	free(arr);
}

void qsort_test(size_t size)
{
	int *arr = malloc(sizeof(int) * size);
	for(int i = 0; i < size; i++)
		arr[i] = randint(0, 9999999);
	quickSort(arr, 0, size - 1);
	//for(int i = 0; i < 50; i++)
	//	printf("%d ", arr[i]);
	free(arr);
}

int main() {
	size_t size = 10000000;
	//tree_test(size);
	//shell_test(size);
	//bubble_test(size);
	qsort_test(size);
	return 0;
}