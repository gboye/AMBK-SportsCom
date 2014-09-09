# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Traitement des informations sur la ligne de temps

# <markdowncell>

# Importation des modules
# - pandas pour la gestion des csv et les calculs type excel
# - numpy pour les calculs en général
# - matplotlib pour les graphiques

# <codecell>

%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# <markdowncell>

# Lecture des fichiers csv dans une DataFrame
# 
# - Syncs pour les textes alignés avec le temps Début, Fin, Speaker, Text (on ajoute : Durée et Longueur dans le script)

# <codecell>

Syncs=pd.read_csv("./Syncs.csv",sep="\t")

# <markdowncell>

# Nettoyage des champs Speaker et Text pour supprimer les blancs en trop
# 
# - le str.strip() s'applique à chaque élément de la colonne

# <codecell>

Syncs['Speaker']=Syncs['Speaker'].str.strip()
Syncs['Text']=Syncs['Text'].str.strip()

# <markdowncell>

# Ajout des colonnes Durée et Longueur
# 
# - la différence entre les colonnes numériques donne directement le résultat dans la nouvelle colonne
# - le str.len() calcule la longueur de la chaîne pour chaque élément de la colonne

# <codecell>

Syncs['Durée']=Syncs['Fin']-Syncs['Début']
Syncs['Longueur']=Syncs['Text'].str.len()

# <markdowncell>

# Calcul du graphe de Durée pour le spk1 en fonction du numéro de Sync (pas de la timeline)
# 
# - Syncs.loc[Syncs['Speaker']=='spk1'] permet de sélectionner dans df seulement les éléments qui ont spk1 dans la colonne Speaker
# - une fois Syncs.loc[Syncs['Speaker']=='spk1'] sélectionnée, on peut l'utiliser comme une DataFrame normale ; ici en spécifiant la colonne Durée pour le graphe

# <codecell>

Syncs.loc[Syncs['Speaker']=="spk1"]['Durée'].plot()

# <markdowncell>

# Calcul du graphe de Longueur et Durée pour le spk1 en fonction du numéro de Sync (pas de la timeline)

# <codecell>

Syncs.loc[Syncs['Speaker']=="spk1"][["Longueur","Durée"]].plot()

# <codecell>


