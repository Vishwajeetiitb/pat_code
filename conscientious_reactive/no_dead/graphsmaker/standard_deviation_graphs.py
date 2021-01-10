import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data/'

cars = [1,2,4,6,10]
deads = [0,2,12]
num_runs = 5
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir+'cr'+str(car)+'/'+str(dead)+'dead/'
		runs = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][5000:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		avg.append(np.mean(graph_idlness))
		std.append(np.std(graph_idlness))
	#avg = np.array(avg)
	#std = np.array(std)
	plt.figure()
	plt.plot(cars, avg, 'b--')
	plt.errorbar(cars, avg,yerr=std,  fmt='o', ecolor='g', capthick=1.0)
	plt.title("standard deviation of idleness with varying runs and agents")
	plt.xlabel("number of agents")
	plt.ylabel("graph idleness")
	# plt.show()
	plt.savefig('dead'+str(dead)+'_new.png', dpi = 100)
	


		


