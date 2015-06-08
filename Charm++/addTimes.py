#!/usr/bin/env python
import subprocess
import os
import re

def addTimes(stringFile):
	numbers = []
	times = []
	y = 0

	with open(stringFile,"r") as fichier:
		for line in fichier:
			if re.match("^\d+?\.\d+?$", line) is not None:
				numbers.append(line)

	for strings in numbers:
		if (strings != '\n'):
			x = float(strings)
			times.append(x)

	for t in times:
		y = y+t

	return y
	fichier.close()

def run():
	nsleep = [0,1,2]
	nTasks = [1,10,100,1000,10000,100000]
	for sleep in nsleep:
		for task in nTasks:
			full_path = os.path.realpath(__file__)
			file_path = '%s/TestTimes%d:%d' % (os.path.dirname(full_path),task,sleep)
			if not os.path.exists(file_path):
				os.makedirs(file_path) 
			name=file_path+"/TestTimes.txt"
			with open(name,'a+') as fil:
				subprocess.Popen("./charmrun hello %d %d 2>/dev/null 1>%s" %(task,sleep,name),shell=True)
				fil.close()
				print(name +":" +str(addTimes(name))+"s")
	return 0

truc = addTimes("TestTimes.txt")
print(truc)



