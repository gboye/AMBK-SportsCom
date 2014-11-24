# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Conversion d'une transcription à un fichier de sous-titres SRT V1.0

# <codecell>

from lxml import etree

# <codecell>

fichierTranscription=open("../AnnotationsCommentaires/France_Argentine_ANNOT-REF_Révisé.trs","r")
# fichierTranscription=open("./TEST-lxml.xml","r")
xmlTranscription=fichierTranscription.read()
# print xmlTranscription

# <codecell>

root=etree.XML(xmlTranscription)

# <codecell>

def calculChaine(chaineTemps):
    temps=float(chaineTemps)
    heures=temps//3600
    reste=temps-heures*3600
    minutes=reste//60
    secondes=reste-minutes*60
    milliemes=1000*(secondes-int(secondes))
    secondes=int(secondes)
    result="%02d:%02d:%02d,%03d" % (heures,minutes,secondes,milliemes)
    return result

# <codecell>

Topics=root[1]
Episodes=root[2]
sections=[]
for section in Episodes.findall('Section'):
	sectionType=section.get('type')
	sectionTopic=section.get('topic')
	sectionStart=section.get('startTime')
	sectionEnd=section.get('endTime')
	turns=[]
	for turn in section.findall('Turn'):
		speaker=turn.get('speaker')
		if speaker:
			speakers=speaker.split(" ")
		else:
			speakers=[""]
		startTime=turn.get('startTime')
		endTime=turn.get('endTime')
		syncs=[]
		whos=0
		for element in turn.iter():
			if element.tag=="Sync":
				syncs.append((element.get('time'),speakers[0]))
			elif element.tag=="Who":
				whos+=1
				if whos>1:
					syncs.append((syncs[-1][0],speakers[-1]))
			elif element.tag!="Turn":
				contents=[element.tag]
				for attrib in element.attrib:
					contents.append(attrib)
					contents.append(element.attrib[attrib])
				content=" ".join(contents)
				syncs.append((syncs[-1][0],content))
		texts=[]
		for text in turn.itertext():
			if text!="\n":
				texts.append(text.strip("\n"))
		elements=[]
		for i in range(len(texts)):
			elements.append((syncs[i][0],syncs[i][1],texts[i]))
		turns.append((startTime,endTime,speaker,elements))
	sections.append((sectionType,sectionTopic,sectionStart,sectionEnd,turns))

# <codecell>

printSelection="Sync"

numSection=0
numTurn=0
numSync=0
nSync={}
for stype,stopic,sstart,send,turns in sections:
	numSection+=1
#	 print "Section",numSection,stype,stopic,sstart,send
	if printSelection=="Section":
		print sstart,";",send,";",stype,";",stopic
	numTurnIn=0
	for tstart,tend,speaker,text in turns:
		if speaker not in nSync:
			nSync[speaker]=0
		numTurn+=1
		numTurnIn+=1
#		 print "\tTurn",numTurn,tstart, tend, speaker
		if printSelection=="Turn":
			print tstart,";",tend,";",speaker
		numSyncIn=0
		for sync in text:
#			 print "\t\tSync",numSync, sync[0], sync[1], sync[2]
			if printSelection=="Sync" and sync[1]!="":
				numSync+=1
				numSyncIn+=1
				print numSync
				print calculChaine(sync[0]),"-->", calculChaine(tend)
				if sync[1]!="" and sync[1] in nSync:
					nSync[sync[1]]+=1
					print sync[1]+"-%03d "%nSync[sync[1]],
				print sync[2].encode("utf8")
				print

# <codecell>


