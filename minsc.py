#!/usr/bin/env sage

import sys
from sage.all import *
import itertools as it

def NofuOutsideU(u,U,G):
    NofuoU=[]
    Nofu=[]
    Nofu=G.neighbors(u)
    NofuoU=list(set(Nofu).difference(set(U)))
    return NofuoU

def NofX(X,G):
    NofX=[]
    for x in X:
        NofxoX=NofuOutsideU(x,X,G)
        for n in NofxoX:
            if n not in NofX:
                NofX.append(n)
    return NofX

def Compvi(vi,Ai,G):
    if vi in Ai:
        Ai.remove(vi)
    Gcopy=copy(G)
    Gcopy.delete_vertices(Ai)
    vc=Gcopy.connected_component_containing_vertex(vi)
    return vc

def rmSpare(initCandids,Ai,G):
    #initCandids hold N(vc) and Ai contains vi
    #check if initCandids is indeed subset of Ai
    if not(set(initCandids).issubset(set(Ai))):
        raise ValueError('!!!!!!!!!!!!!!!initCandids %s was not subset of Ai %s' % (initCandids,Ai))
    #Zi must be subset of initcandids that see other vertices in vc
    Zi=[]
    for c in initCandids:
        NofcoAi=NofuOutsideU(c,Ai,G)
        if len(NofcoAi)>0 and c not in Zi:
            Zi.append(c)
    return Zi

def Zigen(vi,Ai,G):
    Zi=[]
    #check if vi is already clean
    if vi not in Ai:
        raise ValueError('!!!!!!!!!!!!!!!Ai %s does not contain vi %d' % (Ai,int(vi)))
    #define the dirty area in which f can awake after placing s on vi
    vc=Compvi(vi,Ai,G)
    #N(vc) is the border of the dirty area
    initCandids=NofX(vc,G)
    #not all N(vc) have to be guarded as there is s on vi
    Zi=rmSpare(initCandids,Ai,G)
    return Zi

def cost(s,G,V,n,bestSolution):
    print('SSSSSS-solution is %s and bestSolution is %d' % (list(s),int(bestSolution)))
    Ai=[]
    Zi=[]
    cost=0
    busy=True
    i=0
    while i<(n-1) and busy:
        vi=V[s[i]]
        Ai.append(vi)
        print('AAAAAA-Ai is %s at %d' % (list(Ai),int(i)))
        Zi=Zigen(vi,Ai,G)
        print('ZZZZZZ-Zi is %s at %d' % (list(Zi),int(i)))
        if cost+len(Zi)>=bestSolution:
            print('CCOSTT-cost went over to %d by adding vi %d at time %d broke loop' % (int(cost+len(Zi)),int(vi),int(i)))
            cost=99999999
            busy=False
        else:
            cost=cost+len(Zi)
        i=i+1
    if cost<bestSolution:
        print('YYYYYY-cost of solution is %s is %d and is best now' % (list(s),int(cost)))
        return cost
    else:
        print('NNNNNN-cost of solution is %s is too much should be an error up there' % (list(s)))
        return bestSolution

#init
i="o"
iending='.graph'
finfilename=i+iending
fin=open(finfilename,"r")
thisEntry=""
text=""
G=Graph({})
graph=fin.readlines()
for e in range(0, len(graph)):
    thisE=graph[e]
    thisE.replace("\n","")
    endpoint1=thisE.split(' ')[0]
    endpoint2=thisE.split(' ')[1]
    if endpoint1!=thisEntry or e==0:
        thisEntry=endpoint1
        G.add_vertices([int(endpoint1)])
        G.add_vertices([int(endpoint2)])
        G.add_edge((int(thisEntry),int(endpoint2)))
    else:
        G.add_vertices([int(endpoint2)])
        G.add_edge((int(thisEntry),int(endpoint2)))
V=G.vertices()
n=len(V)
pic=G.plot()
pic.save('pic.png')

#calculations
solutions=list(it.permutations(V))
bestSolution=0
if len(solutions)>0:
    s=solutions[0]
    bestSolution=cost(s,G,V,n,99999999)
for sIndex in range(1,len(solutions)):
    bestSolution=cost(s,G,V,n,bestSolution)
print('TTTTTTERMINATE-best solution has cost: '+str(bestSolution))
