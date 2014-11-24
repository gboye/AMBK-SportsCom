# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import codecs

# <codecell>

fichier=open('./MiTemps1.ass','r')
lignes=fichier.readlines()

# <codecell>

sortie=[]
ligneUnique="0:06:43.06,0:06:46.36"
tempsFin="0:50:00.00"
nombreLignes=0

# <codecell>

for ligne in lignes:
    ligneTransition=True
    if 'Dialogue' in ligne:
        if ligneUnique in ligne or not ligneTransition:
            if ligneTransition:
                tempsDebut=derniereLigne.split(",")[2]
                ligneTransition=False
            nombreLignes+=1
        else:
            derniereLigne=ligne

# <codecell>

# print nombreLignes, tempsDebut, tempsFin

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

def changeLigne(chaine):
    champs=chaine.split(',')
    champs[1]=calculChaine(timingDebut+increment*nombreLignes)
    champs[2]=calculChaine(timingDebut+increment*(nombreLignes+1))
    result=",".join(champs)
    return result
        

# <codecell>

timingDebut=calculTemps(tempsDebut)
timingFin=calculTemps(tempsFin)
timing=timingFin-timingDebut

# <codecell>

increment=timing/nombreLignes
# print calculChaine(timingDebut+increment)

# <codecell>

nombreLignes=0
for ligne in lignes:
    ligneTransition=True
    if 'Dialogue' in ligne:
        if ligneUnique in ligne:
#            print "original", ligne
#            print "nouvelle", 
            print changeLigne(ligne)
            nombreLignes+=1
        else:
            print ligne
    else:
        print ligne

# <codecell>


