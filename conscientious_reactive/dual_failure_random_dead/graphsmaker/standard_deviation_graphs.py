import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../updated_data/'

cars =  [1,3,6,9,12]
deads = [0,12,25]
num_runs = 3
plt.figure()
dev = []
avgs = []
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
		runs = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			#print(path+'run'+str(i)+'/run.xlsx')
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][0:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		avg.append(np.mean(graph_idlness))
		std.append(np.std(graph_idlness))
	print(std)
	# plt.plot(avg,cars, label =str(dead)+"failures")

	avgs.append(avg)
	dev.append(std)
	if dead == 0:
		plt.errorbar(avg,cars,xerr=std, capthick=1.0, label=str(dead)+" failure")
	else:
		plt.errorbar(avg,cars,xerr=std, capthick=1.0, label=str(dead)+" failures")
	plt.draw()
	# plt.plot(avg,cars, label ="no of device failures ="+str(dead))
# plt.plot(avg,cars, 'b--')
# for i in range(len(dev)):
	# plt.plot(avg,carss[i])#, label ="no of device failures ="+str(i*2))
	# plt.errorbar(avg,carss[i], yerr = dev[i],  capthick=1.0)
plt.title("Graph Idleness with standard deviation for Map A")
plt.xlabel("# agents")
plt.ylabel("Graph Idleness")
plt.legend()
# plt.show()
plt.savefig('std_deviations.png', dpi = 100)
# plt.savefig('dead'+str(dead)+'_new.png', dpi = 100)