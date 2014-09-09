# -*- coding: utf-8 -*-


import sys, re
import codecs
import time, datetime


from collections import defaultdict
from operator import itemgetter


if len(sys.argv) <> 3:
	print 'Please provide action file and rythme(actions per time) *output* file' 
	sys.exit()

try:
    rugby=codecs.open(sys.argv[1],"r", "utf-8") 
    
except IOError:
    print 'I could not open the file', sys.argv[1]
    sys.exit()

try:
        rythme=codecs.open(sys.argv[2], "w", "utf-8")
except IOError:
        print 'I could not find', sys.argv[2], 'file'

#####
def time2secs(seq): # seq is a timedelta
        sec=getattr(seq, "seconds")
        msec=getattr(seq, "microseconds")
        seconds=int(sec)+float(msec)/1000000
        return seconds

def nested_dict_form(): 
  return defaultdict(int)
def nested_dict2(): 
  return defaultdict(nested_dict_form)



FinActDebComm = []
act={}
actcomm=defaultdict(nested_dict_form)
eveComm= defaultdict(nested_dict_form)
times=[] # list of all intervals
actions=[] # list of action-slots
events = [] # list of event-slots
comments = [] # list of comment-slots
texts = [] # list of turn-slots
for line in rugby:
        line=line.strip().encode("utf-8")
        champs=line.split(";")
        action=champs[5].strip('"')
        action=action.strip()
        debut=champs[0].strip('"')
        fin=champs[1].strip('"')
        event=champs[4].strip('"')
        event=event.lower().strip()
        comment=champs[6].strip('"')
        comment=comment.lower().strip()
        text=champs[7].strip('"')
        text=text.strip()
        if debut != "Début" and fin != "Fin":
                db, mSecd = debut.split(".")
                db = datetime.datetime(*time.strptime(db, "%H:%M:%S")[0:6])
                mSecond = datetime.timedelta(microseconds = int(mSecd)*10000)
                dbfull = db + mSecond
                fn, mSecf = fin.split(".")
                fn = datetime.datetime(*time.strptime(fn, "%H:%M:%S")[0:6])
                mSeconf = datetime.timedelta(microseconds = int(mSecf)*10000)
                fnfull = fn + mSeconf
                duree = fnfull-dbfull
                times.append((debut, fin,duree))
                texts.append(text)
        if action.startswith('A-'):
                action1=action[6:]
                action1= action1.lower().strip()
                actions.append((action, action1))
                events.append(event)
                comments.append(comment)
        elif action != "Actions": 
                action1 = action.lower().strip()
                actions.append((action, action1)) #ak: empty isn't an action
                events.append(event)
                comments.append(comment)


actTime=[] # le fichier entier
# non-actions
nonActions= ['', "ralenti", "replay", "hors-jeu", "hors jeu", "mi-temps", "stade", "terrain"] 
it = 0
while it < len(actions):
        actTime.append([actions[it],times[it],events[it], comments[it], texts[it]])
        it+=1


# actions per time interval:

before=2 # time before in secs
after=3  # time after in secs 
tb= time2secs(datetime.timedelta(seconds=before))
ta= time2secs(datetime.timedelta(seconds=after))

intervalT= datetime.timedelta(seconds=before+after)
intervalT= time2secs(intervalT)

rythme.write(";;;;;;tempsInterval: "+str(intervalT)+" secs;dont "+str(before)+" secs avant;"+str(after)+" secs apres action actuelle;\n")
rythme.write("debut;fin;duree;event;Nr action;action;Nr ActionsDansInterval;actionsAvant;actionsApres;commentataires;text\n")
i=0

while (i < len(actTime)):
        t = time2secs(actTime[i][1][2]) # time of action
        td = actTime[i][1][0] # start time
        tf = actTime[i][1][1] # end time
        a = actTime[i][0][1].decode("utf-8")
        aNr = actTime[i][0][0].decode("utf-8")
        evt = actTime[i][2].decode("utf-8")
        spk = actTime[i][3].decode("utf-8")
        txt = actTime[i][4].decode("utf-8")
        if spk.startswith("spk1"): Spk= "spk1"
        elif spk.startswith("spk2"): Spk= "spk2"
        elif spk.startswith("spk3"): Spk= "spk3"
        else: Spk = "none"
        count=1

        # events & comments
        rev = re.match(r"\d+ (.*)", evt)
        if rev:
                evI = rev.group(1).strip() # event type
                if evI != "mi-temps":
                        if evI in eveComm and evt in eveComm[evI]:
                                eveComm[evI][evt].append(Spk)
                        else:
                                eveComm[evI][evt]= [Spk]
        
        if a in nonActions:
                rythme.write(td+";"+tf+";"+str(t)+";"+evt+";"+aNr+";"+a+";;;;"+spk+";"+txt+"\n")
        elif t >= intervalT:                
                rythme.write(td+";"+tf+";"+str(t)+";"+evt+";"+aNr+";"+a+";"+str(count)+";0;0;"+spk+";"+txt+"\n")
                
                if a in actcomm and Spk in actcomm[a]:
                        actcomm[a][Spk]+=1
                else:
                        actcomm[a][Spk]=1
        else:
                countb=0 
                k=1 # we count only *preceding* actions; the current one is put apart
                # preceding actions
                rest = tb - 0.5*t
                while (rest > 0 and i-k >= 0): 
                        if actTime[i-k][0][1] not in nonActions:
                                rest = rest - time2secs(actTime[i-k][1][2])
                                # ak: if rest > 0: # add to general count only if the action completed
                                countb+=1
                                 
                        k+=1
                # following actions
                counta=0
                j=1 # we count only *following* actions
                rest = ta - 0.5*t
                while (rest > 0 and i+j < len(actTime)):
                        if actTime[i+j][0][1] not in nonActions:
                                rest = rest - time2secs(actTime[i+j][1][2])
                                # ak: if rest > 0: # ak: if commented, counts all *started* actions
                                counta+=1
                        j+=1
                count = count+countb+counta
                if a in actcomm and Spk in actcomm[a]:
                        actcomm[a][Spk]+=1
                else:
                        actcomm[a][Spk]=1

                rythme.write(td+";"+tf+";"+str(t)+";"+evt+";"+aNr+";"+a+";"+str(count)+";"+str(countb)+";"+str(counta)+";"+spk+";"+txt+"\n")
        i+=1
rythme.close()

print "Action;% commentees;totalActions;spk1;spk2;spk3;non-commentees"
for act in actcomm:
        total= sum(actcomm[act].values())
        print act.encode("utf-8")+";",
        if "none" in actcomm[act]:
                comment = total - actcomm[act]["none"]
                proc = float(comment)*100/total
                print "%3.2f %%;%d;" %(proc, total),
        else:
                proc = 100
                print "%3.2f %%;%d;" %(proc,total),
        for s in ["spk1", "spk2","spk3","none"]:
                if s in actcomm[act]:
                        print str(actcomm[act][s])+";",
                else:
                        print ";",
        print

print
print 
print "Event;total;commented;pourcentage commented;spk1;spk2;spk3;no comment"
com = defaultdict(nested_dict_form)
for e in eveComm:
        proc = 0
        total= len(eveComm[e].keys())
        print e.encode("utf-8")+";",
        for ei in eveComm[e]:
                commented= " ".join(eveComm[e][ei])
                commented = commented.replace("none", "")
                commented = commented.strip()
                if commented != "":
                        proc+=1
                comts=commented.split()
                comts=set(comts) # no duplicates for an event
                for c in comts:
                        if e in com and c in com[e]:
                                com[e][c]+=1
                        else:
                                com[e][c]=1
        print "%d;%d;%3.2f %%;" %(total, proc, float(proc)*100/total),
        for s in ["spk1", "spk2","spk3"]:
                print "%d;" %com[e][s],
        print "%d" %(total-proc),
        print
 

# time of a fixed number of actions
##Abefore=2
##Aafter=3
##print ";",Abefore,"actions avant et",Aafter,"actions apres"
##print "Action;tempsActionsAutour"
##n=Abefore # 0  
##while(n< len(actTime)-Aafter):  # controls window size to prevent index errors
##        t = actTime[n][1]
##        a = actTime[n][0] #.decode("utf-8")
##        if n < Abefore or n >= len(actTime)-Aafter: # if the action number incorrect, gets only time of the current action
##               print a+";"+str(time2secs(t))
##        else:
##                m=0
##                while (m < Abefore):
##                        t+= actTime[n-m-1][1]
##                        m+=1
##                k= 1
##                while (k<= Aafter):
##                        t+= actTime[n+k][1]
##                        k+=1
##                print a+";"+str(time2secs(t))
##        n+=1
##        
