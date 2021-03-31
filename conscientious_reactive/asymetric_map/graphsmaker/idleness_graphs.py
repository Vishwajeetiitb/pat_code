import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data_3_updated/'

cars =  [1,2, 5,8,12]
deads = [0, 4, 10, 14, 21, 28]
num_runs = 3
plt.figure()

for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
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
	if dead == 0:
		plt.plot(avg, cars, label =str(dead)+" failure")
	else:
		plt.plot(avg, cars, label =str(dead)+" failures")
	plt.draw()

# plt.plot(cars,avg, 'b--')
# for i in range(len(avgs)):
# 	plt.plot(cars,avgs[i], label ="no of device failures ="+str(i*2))
# plt.errorbar(cars,avg,yerr=std,  fmt='o', ecolor='g', capthick=1.0)
# plt.title("Map C")
plt.ylabel("# agents")
plt.xlabel("Graph Idleness")
plt.legend()
# plt.show()
plt.savefig('result3.png', dpi = 100)
# plt.savefig('dead'+str(dead)+'_new.png', dpi = 100)
	


		


