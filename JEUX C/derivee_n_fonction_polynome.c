 #include <stdio.h>
#include <stdlib.h>



 int main()
{

    int n=8,i,k,p;
   int tab[n+1];
    printf("Veuillez entrer les valeurs des facteurs de chaque terme du polynome: \n");
    for(i=0;i<9;i++)
    {
        scanf("%d",&tab[i]);

    }
   for(i=0;i<9;i++)
    {
       printf("[%d]",tab[i]);
    }
    printf("\nCe programme va deriver une fonction polynomiale dont les facteurs sont les valeurs du tableau.");
    printf("\nEntrez la puissance de derivation: ");
    scanf("%d",&k);
    if(k>n)
    {
        for(i=0;i<9;i++)
        {
            tab[i]=0;
        }
         for(i=0;i<9;i++)
            {
               printf("[%d]",tab[i]);
            }
    }
    else
    {
        for(p=1;p<=k;p++)
        {
            i=1;
            while(i<n+2-p)
            {
                tab[i-1]=i*tab[i];
                i++;
            }
            tab[i-1]=0;


        }
        printf("Voici les facteurs des termes de %d_ieme derivee:\n",k);
            for(i=0;i<9;i++)
                {
                   printf("[%d]",tab[i]);
                }
    }
 return 0;
}

