#include "hashtable.h"
#test test_hashtable
{
  map *map = createMap(100);
  addItem(map, 34, 10000);
  addItem(map, 1022, 42);
  ck_assert_int_eq(getItem(map, 1022), 42);
  ck_assert_int_eq(getItem(map, 34), 10000);
  destroyMap(map);
}

#test test_hasItem
{
  map *map = createMap(100);
  addItem(map, 34, 100);
  ck_assert(hasItem(map, 34));
  ck_assert(!hasItem(map, 35));
  destroyMap(map);
}
