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
		run_exploration_time =[]
		
		for i in range(num_runs):
			node_list = [i for i in range(25)]
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][0:][:,:]
			for step in runs[i]:
				visited_node = np.where(step[1:] == 0)[0]
				if len(visited_node) is not 0:
					visited_node = visited_node[0]
					if visited_node in node_list:
						node_list.remove(visited_node)
				if len(node_list)==0:
					run_exploration_time.append(step[0])
					break

		avg.append(np.mean(run_exploration_time))
		std.append(np.std(run_exploration_time))
	plt.figure()
	plt.plot(cars, avg, 'b--')
	plt.errorbar(cars, avg,yerr=std, fmt = 'o', ecolor='g', capthick=1.0)
	plt.title("exploration with varying runs and agents")
	plt.xlabel("number of agents")
	plt.ylabel("graph idleness")
	#plt.show()
	plt.savefig('exploredead'+str(dead)+'_new.png',dpi=100)
	


		


