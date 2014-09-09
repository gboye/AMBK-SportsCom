# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Version 1.0 (Python 2.7)
# Répartition des actions en fonction du temps restant à partir d'une étiquette de temps donnée (ligneUnique)

# <codecell>

import codecs, sys

# <codecell>

def vprint(chaine):
    if sys.version_info[0]==2:
        print chaine
    elif sys.version_info[0]==3:
        print (chaine)

# <codecell>

fichier=open('./MiTemps1-GB.ass','r')
lignes=fichier.readlines()

# <codecell>

nbLigne=1
for ligne in lignes:
    if 'Dialogue' in ligne:
        dialogueElements=ligne.split(",")
        dialogueElements[-1]="A-%03d "%nbLigne+dialogueElements[-1]
        vprint(",".join(dialogueElements))
        nbLigne+=1
    else:
        vprint(ligne)

# <codecell>


