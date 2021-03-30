import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir1 ='/home/dikshant/github/pat_code/conscientious_reactive/dual_failure_random_dead/updated_data/'
rootdir2 = '/home/dikshant/github/pat_code/conscientious_reactive/dual_failure_random_dead_asymmetric_length/data_2/'

cars =  [1,3,6,9,12]
deads = [0,12,25]
num_runs = 3
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
			runs[i] = runs[i][0:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		avg.append(np.mean(graph_idlness))
		# std.append(np.std(graph_idlness))
	print(avg)
	if check == 0:
		plt.plot(avg,cars, 'r-',label =str(dead)+" failure(A)")
	elif check == 1:
		plt.plot(avg,cars, 'g-',label =str(dead)+" failures(A)")
	else:
		plt.plot(avg,cars, 'b-',label =str(dead)+" failures(A)")
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
		plt.plot(avg,cars, 'r--',label =str(dead)+" failure(B)")
	elif check == 1:
		plt.plot(avg,cars, 'g--',label =str(dead)+" failures(B)")
	else:
		plt.plot(avg,cars, 'b--',label =str(dead)+" failures(B)")
	check += 1
	plt.draw()
# plt.plot(avg,cars, 'b--')
# for i in range(len(avgs)):
# 	plt.plot(avg,carss[i], label ="no of device failures ="+str(i*2))
# plt.errorbar(avg,cars,yerr=std,  fmt='o', ecolor='g', capthick=1.0)
# plt.title("Idleness comparison b/w Map A and B")
plt.ylabel("# agents")
plt.xlabel("Graph Idleness")
plt.legend()
# plt.show()
plt.savefig('idleness2.png', dpi = 100)
# plt.savefig('dead'+str(dead)+'_new.png', dpi = 100)
	


		



