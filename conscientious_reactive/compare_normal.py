import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir1 ='/home/arms03/Documents/patrolling_vishwajeet_dikshant/pat_code/conscientious_reactive/dual_failure_random_dead/data_3/'
rootdir2 = '/home/arms03/Documents/patrolling_vishwajeet_dikshant/pat_code/conscientious_reactive/dual_failure_random_dead_asymmetric_length/data/'

cars = [1, 2, 4, 5, 6, 7, 8, 10, 12]
deads = [0,5,12,20,25]
num_runs = 8
plt.figure()
for dead in deads:
	avg_norm = []
	std_norm = []
	for car in cars:
		path = rootdir1+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
		runs = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			print(path+'run'+str(i)+'/run.xlsx')
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][500:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		graph_idlness = np.array(graph_idlness)*car/25
		avg_norm.append(np.mean(graph_idlness))
		std_norm.append(np.std(graph_idlness))
	print(avg_norm)
	plt.plot(cars, avg_norm, '-',label ="no of device failures ="+str(dead)+" for equal length")
	plt.draw()
for dead in deads:
	avg_norm = []
	std_norm = []
	for car in cars:
		path = rootdir2+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
		runs = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			print(path+'run'+str(i)+'/run.xlsx')
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][500:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		graph_idlness = np.array(graph_idlness)*car/25
		avg_norm.append(np.mean(graph_idlness))
		std_norm.append(np.std(graph_idlness))
	print(avg_norm)
	plt.plot(cars, avg_norm,'--', label ="no of device failures ="+str(dead)+" for varying length")
	plt.draw()

# plt.figure()
# plt.plot(cars, avg_norm, 'b--')
# plt.errorbar(cars, avg_norm,yerr=std_norm,  fmt='o', ecolor='g', capthick=1.0)
plt.title("comparison in normalized idleness for symmetric and asymmetric maps")
plt.xlabel("number of agents")
plt.ylabel("normalized graph idleness")
plt.legend()
# plt.show()
plt.savefig('normalized_final.png', dpi = 100)
	


		


