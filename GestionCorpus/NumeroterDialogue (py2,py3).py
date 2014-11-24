# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Version 1.0 (Python 2 & 3)
# Ajouter des numéros d'action aux descriptions
# Mettre le style "action" dans la colonne style

# <markdowncell>

# => from \_\_future\_\_ doit figurer en premier

# <codecell>

from __future__ import print_function
import codecs

# <markdowncell>

# ##Ouverture du fichier des sous-titres .ASS
# 
# Ce type de fichier est encodé avec UTF8 With BOM mais l'ouverture normale fonctionne sans encodage

# <codecell>

fichier=open('/Users/gilles/Copy/Recherche/Rugby/Videos/FranceArgentine-FR-actions-MT2.ass','r')
lignes=fichier.readlines()

# <markdowncell>

# ##Ajout des numéros d'action sur les éléments de dialogue
# Pour chaque *ligne* dans *lignes*
# 
# - si la *ligne* contient "Dialogue"
#  - on coupe la *ligne* sur les virgules "," dans *dialogueElements*
#  - on modifie le dernier *dialogueElements* pour ajouter un numéro en tête
#  - on réassemble la ligne et on l'écrit
# - sinon on écrit la ligne telle quelle

# <codecell>

style="action"
prefixe="A"
nbLigne=851
for ligne in lignes[:]:
    if 'Dialogue' in ligne:
        dialogueElements=ligne.strip().split(",")
        dialogueElements[-1]="%s-%03d "%(prefixe, nbLigne)+dialogueElements[-1]
        dialogueElements[3]=style
        print(",".join(dialogueElements))
        nbLigne+=1
    else:
        print(ligne.strip())

# <codecell>


