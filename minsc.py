#!/usr/bin/env sage
import sys
from sage.all import *
from itertools import permutations

global bests
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
    global Zirec
    thisZirec=[]
    #print('Solution is %s and bestSolution is %d' % (s,int(bestSolution)))
    Ai=[]
    cost=0
    busy=True
    i=0
    while i<n and busy:
        Zi=[]
        vi=V[s[i]]
        vc=Compvi(vi,Ai,G)
        Nvc=[]
        Nvc=NofX(vc,G)
        for guard in Nvc:
            Zi.append(guard)
        thisZireccopy=thisZirec
        thisZireccopy.append(Zi)
        thisZirec=thisZireccopy
        Ai.append(vi)
        #print('     Ai is %s at %d' % (Ai,int(i)))
        #print('     Zi is %s at %d' % (Zi,int(i)))
        if cost+len(Zi)>=bestSolution:
            cost=99999999
            busy=False
        else:
            cost=cost+len(Zi)
        i=i+1
    if cost<bestSolution:
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
progress=0
solutions=sorted(list(it.permutations(V)))
O=len(solutions)
bestSolution=99999999
for sIndex in range(0,O):
    newprogress=(sIndex*100)/O
    if not(newprogress==progress):
        progress=newprogress
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        print('progress: %d' % progress)
    s=solutions[sIndex]
    bestSolution=cost(s,G,V,n,bestSolution)
print('Best solution has cost %d and is %s' % (bestSolution, bests))
print(Zirec)
