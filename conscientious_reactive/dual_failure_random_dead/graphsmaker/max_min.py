import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data_3/'

cars = [1,2,3,4,5,6,7,8,9,10,12]
deads = [0,5,12,20,25]
num_runs = 8
plt.figure()
dev = []
avgs = []
for dead in deads:
	avg = []
	min1 = []
	max1 = []
	std = []
	for car in cars:
		path = rootdir+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
		runs = []
		min_val = []
		max_val = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			#print(path+'run'+str(i)+'/run.xlsx')
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][0:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
			min_val.append(np.min(runs[i])
			max_val.append(np.max(runs[i])
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		max_check = np.max(max_val)
		min_check = np.max(min_val)
		avg.append(np.mean(graph_idlness))
		std.append(np.std(graph_idlness))
		max1.append(max_check)
		min1.append(min_check)
	print(std)
	# plt.plot(cars, avg, label =str(dead)+"failures")

	avgs.append(avg)
	dev.append(std)
	plt.errorbar(cars, avg,yerr=[min1, max1], capthick=1.0, label=str(dead)+" failures")
	plt.draw()
	# plt.plot(cars, avg, label ="no of device failures ="+str(dead))
# plt.plot(cars, avg, 'b--')
# for i in range(len(dev)):
	# plt.plot(cars, avgs[i])#, label ="no of device failures ="+str(i*2))
	# plt.errorbar(cars, avgs[i], yerr = dev[i],  capthick=1.0)
plt.title("Idleness with varying runs and agents")
plt.xlabel("# agents")
plt.ylabel("Graph Idleness")
plt.legend()
# plt.show()
plt.savefig('max-min.png', dpi = 100)
# plt.savefig('dead'+str(dead)+'_new.png', dpi = 100)
