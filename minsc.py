#!/usr/bin/env sage

import sys
from sage.all import *
import itertools as it

global bests
global bads
global badsi
global Zirec
Zirec=[]

def NofX(X,G):
    NofX=[]
    for x in X:
        Nx=[]
        Nx=G.neighbors(x)
        for nx in Nx:
            if nx not in X and nx not in NofX:
                NofX.append(nx)
    return NofX

def Compvi(vi,Ai,G):
    Gcopy=copy(G)
    Gcopy.delete_vertices(Ai)
    vc=Gcopy.connected_component_containing_vertex(vi)
    return vc

def cost(s,G,V,n,bestSolution):
    global bests
    global bads
    global badsi
    global Zirec
    thisZirec=[]
    print('Solution is %s and bestSolution is %d' % (s,int(bestSolution)))
    Ai=[]
    cost=0
    busy=True
    i=0
    while i<n-1 and busy:
        Zi=[]
        vi=V[s[i]]
        vc=Compvi(vi,Ai,G)
        Ai.append(vi)
        candids=[]
        candids=NofX(vc,G)
        for c in candids:
            count=0
            neighbors=G.neighbors(c)
            for neighbor in neighbors:
                if not(neighbor==vi) and neighbor not in Ai:
                    count=count+1
            if count>0 and c not in Zi:
                Zi.append(c)
        Zi.append(vi)
        thisZireccopy=thisZirec
        thisZireccopy.append(Zi)
        thisZirec=thisZireccopy
        print('     Ai is %s at %d' % (Ai,int(i)))
        print('     Zi is %s at %d' % (Zi,int(i)))
        if cost+len(Zi)>=bestSolution:
            bads=s
            badsi=i
            cost=99999999
            busy=False
        else:
            cost=cost+len(Zi)
        i=i+1
    if cost<bestSolution:
        Ai.append(V[s[len(s)-1]])
        bests=Ai
        Zirec=thisZirec
        return cost
    else:
        return bestSolution

#init
inname="o"
iending='.graph'
finfilename=inname+iending
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
solutions=sorted(list(it.permutations(V)))
bestSolution=0
if len(solutions)>0:
    s=solutions[0]
    bestSolution=cost(s,G,V,n,99999999)
    bads=s
    badsi=len(bads)-1
for sIndex in range(1,len(solutions)):
    s=solutions[sIndex]
    new=False
    for p in range(badsi+1):
        if not(s[p]==bads[p]):
            new=True
    if new==True:
        bestSolution=cost(s,G,V,n,bestSolution)
print('Best solution has cost %d and is %s' % (bestSolution, bests))
print(Zirec)
