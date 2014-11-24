
# coding: utf-8

# #Mise en forme pour un graphe à barres de largeur variable

# In[37]:

import codecs,sys

sep="\t"


# In[38]:

File="/Users/gilles/Downloads/MotsDureeSpeaker.csv"
try:
    fileContent=codecs.open(File,"r", "utf-8") 

except IOError:
    print 'I could not open the file', colonnesFile
    sys.exit()


# ###Calcul de l'indice de temps en centièmes de secondes
# 
# - calcul des centièmes
# - différence avec le temps initial

# In[39]:

base=0
def formatTime(date):
    jour,instant=date.split(" ")
    heures, minutes, secmil = instant.split(":")
    if "." in secmil:
        secondes, milliemes=secmil.split(".")
    else:
        secondes=secmil
        milliemes="0"
    numero=int(milliemes)/10000+100*int(secondes)+6000*int(minutes)+360000*int(heures)
    return numero-base

def formatLine(line):
    champs=line.split(sep)
    debut=str(formatTime(champs[1]))
    fin=str(formatTime(champs[2]))
    valeurs=[]
    zeros=[]
    for champ in champs[3:]:
        valeur=champ.strip()
        if valeur=="" :
            valeurs.append("0")
        else:
            valeurs.append(valeur)
        zeros.append("0")
    return (debut, fin, valeurs, zeros)


# ###Transformation des lignes
# 
# - au départ on a une ligne avec le début et la fin pour les 3 valeurs
# - à l'arrivée on a quatre lignes
#  - le début avec des zéros
#  - le début avec les 3 valeurs
#  - la fin avec les 3 valeurs
#  - la fin avec des zéros

# In[40]:

lignes=fileContent.readlines()
titres=lignes[0].split("\t")
print titres[1].encode("utf8")+sep+sep.join(titres[3:]).encode("utf8").strip()
champs=formatLine(lignes[1])
base=int(champs[0])
for ligne in lignes[1:]:
    (debut,fin,valeurs,zeros)=formatLine(ligne)
    if valeurs!=zeros:
        print debut+sep+sep.join(zeros)
        print debut+sep+sep.join(valeurs)
        print fin+sep+sep.join(valeurs)
        print fin+sep+sep.join(zeros)


# In[40]:



