# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from lxml import etree

# <codecell>

fichierTranscription=open("../France_Argentine_ANNOT-REF_essai.trs","r")
# fichierTranscription=open("./TEST-lxml.xml","r")
xmlTranscription=fichierTranscription.read()
# print xmlTranscription

# <codecell>

root=etree.XML(xmlTranscription)

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
printSelection="Section"

numSection=0
numTurn=0
numSync=0
for stype,stopic,sstart,send,turns in sections:
    numSection+=1
#    print "Section",numSection,stype,stopic,sstart,send
    if printSelection=="Section":
    	print sstart,";",send,";",stype,";",stopic
    numTurnIn=0
    for tstart,tend,speaker,text in turns:
        numTurn+=1
        numTurnIn+=1
#        print "\tTurn",numTurn,tstart, tend, speaker
        if printSelection=="Turn":
        	print tstart,";",tend,";",speaker
        numSyncIn=0
        for sync in text:
            numSync+=1
            numSyncIn+=1
#            print "\t\tSync",numSync, sync[0], sync[1], sync[2]
            if printSelection=="Sync":
            	print sync[0],";", sync[1],";", sync[2].encode("utf8")

# <codecell>


