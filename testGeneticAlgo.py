import matplotlib.pyplot as plt
import numpy as np
import itertools
from random import randint
import random as rn
import curses

plt.ion()
xRange=[0,100]
yRange=[0,100]
#interactionRadius=1
#blue=[[20],[20],[100],[0],[0]]
#red=[[80],[80],[20],[0],[0]]
#red=[[80],[80],[20],[0],[0]]
food=[[50],[50]]
allBlobs=[]
verbose=0
#colz=

class blob:
   def __init__(self, x, y, xdir, ydir, metabolism, volatility, colour, size,fear,reproductivity):
     self.x=x
     self.y=y
     self.xdir=xdir
     self.ydir=ydir
     self.metabolism=abs(metabolism)
     self.volatility=volatility
     self.colour=colour
     self.size=size
     self.fear=fear
     self.reproductivity=max(reproductivity,1)
   
   def procreate(self):
       if (self.size > self.reproductivity*100):
          if verbose: print "ravages of time: procreate: child 1"
          if (rn.uniform(0,1)>0.5):
              variation=0.3
          else :
              variation=0.0
          newcolor1=(max(0,min(1,self.colour[0]+rn.gauss(0.0,variation))),max(0,min(1,self.colour[1]+rn.gauss(0.0,variation))),max(0,(min(1,self.colour[2]+rn.gauss(0.0,variation)))))
          newcolor2=(max(0,min(1,self.colour[0]+rn.gauss(0.0,variation))),max(0,min(1,self.colour[1]+rn.gauss(0.0,variation))),max(0,(min(1,self.colour[2]+rn.gauss(0.0,variation)))))
          ox=rn.uniform(-1,1)
          oy=rn.uniform(-1,1)
          child1=blob(self.x+ox,self.y+oy,rn.gauss(0.0,0.5),rn.gauss(0.0,0.5),self.metabolism+rn.gauss(0.0,variation),self.volatility+rn.gauss(0.0,variation),newcolor1, self.size*0.4, self.fear+rn.gauss(0.0,variation),self.reproductivity+rn.gauss(0.0,variation))
          if verbose: print  "ravages of time: procreate: child 2"
          child2=blob(self.x-ox,self.y-oy,rn.gauss(0.0,0.5),rn.gauss(0.0,0.5),self.metabolism+rn.gauss(0.0,variation),self.volatility+rn.gauss(0.0,variation),newcolor2, self.size*0.4, self.fear+rn.gauss(0.0,variation),self.reproductivity+rn.gauss(0.0,variation))
          if verbose: print  "ravages of time: procreate: append"
          allBlobs.append(child1)
          allBlobs.append(child2)
          if verbose: print  "ravages of time: procreate: delete"
          if self in allBlobs: 
            del allBlobs[allBlobs.index(self)]


   def printStatus(self):
       string= "%d | %3.2f | %.2f | %.2f | %.2f  "%(allBlobs.index(self),  self.size,self.metabolism,self.fear, self.reproductivity)
       return string

   def findNearestFood(self,smellRadius=100):
        minR=100.0
        minRIndex=-1
        for j in range(len(food[0])):
            foodx= food[0][j]
            foody= food[1][j]
            r=((self.x-foodx)**2+(self.y-foody)**2)**(0.5)
            if ((r< minR) and (r<smellRadius)):
              minR=r
              minRIndex=j
        if (minRIndex>-1):
          nearestFoodx= food[0][minRIndex]
          nearestFoody= food[1][minRIndex]
          thisxdir= (nearestFoodx -self.x)/minR
          thisydir= (nearestFoody -self.y)/minR
          return [thisxdir,thisydir]
        else:
          return [self.xdir,self.ydir]
   
   def findNearestBlob(self,smellRadius=30,excludeSameSpecies=False):
        #excluding.append(self)
        minR=100.0
        minRIndex=-1
        for j in range(len(allBlobs)):
            otherBlobx =allBlobs[j].x
            otherBloby =allBlobs[j].y
            r=((self.x-otherBlobx)**2+(self.y-otherBloby)**2)**(0.5)
            if (excludeSameSpecies and allBlobs[j].colour==self.colour ): continue
            if (r==0) : continue
            if ((r< minR) and (r<smellRadius)):
              minR=r
              minRIndex=j
        if (minRIndex>-1):
          nearestBlobx= allBlobs[minRIndex].x
          nearestBloby= allBlobs[minRIndex].y
          thisxdir= (nearestBlobx -self.x)/minR
          thisydir= (nearestBloby -self.y)/minR
          return [thisxdir,thisydir,minRIndex]
        else :
          return [self.xdir,self.ydir,minRIndex]

def applyRavagesOfTime(blobs):
  for blob in blobs[:]:
     if verbose: print  "ravages of time: age"
     blob.size-=0.5*blob.metabolism
     if (blob.size<0): blob.size=1
     if (blob.size <10):
        food[0].append(blob.x)
        food[1].append(blob.y)
        #blob.metabolism=0
        #blob.colour='k'
        del allBlobs[allBlobs.index(blob)] 
     if verbose: print  "ravages of time: procreate"
     blob.procreate()


def moveBlobs(blobs):
   for blob in blobs:
        #blobs[0][i]=blobs[0][i]+randint(-metabolism,metabolism) #x
        #blobs[1][i]=blobs[1][i]+randint(-metabolism,metabolism) #y
        if verbose: print  "moveblobs: find food"
        nearestfood = blob.findNearestFood()
        if verbose: print  "moveblobs: find blob"
        nearestblob = blob.findNearestBlob()
        #if (allBlobs.index(blob)==0):
        #  print "nearestfood", nearestfood , " nearestblob",  nearestblob
        
        blob.xdir =   nearestfood[0]
        blob.ydir =   nearestfood[1]
        if (nearestblob[2]>-1):
          nb=allBlobs[nearestblob[2]]
          if (blob.size == nb.size):
             blob.xdir =   -nearestblob[0]
             blob.ydir =   -nearestblob[1]
          if (blob.fear >= 0):
            hunger=   1- (blob.size-10.0)/blob.size
            if (blob.fear > hunger and  blob.size<nb.size):  
              blob.xdir =   -nearestblob[0]
              blob.ydir =   -nearestblob[1] 
          else:
           nearestblob = blob.findNearestBlob(excludeSameSpecies=True)
           #if (blob.size > (1.0-blob.fear)*nb.size):
           if (blob.size > nb.size):
              blob.xdir =   nearestblob[0]
              blob.ydir =   nearestblob[1]
           else:
              blob.xdir =   -nearestblob[0]
              blob.ydir =   -nearestblob[1]

        if (rn.uniform(0,1)>blob.volatility): blob.xdir=rn.gauss(0,1)
        if (rn.uniform(0,1)>blob.volatility): blob.ydir=rn.gauss(0,1)
        oldx=blob.x
        oldy=blob.y
        blob.x=oldx+blob.metabolism*blob.xdir #x
        blob.y=oldy+blob.metabolism*blob.ydir #y
        #print "old x position ", oldx , " metabolism ", blob.metabolism , " xdir ", blob.xdir , "blob.metabolism*blob.xdir ", blob.metabolism*blob.xdir,  " new x", blob.x
        #print "old y position ", oldy , " metabolism ", blob.metabolism , " ydir ", blob.ydir ," blob.metabolism*blob.ydir " , blob.metabolism*blob.ydir, " new y", blob.y
        if (blob.x<xRange[0]): blob.x = xRange[0] #keep em in the frame
        if (blob.x>xRange[1]): blob.x = xRange[1] #keep em in the frame
        if (blob.y<yRange[0]): blob.y = yRange[0] #keep em in the frame
        if (blob.y>yRange[1]): blob.y = yRange[1] #keep em in the frame

def dropFood():
 diceRoll=rn.uniform(0,1)
 if (diceRoll>0.1 and len(food[0]) < 200):
    food[0].append(randint(0,100))
    food[1].append(randint(0,100))
 print "food dropped!", len(food[0])
    
def interactWithFood(blobs):
    for blob in blobs:
        blobx= blob.x
        bloby= blob.y
        offset=0
        for j in range(len(food[0])):
            foodx= food[0][j-offset]
            foody= food[1][j-offset]
            #print "blob.size ", blob.size
            if (((blobx-foodx)**2+(bloby-foody)**2)**(0.5) < ((blob.size)/(31.4))**0.5 ):
                del food[0][j-offset]
                del food[1][j-offset]
                offset=offset+1
                blob.size= blob.size+15

def interactWithBlobs(blobs):
    for blob in blobs:
        blobx= blob.x
        bloby= blob.y
        offset=0
        for j in range(len(allBlobs)):
            foodx= allBlobs[j-offset].x
            foody= allBlobs[j-offset].y
            foodsize = allBlobs[j-offset].size
            if (allBlobs[j-offset].colour==blob.colour):continue #no cannibals
            if ((((blobx-foodx)**2+(bloby-foody)**2)**(0.5) < ((blob.size)/(31.4))**0.5 ) and (blob.size > 1.2*allBlobs[j-offset].size)):
                del allBlobs[j-offset]
                offset=offset+1
                blob.size= blob.size+0.9*foodsize

 


def pbar(window):
#def pbar():
  allBlobs.append(blob(20,20,0,0,1.0,0.99,(1.0,0.0,0.0),300,-0.1,4.0))
  allBlobs.append(blob(80,80,0,0,0.5,0.99,(0.0,0.0,1.0),50,0.3,1.0))
  redSpeed=0.6
  blueSpeed=0.3
  iterations=0
  while iterations<10000: 
    plt.axis([0, 100, 0, 100])
    iterations=iterations+1
    if verbose: print  "drop food"
    dropFood()
    if verbose: print  "move blobs"
    moveBlobs(allBlobs)
    if verbose: print  "move interact with food"
    interactWithFood(allBlobs)
    interactWithBlobs(allBlobs)
    if verbose: print  "ravages of time"
    applyRavagesOfTime(allBlobs)
    window.addstr(0,0,"b | size  | meta | fear | repro ")
    for b in allBlobs:
      window.addstr(1+allBlobs.index(b), 0, b.printStatus())
      plt.scatter(b.x, b.y, s=b.size, marker='o',c=b.colour)
      label ="%d"%allBlobs.index(b)
      plt.annotate(label, xy = (b.x+0.5, b.y+0.5), xytext = (0, 0), textcoords = 'offset points')
    window.addstr(1+len (allBlobs),0,"-----------------------------------------")
    #plt.scatter(blue[0], blue[1], s=blue[2], marker='o',c='b')
    #plt.scatter(red[0], red[1], s=red[2], marker='o',c='r')
    plt.scatter(food[0], food[1], s=5, marker='^',c='g')
    plt.annotate('Time=%d'%iterations, xy=(0.5, 1.1), xycoords='axes fraction')
    plt.pause(0.01)
    window.refresh()
    plt.clf()


curses.wrapper(pbar)
#pbar()
