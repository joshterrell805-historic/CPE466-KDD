#include "hashtable.h"
#include <stdlib.h>

map *createMap(int size) {
  map *ret = (map *) calloc(1, sizeof(map));
  ret->keys = (unsigned int *) calloc(size, sizeof(unsigned int));
  ret->values = (int *) calloc(size, sizeof(int));
  ret->size = size;
  return ret;
}

void destroyMap(map *garbage) {
  free(garbage->keys);
  free(garbage->values);
  free(garbage);
}

int getItem(map *hashtable, unsigned int key) {
  // Ensure value is non-zero
  key++;
  int index = key % hashtable->size;
  while (hashtable->keys[index] != key && hashtable->keys[index]) {
    index++;
  }
  return hashtable->values[index];
}

void addItem(map *hashtable, unsigned int key, int value) {
  // Ensure key is non-zero
  key++;
  int index = key % (hashtable->size);
  while (hashtable->keys[index]) {
    index++;
  }

  hashtable->keys[index] = key;
  hashtable->values[index] = value;
}

