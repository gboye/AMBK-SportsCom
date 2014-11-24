# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Version 1.0 (Python 2 & 3)
# Ajouter les styles et les acteurs correspondant aux intervenants

# <codecell>

from __future__ import print_function
import codecs

# <markdowncell>

# ##Ouverture du fichier des sous-titres .ASS

# <codecell>

fichier=open('../Videos/FranceArgentine-FR-commentaires.ass','r')
lignes=fichier.readlines()

# <markdowncell>

# ##Ajout des numéros d'action sur les éléments de dialogue
# Pour chaque *ligne* dans *lignes*
# 
# - si la *ligne* contient "Dialogue"
#  - on coupe la *ligne* sur les virgules "," dans *dialogueElements*
#  - on coupe le dernier *dialogueElements* sur les espaces " " dans *dialogue*
#  - si le *dialogue* contient plus d'un élément
#    - on coupe le premier élément de *dialogue* sur le tiret "-" et on met le premier élément dans *speaker*
#    - on renseigne le style *dialogueElements[3]* et l'acteur *dialogueElements[4]* avec *speaker*
#  - sinon 
#    - on renseigne le style *dialogueElements[3]* avec "pb"
#    - on ajoute "PROBLÈME " au dernier élément de *dialogueElements*
#  - on réassemble la ligne et on l'écrit
# - sinon on écrit la ligne telle quelle

# <codecell>

pb=False
for ligne in lignes[:]:
    if 'Dialogue' in ligne:
        dialogueElements=ligne.split(",")
        texte=dialogueElements[-1]
        if "-" in texte:
            dialogue=dialogueElements[-1].split(" ")
            if len(dialogue)>1:
                speaker=dialogue[0].split("-")[0]
                if len(texte)>1:
                    dialogueElements[3]=speaker
                    dialogueElements[4]=speaker
                else:
                    dialogueElements[3]="pb"
                    dialogueElements[-1]="PROBLÈME"+dialogueElements[-1]
            else:
                pb=True
                dialogueElements[3]="pb"
                dialogueElements[-1]="PROBLÈME "+dialogueElements[-1]
            print(",".join(dialogueElements))
        else:
            if pb:
                pb=False
                dialogueElements[3]="pb"
                dialogueElements[4]=speaker
                dialogueElements[-1]="PROBLÈME "+dialogueElements[-1]                
    else:
        print(ligne)

# <codecell>


