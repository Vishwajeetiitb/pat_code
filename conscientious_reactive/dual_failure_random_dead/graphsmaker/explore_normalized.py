import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data/'

cars = [1,2,3,4,5,6,7,8,9,10]
deads = [0,2,4,6,8]
num_runs = 10
plt.figure()
for dead in deads:
	avg_norm = []
	std_norm = []
	for car in cars:
		path = rootdir+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
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
		run_exploration_time = np.array(run_exploration_time)*car/25
		avg_norm.append(np.mean(run_exploration_time))
		std_norm.append(np.std(run_exploration_time))
	print(avg_norm)
	plt.plot(cars, avg_norm, label ="no of device failures ="+str(dead))
	plt.draw()

	# plt.figure()
	# plt.plot(cars, avg_norm, 'b--')
	# plt.errorbar(cars, avg_norm,yerr=std_norm, fmt = 'o', ecolor='g', capthick=1.0)
plt.title("normalized exploration time with varying runs and agents")
plt.xlabel("number of agents")
plt.ylabel("normalized exploration time")
plt.legend()
#plt.show()
plt.savefig('normalized_explore.png',dpi=100)
	


		


