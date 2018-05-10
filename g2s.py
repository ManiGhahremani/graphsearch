#! /usr/bin/python

import os
i="o"
o="s"

iending='.graph'
oending='.sage'

finfilename=i+iending
foutfilename=o+oending

fin=open(finfilename,"r")
fout=open(foutfilename,"w")

thisEntry=""
text=""

graph=fin.readlines()
for e in range(0, len(graph)):
	thisE=graph[e]
	thisE.replace("\n","")
	endpoint1=thisE.split(' ')[0]
	endpoint2=thisE.split(' ')[1]
	if endpoint1!=thisEntry and e!=0:
		text=text+'],'
		thisEntry=endpoint1
		text=text+thisEntry+':['
	elif e==0:
		thisEntry=endpoint1
		text=text+thisEntry+':['
	else:
		text=text+','
	text=text+endpoint2

text=text+']'
text=text.replace('\n','').replace('\t','')
begtext='G=Graph({'
endtext='})'
text=begtext+text+endtext
fout.write(text)
fout.close()


