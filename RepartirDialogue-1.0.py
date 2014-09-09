# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Version 1.0 (Python 2.7)
# Répartition des actions en fonction du temps restant à partir d'une étiquette de temps donnée (ligneUnique)

# <codecell>

import codecs

# <codecell>

fichier=open('./MiTemps1-v1.ass','r')
lignes=fichier.readlines()

# <codecell>

sortie=[]
ligneUnique=",0:16:29.58"
tempsFin="0:50:00.00"
nbCourtes=0
nbNormales=0
nbLongues=0
incrementCourt=0
ratioCourtNormal=8
ratioCourtLong=25
Transition=False
ActionsCourtes=["passe","réception","extraction","plaquage","récupération","lacher","rebond","porté","écroulement"]
SequencesLongues=["mise en ligne","ralenti","replay","marqué"]

# <codecell>

for ligne in lignes:
    if 'Dialogue' in ligne:
        if ligneUnique in ligne:                
            tempsDebut=ligne.split(",")[2]
            Transition=True
        elif Transition:
            action=ligne.split(",")[9].strip()
            if action in ActionsCourtes:
                nbCourtes+=1
            elif action in SequencesLongues:
                nbLongues+=1
            else:
                nbNormales+=1

# <codecell>

print nbCourtes, nbNormales, nbLongues, tempsDebut, tempsFin

# <codecell>

def calculTemps(chaine):
    heures,minutes,secondes=chaine.split(":")
    result=float(secondes)
    result+=60*float(minutes)
    result+=3600*float(heures)
    return result

def calculChaine(temps):
    heures=temps//3600
    reste=temps-heures*3600
    minutes=reste//60
    secondes=reste-minutes*60
    result="%d:%02d:%05.2f" % (heures,minutes,secondes)
    return result

def changeLigne(chaine,increment):
    champs=chaine.split(',')
    champs[1]=calculChaine(timingDebut+(nbCourtes+ratioCourtNormal*nbNormales+ratioCourtLong*nbLongues)*incrementCourt)
    champs[2]=calculChaine(timingDebut+(nbCourtes+ratioCourtNormal*nbNormales+ratioCourtLong*nbLongues)*incrementCourt+increment)
    result=",".join(champs)
    return result
        

# <codecell>

timingDebut=calculTemps(tempsDebut)
timingFin=calculTemps(tempsFin)
timing=timingFin-timingDebut

# <codecell>

equivalentCourt=nbCourtes+ratioCourtNormal*nbNormales+ratioCourtLong*nbLongues
incrementCourt=timing/equivalentCourt
incrementNormal=ratioCourtNormal*incrementCourt
incrementLong=ratioCourtLong*incrementCourt

print calculChaine(timingDebut+incrementCourt*(nbCourtes+ratioCourtNormal*nbNormales+ratioCourtLong*nbLongues))

# <codecell>

nbCourtes=0
nbNormales=0
nbLongues=0
Transition=False
for ligne in lignes:
    if 'Dialogue' in ligne:
        if ligneUnique in ligne:                
            Transition=True
            print ligne
        elif Transition:
            action=ligne.split(",")[9].strip()
            if action in ActionsCourtes:
                print changeLigne(ligne,incrementCourt)
                nbCourtes+=1
            elif action in SequencesLongues:
                print changeLigne(ligne,incrementLong)
                nbLongues+=1                
            else:
                print changeLigne(ligne,incrementNormal)
                nbNormales+=1
        else:
            print ligne
    else:
        print ligne
# print nbCourtes, nbNormales, nbLongues

# <codecell>


