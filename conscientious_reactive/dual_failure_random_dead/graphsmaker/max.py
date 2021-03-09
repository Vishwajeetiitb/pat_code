import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data_3/'

cars =  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
deads = [0,5,12,20,25]
num_runs = 8
plt.figure()
# ignore the terminologies
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
			runs[i] = runs[i][0:][:,1:]
			instantaneous_node_idleness.append(np.max(runs[i]))
		graph_idlness = np.max(instantaneous_node_idleness)
		avg.append(np.max(graph_idlness))
	# 	# std.append(np.std(graph_idlness))
	print(avg)
	plt.plot(cars, avg, label =str(dead)+' failures')
	plt.draw()
	

# plt.plot(cars, avg, 'b--')
# for i in range(len(avgs)):
# 	plt.plot(cars, avgs[i], label ="no of device failures ="+str(i*2))
# plt.errorbar(cars, avg,yerr=std,  fmt='o', ecolor='g', capthick=1.0)
plt.title("Max Idleness with varying runs and agents")
plt.xlabel("# agents")
plt.ylabel("Graph Idleness")
plt.legend()
# plt.show()
plt.savefig('max.png', dpi = 100)
# plt.savefig('dead'+str(dead)+'_new.png', dpi = 100)
	


		


