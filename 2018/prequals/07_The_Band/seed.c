#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

void InitSeed(int *a1)
{
  struct timeval tv;

  gettimeofday(&tv, 0LL);
  srandom((tv.tv_sec & 0xffffffff) + ((tv.tv_usec & 0xffffffff) * 1000000));
  *a1 = rand() % 20 + 80;
  // printf("%d\n", *a1);
  do
  {
    do
      a1[1] = rand() % 20 + 80;
    while ( (a1[1] - *a1) >= -2 && (a1[1] - *a1) <= 2 );
  }
  while ( abs(a1[1] - *a1) > 10 );
}

int SeedRelated(int *a1)
{
  return (unsigned int)(4 * (abs(2 * (a1[1] - *a1)) - 1) + 3);
}

int main() {
  int seeds[2] = {0};
  InitSeed(seeds);
  // printf("%d\n", seeds[0]);
  printf("%d %d %d", seeds[0], seeds[1], SeedRelated(seeds));
  exit(0);
}
