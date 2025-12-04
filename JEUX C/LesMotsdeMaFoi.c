#include<stdio.h>

int main()
{   char c;
    int i=0,taille=10;
    char*tab[10]={"D : d","A : a","B : b","C : c","G : g","E : e","F : f","Z : z","Q : q","H : h"};
    printf("Voici le jeu Les mots de ma foi.\n");
    printf("Que veut dire le mot suivant: \n");
    do
    {
        if(i%2==0) printf("%s \n",tab[i]);
        else printf("%s \n",tab[i+taille-2]);


        if(i==0) printf("Continuer ? O-o pour dire oui/N-n pour dire non. \n");
        else printf("Continuer?");
        scanf("%c",&c);
        while(getchar()!='\n');
        i++;
    }while(c!='n'&&c!='N');

return 0;
}
