#include <stdio.h>
#include <stdlib.h>

void accessTerminal()
{
  const char *flag = getenv("FLAG");

  puts("Welcome to my terminal!");
  if (flag == NULL) {
    printf("No Flag defined \n");
    fflush(stdout);
    return 1;
  }
  else {
    printf("The Flag is: %s \n",flag);
    fflush(stdout);
  }
  return;
}

int main()
{
  start();
  puts("Not so easy!");
  fflush(stdout);
  return 0;
}

void start()
{
  char input [16];
  printf("%p\n",start);
  fflush(stdout);
  puts("Tell me the access word:");
  fflush(stdout);
  scanf("%s",input);
  return;
}
