#!/usr/bin/env sage

import sys
from sage.all import *
import itertools as it

def cost(s,G,V,n,bestSolution):
    print('trying the solution: ')
    print(s)
    print('while the best one is: '+str(bestSolution))
    cost=0
    t=True
    while cost<bestSolution and t:
        Ai=[]
        Zi=[]
        Yi=[]
        i=0
        while i<(n-1):
            vi=V[i]
            Yi=[]
            for u in Ai:
                P=G.all_paths(vi,u)
                #problem is that the lenght at first is one but later cannot be one
                #ie in case of a square the third searched vertex we need to remove
                #the second searched vertex
                for p in P:
                    if len(p)>1:
                        for x in range(1,len(p)):
                            if (p[x] in Ai) and p[x]!=vi and x<len(p):
                                firstGuardIndex=p.index(p[x])
                                break
                            x=x+1
                        if not(p[firstGuardIndex] in Yi):
                            Yi.append(p[firstGuardIndex])
            Ai.append(vi)
            print('at interval: '+ str(i)+ ' Ai is: '+ str(Ai))
            Zi=Yi
            Zi.append(vi)
            print('at interval: '+ str(i)+ ' Zi is: '+ str(Zi))
            cost=cost+len(Zi)
            i=i+1
        t=False
    if cost<bestSolution:
        return cost
    else:
        return bestSolution

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

print(G.adjacency_matrix())

V=G.vertices()
n=len(V)
solutions=list(it.permutations(V))
bestSolution=-1
if len(solutions)>0:
    s=solutions[0]
    bestSolution=cost(s,G,V,n,999999)
for sIndex in range(1,len(solutions)):
    s=solutions[sIndex]
    bestSolution=cost(s,G,V,n,bestSolution)
print('best solution has cost: '+str(bestSolution))
