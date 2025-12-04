# -*- coding: utf-8 -*-
def lire_mots_depuis_fichier(nom_fichier):
    lignes = []

    with open(nom_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if " : " in ligne:
                lignes.append(ligne)

    return lignes

tab=lire_mots_depuis_fichier(r"C:\Users\HP 1030X360 G2\Documents\Projets Importants\PROJETS POO PYTHON\LesMotsdeMaFoi\glossaire_AZ.txt")
print("Voici le jeu Les mots de ma foi!")
print("Le but du jeu est de deviner un mot mystère lié à la foi chrétienne.")
print("Que veut dire le mot suivant : ")
taille=len(tab)
n=0
i=0
lettre= "O"
if(taille%2==0):
    while (lettre!="N" and i<taille/2):
        
        if(n%2==0):
            print(tab[i])
        else:
            print(tab[taille-1-i])
            i=i+1
        lettre=input("Appuyez sur O pour continuer ou N pour quitter : ").upper()
        n=n+1
        print(i)
else : #taille est impair
    while (lettre!="N" and i<=taille//2):
        if(i==taille//2):
            print(tab[taille//2])
            break
        if(n%2==0):
            print(tab[i])
        else:
            print(tab[taille-1-i])
            i=i+1
        lettre=input("Appuyez sur O pour continuer ou N pour quitter : ").upper()
        n=n+1
        print(i)
        



if(i==taille//2):
    print("Félicitations ! Vous avez découvert tous les mots mystères.")
else:
    print("Il reste encore des mots.Merci d'avoir joué !")