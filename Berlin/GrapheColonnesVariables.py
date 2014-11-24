
# coding: utf-8

# In[79]:

import codecs,sys


# In[80]:

File="/Users/gilles/Downloads/ToursDureeSpeaker.csv"
try:
    fileContent=codecs.open(File,"r", "utf-8") 

except IOError:
    print 'I could not open the file', colonnesFile
    sys.exit()


# In[81]:

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


# In[82]:

lignes=fileContent.readlines()
(num,debut,fin,spk1,spk2,spk3)=lignes[1].split("\t")
base=formatTime(debut)
print "%s\t%s\t%s\t%s"%("Temps","Spk1","Spk2","Spk3")
for ligne in lignes[1:]:
#    print ligne.strip().split("\t")
    (num,debut,fin,spk1,spk2,spk3)=ligne.split("\t")
    if spk1.strip()=="": spk1="0"
    if spk2.strip()=="": spk2="0"
    if spk3.strip()=="": spk3="0"
    
    print "%s\t%s\t%s\t%s"%(formatTime(debut),"0","0","0")
    print "%s\t%s\t%s\t%s"%(formatTime(debut),spk1,spk2,spk3)
    print "%s\t%s\t%s\t%s"%(formatTime(fin),spk1,spk2,spk3)
    print "%s\t%s\t%s\t%s"%(formatTime(fin),"0","0","0")


# In[82]:



