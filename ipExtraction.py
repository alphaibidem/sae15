

import re
import pandas as pd
from collections import Counter
# Ouvrir le fichier en mode lecture
with open('C:/Users/userlocal/Documents/ProjetSAE15/DumpFile.txt', 'r') as f:
    # Lire le contenu du fichier
    text = f.read()
    # Compiler l'expression régulière pour détecter les adresses IP
    pattern = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    # Trouver toutes les occurences d'adresses IP dans le contenu
    matches = pattern.findall(text)
    # Utiliser Counter pour compter le nombre d'occurrences de chaque adresse IP
    counts = dict(Counter(matches))
    # Convertir les résultats en DataFrame
    df = pd.DataFrame(counts.items(), columns=['Adresse IP', 'Occurences'])
    # Enregistrer le DataFrame dans un fichier Excel
    df.to_excel('resultats.xlsx', index=False)
    print("Les données ont été exportées vers le fichier resultats.xlsx")
most_common_ip = max(counts, key=counts.get)
print("Adresse IP qui envoie le plus de requêtes: ", most_common_ip)
print("Nombre de requêtes envoyées: ", counts[most_common_ip])

# Création d'un dictionnaire pour stocker les informations sur les destinataires des requêtes
request_info = {}

# Ouvrir de nouveau le fichier en mode lecture
with open('C:/Users/userlocal/Documents/ProjetSAE15/DumpFile.txt', 'r') as f:
    # Parcourir chaque ligne du fichier
    for line in f:
        # Vérifier si l'adresse IP courante est celle qui envoie le plus de requêtes
        if most_common_ip in line:
            # Utiliser l'expression régulière pour extraire l'adresse IP destinataire
            match = re.search(most_common_ip + ' > (.*)', line)
            if match:
                dest_ip = match.group(1).split(" ")[0]
                if dest_ip not in request_info:
                    request_info[dest_ip] = 1
                else:
                    request_info[dest_ip] += 1

# Afficher les informations sur les destinataires des requêtes
print("Destinataires des requêtes de l'adresse IP", most_common_ip)
for dest, count in request_info.items():
    print("Destinataire: ", dest)
    print("Nombre de requêtes: ", count)
    time = line.split(" ")[0]

