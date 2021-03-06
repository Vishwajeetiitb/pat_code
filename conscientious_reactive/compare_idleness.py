import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir1 ='/home/arms03/Documents/patrolling_vishwajeet_dikshant/pat_code/conscientious_reactive/dual_failure_random_dead/data_3/'
rootdir2 = '/home/arms03/Documents/patrolling_vishwajeet_dikshant/pat_code/conscientious_reactive/dual_failure_random_dead_asymmetric_length/data/'

cars =  [1, 2, 4, 5, 6, 7, 8, 10, 12]
deads = [0,12,25]
num_runs = 8
plt.figure()
check = 0
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir1+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
		runs = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			# print(path+'run'+str(i)+'/run.xlsx')
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][500:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		avg.append(np.mean(graph_idlness))
		# std.append(np.std(graph_idlness))
	print(avg)
	if check == 0:
		plt.plot(cars, avg, 'r-',label ="no. of device failures ="+str(dead)+" for equal length")
	elif check == 1:
		plt.plot(cars, avg, 'g-',label ="no. of device failures ="+str(dead)+" for equal length")
	else:
		plt.plot(cars, avg, 'b-',label ="no. of device failures ="+str(dead)+" for equal length")
	check += 1
	plt.draw()
check = 0
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir2+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
		runs = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			# print(path+'run'+str(i)+'/run.xlsx')
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][500:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		avg.append(np.mean(graph_idlness))
		# std.append(np.std(graph_idlness))
	print(avg)
	if check == 0:
		plt.plot(cars, avg, 'r--',label ="no. of device failures ="+str(dead)+" for equal length")
	elif check == 1:
		plt.plot(cars, avg, 'g--',label ="no. of device failures ="+str(dead)+" for equal length")
	else:
		plt.plot(cars, avg, 'b--',label ="no. of device failures ="+str(dead)+" for equal length")
	check += 1
	plt.draw()
# plt.plot(cars, avg, 'b--')
# for i in range(len(avgs)):
# 	plt.plot(cars, avgs[i], label ="no of device failures ="+str(i*2))
# plt.errorbar(cars, avg,yerr=std,  fmt='o', ecolor='g', capthick=1.0)
plt.title("comparison in idleness for symmetric and asymmetric maps")
plt.xlabel("number of agents")
plt.ylabel("graph idleness")
plt.legend()
# plt.show()
plt.savefig('final.png', dpi = 100)
# plt.savefig('dead'+str(dead)+'_new.png', dpi = 100)
	


		



