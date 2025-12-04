#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>// contient la fonction Sleep()

const int nl=40;
const int nc=90;
const int sl=9;
const int sc=36;
const int x=10;
const int y=10;


void display_tab(char tab[][nc])
{
    int i=0,j=0;

    for(i=0;i<nl;i++)
    {
        for(j=0;j<nc;j++)
        {
            if(i==0||i==nl-1)
            {
                tab[i][j]='-';
                printf("%c",tab[i][j]);
            }
            else if(j==0 || j==nc-1)
            {
                tab[i][j]='|';
                printf("%c",tab[i][j]);
            }
            else

                printf("%c",tab[i][j]);

        }
        printf("\n");
    }

}

char update_cell(char tab[][nc],int ipos,int jpos)
{
      int nbalive=0,i=0,j=0;

      for(i=ipos-1;i<=ipos+1;i++)
      {
          if(0<i&&i<nl)
          {
            for(j=jpos-1;j<=jpos+1;j++)
            {
            if(0<j&&j<nc)
            {

                if(!(i==ipos&&j==jpos))
                {
                    if (tab[i][j]=='*')
                        nbalive++;

                }
            }

          }
      }
}



if (tab[ipos][jpos]==' ')
{
    if(nbalive==3)
        return '*';
    else
        return ' ';
}
else
{
    if(nbalive==2||nbalive==3)
        return '*';
    else
        return ' ';
}

}

void updateV1(char tab[][nc],char bis_tab[][nc])
{
int i=0,j=0;
for(i=1;i<nl-1;i++)
    {
        for(j=1;j<nc-1;j++)
        {
          bis_tab[i][j]=update_cell(tab,i,j);
        }

    }

for(i=0;i<nl;i++)
    {
        for(j=0;j<nc;j++)
        {
            tab[i][j]=bis_tab[i][j];
        }

    }
}



int main()
{

    int i=0,j=0;
    char tableau[nl][nc];
    char bis_tab[nl][nc];
    char smatrix[9][36]={
    {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '},
    {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*',' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '},
    {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*','*',' ',' ',' ',' ',' ',' ','*','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*','*'},
    {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' ','*',' ',' ',' ',' ','*','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*','*'},
    {'*','*',' ',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' ',' ',' ','*',' ',' ',' ','*','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '},
    {'*','*',' ',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' ','*',' ','*','*',' ',' ',' ',' ','*',' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '},
    {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' ',' ',' ','*',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '},
    {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*',' ',' ',' ','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '},
    {' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','*','*',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '}
    };

    /*{
    {' ','*',' '},
    {'*','*','*'},
    {' ','*',' '}

    };*/

    for(i=0;i<nl;i++)
    {
        for(j=0;j<nc;j++)
        {
            tableau[i][j]=' ';
            bis_tab[i][j]=tableau[i][j];
        }

    }

    for(i=y;i<y+sl;i++)
    {
        for(j=x;j<x+sc;j++)
        {
            tableau[i][j]=smatrix[i-y][j-x];
            bis_tab[i][j]=tableau[i][j];
        }

    }


    display_tab(tableau);
    Sleep(100);
    while(1)
    {
       system("cls");// effacer tout ce qu'il y a dans le terminal(apres avoir executé le code)
       updateV1(tableau,bis_tab);
    display_tab(tableau);
    Sleep(1000);//  met le programme sur pause en microseconds

    }

return 0;
}
