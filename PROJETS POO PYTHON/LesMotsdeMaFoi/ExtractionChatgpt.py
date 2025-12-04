# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time

# URL de la page des mots commençant par "A"
url = "https://eglise.catholique.fr/glossaire/lettre/a"

# Ajouter un User-Agent pour éviter les blocages
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}

# Télécharger la page principale
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Trouver tous les liens vers les mots (balises <a> dans les <li>)
items = soup.select("ul.glossary-list li a")

with open("glossaire_A.txt", "w", encoding="utf-8") as f:
    for a in items:
        mot = a.get_text(strip=True)
        lien = a.get("href")

        if not lien.startswith("http"):
            lien = "https://eglise.catholique.fr" + lien

        # Télécharger la page individuelle du mot
        page = requests.get(lien, headers=headers)
        page.raise_for_status()

        page_soup = BeautifulSoup(page.text, "html.parser")

        # Chercher le contenu de la définition complète
        contenu = page_soup.select_one("div.entry-content")

        if contenu:
            definition = contenu.get_text(" ", strip=True)
            f.write(f"{mot} : {definition}\n\n")
            print(f"✅ {mot}")
        else:
            print(f"⚠️ Définition introuvable pour {mot}")

        # Petite pause pour ne pas surcharger le site
        time.sleep(1)

print("\n📘 Fichier 'glossaire_A.txt' créé avec succès !")
