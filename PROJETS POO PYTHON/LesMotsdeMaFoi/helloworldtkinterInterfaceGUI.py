import tkinter as tk

def dire_bonjour():
    label_message.config(text="Bonjour, utilisateur !")

def quitter():
    fenetre.destroy()

fenetre = tk.Tk()
fenetre.title("Exemple sans POO")

label_titre = tk.Label(fenetre, text="Mon premier programme Tkinter", font=("Arial", 16))
label_titre.pack(pady=10)

bouton_bonjour = tk.Button(fenetre, text="Dire Bonjour", command=dire_bonjour, bg="green", fg="white")
bouton_bonjour.pack(pady=5)

bouton_quitter = tk.Button(fenetre, text="Quitter", command=quitter, bg="red", fg="white")
bouton_quitter.pack(pady=5)

label_message = tk.Label(fenetre, text="")
label_message.pack(pady=10)

fenetre.mainloop()
