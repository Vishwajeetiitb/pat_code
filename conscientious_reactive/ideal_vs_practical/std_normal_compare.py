import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir1 ='./data/'
rootdir2 ='./no_dead_data/'

cars = [1,2,4,6,10]
deads = [0,2,12]
no_deads = [26]
num_runs = 5
avg = []
avg2 = []
for dead in deads:
	avg1 = []
	for car in cars:
		path1 = rootdir1+'cr'+str(car)+'/'+str(dead)+'dead/'
		runs1 = []
		instantaneous_node_idleness1 = []
		for i in range(num_runs):
			runs1.append(np.array(pd.read_excel(pd.ExcelFile(path1+'run'+str(i)+'/run.xlsx'))))
			runs1[i] = runs1[i][500:][:,1:]
			instantaneous_node_idleness1.append(np.mean(runs1[i],axis=1))
		graph_idlness1 = np.mean(instantaneous_node_idleness1,axis=1)
		graph_idlness1 = np.array(graph_idlness1)*car/25
		avg1.append(np.mean(graph_idlness1))
	avg.append(avg1)

for dead in no_deads:
	
	for car in cars:
		path2 = rootdir2+'cr'+str(car)+'/'+str(dead)+'dead/'
		runs2 = []
		instantaneous_node_idleness2 = []
		for i in range(num_runs):
			runs2.append(np.array(pd.read_excel(pd.ExcelFile(path2+'run'+str(i)+'/run.xlsx'))))
			runs2[i] = runs2[i][500:][:,1:]
			instantaneous_node_idleness2.append(np.mean(runs2[i],axis=1))
		graph_idlness2 = np.mean(instantaneous_node_idleness2,axis=1)
		graph_idlness2 = np.array(graph_idlness2)*car/25
		avg2.append(np.mean(graph_idlness2))
		# std.append(np.std(graph_idlness))
	#avg = np.array(avg)
	#std = np.array(std)
	#avg1 = np.array(avg1)
	#avg2 = np.array(avg2)
	
for dead in range(len(deads)):
	plt.figure()
	print(avg)
	print(avg2)
	# plt.errorbar(cars, avg,yerr=std, ecolor='g', capthick=1.0)
	plt.plot(cars, avg[dead],label = 'practical')
	plt.plot(cars, avg2, label = 'ideal')
	plt.legend()
	plt.title("ideal vs practical")
	plt.xlabel("number of agents")
	plt.ylabel("graph idleness")
	# plt.show()
	plt.savefig('comparison with std normalized'+str(dead)+'_new.png', dpi=100)


		


