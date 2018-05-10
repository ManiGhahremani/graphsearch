#! /usr/bin/python

import os


i="x"
o="o"

iending='.adj'
oending='.graph'

finfilename=i+iending
foutfilename=o+oending

fin=open(finfilename,"r")
fout=open(foutfilename,"w")

adjacency=fin.readlines()
for r in range(0, len(adjacency)):
	row=adjacency[r]
	row=row.replace(" ","").replace(",","")
	for c in range(0, len(row)):
		endpoint=row[c]
		if endpoint=='1' and r<c:
			edge=str(r)+" "+str(c)
			fout.write(edge+'\n')

fout.close()


