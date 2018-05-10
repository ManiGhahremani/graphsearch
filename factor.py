#!/usr/bin/env sage

import sys
from sage.all import *
import itertools as it

global Airec
global AirecP
global Zirec
global si
si=0
Airec=[]
AirecP=[]
Zirec=[]

def NofX(X,G):
    NofX=[]
    for x in X:
        Nx=[]
        Nx=G.neighbors(x)
        for nx in Nx:
            if nx not in X:
                if nx not in NofX:
                    NofX.append(nx)
    return NofX

def countNinC(u,C,G):
    count=0
    Nu=G.neighbors(u)
    for nu in Nu:
        if nu in C:
            count=count+1
    return count


def cost(s,G,V,n,bestSolution):
    global Zirec
    global Airec
    global si
    cost=0
    busy=True
    thisAirec=[]
    thisZirec=[]
    Ai=[]
    Zi=[]
    Yi=[]
    i=0
    while i<=(n-1) and busy:
        vi=V[s[i]]
        Gcopy=copy(G)
        Gcopy.delete_vertices(Ai)
        vc=Gcopy.connected_component_containing_vertex(vi)
        nofx=NofX(vc,G)
        Zi=nofx
        thisZirec.append(Zi)
        Ai.append(vi)
        thisAirec.append(Ai)
        if cost+len(Zi)>=bestSolution:
            cost=99999999
            si=i
            AirecP=Ai
            busy=False
        else:
            cost=cost+len(Zi)
        i=i+1
    if cost<bestSolution:
        Airec=Ai
        Zirec=thisZirec
        return cost
    else:
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
#calculations
solutions=list(it.permutations(V))
bestSolution=-1
if len(solutions)>0:
    s=solutions[0]
    bestSolution=cost(s,G,V,n,99999999)
for sIndex in range(1,len(solutions)):
    s=solutions[sIndex]
    new=False
    for pos in range(0,si):
        if s[pos]!=AirecP[pos]:
            new=True
    if new:
        bestSolution=cost(s,G,V,n,bestSolution)
print('best solution has cost: '+str(bestSolution))
print('Zi:')
print(Zirec)
print('Ai:')
print(Airec)
