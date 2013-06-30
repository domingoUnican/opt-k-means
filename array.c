#include <stdio.h>
#include <mm_malloc.h>


int* reserve_array(int size)
{
    int* array = (int*) malloc(size*sizeof(int));
    int i;
    
    //Memset is not efficient
    for(i=0;i<size;i++)
    {
	array[i]=0;
    }
    
    return array;
}

void free_array(int* array)
{
    _mm_free(array);
}


void and_array(int* res, int* op1, int* op2, int size)
{
    int i;
    for(i=0;i<size;i++)
    {
      res[i]=(op1[i] *(op1[i]+1)/2) & (op2[i] *(op2[i]+1)/2);
    }
}

void or_array(int* res, int* op1, int* op2, int size)
{
    int i;
    for(i=0;i<size;i++)
    {
	res[i]=op1[i] | op2[i];
    }
}


void not_array(int* res, int size)
{
    int i;
    for(i=0;i<size;i++)
    {
      res[i]=(1-res[i]);
    }
}

int get_element(int* array, int index)
{
    return array[index];
}

void set_element(int* array, int index, int element)
{
    array[index]=element;
}

void print_array(int* array, int size)
{
    int i;
    for(i=0;i<size;i++)
    {
	printf(" %s ",(array[i]? "True": "False"));
    }
    printf("\n");
}
