#include <stdio.h>

int main()
{
  system("python gameFiles/chessGame.py");//the -i is there so we can see the error message if it crashes. TODO: remove the -i when ready to release
  return 1;
}
