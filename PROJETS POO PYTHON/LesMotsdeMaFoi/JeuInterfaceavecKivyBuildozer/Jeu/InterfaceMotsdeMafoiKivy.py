# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

# --- Lecture du fichier texte ---
def lire_mots_depuis_fichier(nom_fichier):
    lignes = []
    with open(nom_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if " : " in ligne:
                lignes.append(ligne)
    return lignes


# --- Widget principal ---
class LesMotsDeMaFoi(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=20, padding=20, **kwargs)

        # --- Couleur de fond ---
        Window.clearcolor = (135/255, 206/255, 235/255, 1) # bleu ciel

        # --- Titre ---
        self.label_titre = Label(
            text="✨ Les mots de ma foi ✨",
            font_size='24sp',
            bold=True,
            color=(30/255, 144/255, 1, 1),  # bleu dodger
            size_hint=(1, 0.2)
        )
        self.add_widget(self.label_titre)

        # --- Label du mot ---
        self.label_mot = Label(
            text="Cliquez sur 'Suivant' pour commencer.",
            font_size='18sp',
            color=(0,0,0,1),
            size_hint=(1, 0.5),
            halign='center',
            valign='middle'
        )
        self.label_mot.bind(size=self.label_mot.setter('text_size'))
        self.add_widget(self.label_mot)

        # --- Boutons ---
        boutons_layout = BoxLayout(size_hint=(1, 0.1), spacing=20)

        self.bouton_suivant = Button(
            text="Suivant",
            background_color=(0, 1, 0, 1),
            font_size='18sp'
        )
        self.bouton_suivant.bind(on_press=self.mot_suivant)
        boutons_layout.add_widget(self.bouton_suivant)

        self.bouton_quitter = Button(
            text="Quitter",
            background_color=(1, 0, 0, 1),
            font_size='18sp'
        )
        self.bouton_quitter.bind(on_press=self.quitter)
        boutons_layout.add_widget(self.bouton_quitter)

        self.bouton_precedent = Button(
            text="Précédent",
            background_color=(0, 0, 1, 1),
            font_size='18sp',
        )
        self.bouton_precedent.bind(on_press=self.mot_precedent)
        boutons_layout.add_widget(self.bouton_precedent)

        self.add_widget(boutons_layout)

        # --- Initialisation du jeu ---
        self.tab = lire_mots_depuis_fichier(r"C:\Users\HP 1030X360 G2\Documents\Projets Importants\PROJETS POO PYTHON\LesMotsdeMaFoi\JeuInterfaceavecKivyBuildozer\Jeu\glossaire_AZ.txt")  # adapte le chemin pour Android
        self.taille = len(self.tab)
        self.n = 0
        self.i = 0
        self.j = 0
        self.historique_mots = []

    # --- Fonction pour afficher le mot suivant ---
    def mot_suivant(self, instance):
        if self.taille == 0:
            self.label_mot.text = "Aucun mot trouvé dans le fichier."
            return

        if self.taille % 2 == 0:
            if self.i < self.taille / 2:
                if self.n % 2 == 0:
                    self.label_mot.text = self.tab[self.i]
                    self.historique_mots.append(self.tab[self.i])
                else:
                    self.label_mot.text = self.tab[self.taille - 1 - self.i]
                    self.historique_mots.append(self.tab[self.taille - 1 - self.i])
                    self.i += 1
                self.n += 1
            else:
                self.label_mot.text = "🎉 Félicitations ! Vous avez découvert tous les mots mystères."
                self.bouton_suivant.disabled = True
        else:
            if self.i <= self.taille // 2:
                if self.i == self.taille // 2:
                    self.label_mot.text = self.tab[self.taille // 2]
                    self.bouton_suivant.disabled = True
                    self.historique_mots.append(self.tab[self.taille // 2])
                elif self.n % 2 == 0:
                    self.label_mot.text = self.tab[self.i]
                    self.historique_mots.append(self.tab[self.i])
                else:
                    self.label_mot.text = self.tab[self.taille - 1 - self.i]
                    self.historique_mots.append(self.tab[self.taille - 1 - self.i])
                    self.i += 1
                self.n += 1
            else:
                self.label_mot.text = "🎉 Félicitations ! Vous avez découvert tous les mots mystères."
                self.bouton_suivant.disabled = True

    # --- Fonction pour quitter ---
    def quitter(self, instance):
        App.get_running_app().stop()
    
    #---Fonction pour afficher le Précédent---
    def mot_precedent(self, instance):
        if len(self.historique_mots)==0 :
            self.label_mot.text="Vous êtes au début."
        else:
            self.j=len(self.historique_mots)-2
            self.label_mot.text=self.historique_mots[self.j]
            self.historique_mots.remove(self.historique_mots[self.j])





# --- Classe App ---
class JeuApp(App):
    def build(self):
        return LesMotsDeMaFoi()


if __name__ == "__main__":
    JeuApp().run()
