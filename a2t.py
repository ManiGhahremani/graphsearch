#! /usr/bin/python

import os
cwd = os.getcwd()
print cwd

i="x"
o="t"

iending='.adj'
oending='.gr'

finfilename=i+iending
foutfilename=o+oending

fin=open(finfilename,"r")
fout=open(foutfilename,"w")
adjacency=fin.readlines()
fout.write('p tw '+str(len(adjacency)))
text=''
m=0
for r in range(0, len(adjacency)):
	row=adjacency[r]
	row=row.replace(" ","").replace(",","")
	for c in range(0, len(row)):
		endpoint=row[c]
		if endpoint=='1' and r<c:
			m=m+1
			edge=str(r+1)+" "+str(c+1)
			text=text+edge
			text=text+'\n'
fout.write(' '+str(m)+'\n')
fout.write(text)
fout.close()


