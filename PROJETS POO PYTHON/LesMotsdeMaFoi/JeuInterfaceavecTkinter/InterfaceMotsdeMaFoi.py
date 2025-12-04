# -*- coding: utf-8 -*-
import tkinter as tk

# --- Lecture du fichier texte ---
def lire_mots_depuis_fichier(nom_fichier):
    lignes = []
    with open(nom_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if " : " in ligne:
                lignes.append(ligne)
    return lignes


# --- Initialisation du jeu ---
tab = lire_mots_depuis_fichier(/media/donaldrobotics/8A181BB8181BA26D/Documents and Settings/HP 1030X360 G2/Documents/Projets Importants/PROJETS POO PYTHON/LesMotsdeMaFoi/JeuInterfaceavecTkinter)
taille = len(tab)
n = 0
i = 0
j=0
historique_mots = []

#---Fonction pour afficher le Précédent---
def mot_precedent():
    global historique_mots,j
    if len(historique_mots)==0 :
        label_mot.config(text="Vous êtes au début.")
    else:
        j=len(historique_mots)-2
        label_mot.config(text=historique_mots[j])
        historique_mots.remove(historique_mots[j])



# --- Fonction pour afficher le mot suivant ---
def mot_suivant():
    global n, i,historique_mots
    if taille == 0:
        label_mot.config(text="Aucun mot trouvé dans le fichier.")
        return

    if taille % 2 == 0:
        if i < taille / 2:
            if n % 2 == 0:
                label_mot.config(text=tab[i])
                historique_mots.append(tab[i])
            else:
                label_mot.config(text=tab[taille - 1 - i])
                historique_mots.append(tab[taille - 1 - i])
                i += 1
            n += 1
        else:
            label_mot.config(text="🎉 Félicitations ! Vous avez découvert tous les mots mystères.")
            bouton_suivant.config(state="disabled")
    else:
        if i <= taille // 2:
            if i == taille // 2:
                label_mot.config(text=tab[taille // 2])
                bouton_suivant.config(state="disabled")
                historique_mots.append(tab[taille // 2])
            elif n % 2 == 0:
                label_mot.config(text=tab[i])
                historique_mots.append(tab[i])
            else:
                label_mot.config(text=tab[taille - 1 - i])
                historique_mots.append(tab[taille - 1 - i])
                i += 1
            n += 1
        else:
            label_mot.config(text="🎉 Félicitations ! Vous avez découvert tous les mots mystères.")
            bouton_suivant.config(state="disabled")


# --- Fonction pour quitter ---
def quitter():
    fenetre.destroy()


# --- Création de la fenêtre principale ---
fenetre = tk.Tk()
fenetre.title("Les mots de ma foi")
fenetre.geometry("700x400")


#fenetre.config(bg="#f4f4f4") #blanc
fenetre.config(bg="#87CEEB")   # bleu ciel
# --- Widgets ---
label_titre = tk.Label(
    fenetre,
    text="✨ Les mots de ma foi ✨",
    font=("Arial", 20, "bold"),
    bg="#f4f4f4",
    fg="#1E90FF",  # bleu dodger
    #fg="#333",
)
label_titre.pack(pady=20)

label_mot = tk.Label(
    fenetre,
    text="Cliquez sur 'Suivant' pour commencer.",
    font=("Arial", 14),
    bg="white",
    fg="#222",
    wraplength=650,
    justify="center",
    relief="solid",
    padx=10,
    pady=10,
)
label_mot.pack(pady=20)

# Boutons
frame_boutons = tk.Frame(fenetre, bg="#87CEEB")
frame_boutons.pack(side="bottom",pady=10) #j'ai ajouté side="bottom"

bouton_suivant = tk.Button(
    frame_boutons,
    text="Suivant",
    command=mot_suivant,
    bg="green",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10,
)
bouton_suivant.grid(row=0, column=0, padx=20)

bouton_quitter = tk.Button(
    frame_boutons,
    text="Quitter",
    command=quitter,
    bg="red",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10,
)
bouton_quitter.grid(row=0, column=1, padx=20)

bouton_precedent = tk.Button(
    frame_boutons,
    text="Précédent",
    command=mot_precedent,
    bg="orange",
    fg="white",
    font=("Arial", 12, "bold"),
    width=10,
)
bouton_precedent.grid(row=0, column=2, padx=20)


# --- Lancer l'application ---
fenetre.mainloop()
