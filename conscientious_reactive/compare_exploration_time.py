import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir1 ='/home/arms03/Documents/patrolling_vishwajeet_dikshant/pat_code/conscientious_reactive/dual_failure_random_dead/data_3/'
rootdir2 = '/home/arms03/Documents/patrolling_vishwajeet_dikshant/pat_code/conscientious_reactive/dual_failure_random_dead_asymmetric_length/data/'

cars = [1, 2, 4, 5, 6, 7, 8, 10, 12]
deads = [0,12,25]
num_runs = 8
plt.figure()
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir1+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
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
	print(avg)
	plt.plot(cars, avg, '-', label ="no of device failures ="+str(dead)+" for equal length")
	plt.draw()
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir2+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
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
	print(avg)
	plt.plot(cars, avg, '--',label ="no of device failures ="+str(dead)+" for varying length")
	plt.draw()
# plt.plot(cars, avg, 'b--')
# plt.errorbar(cars, avg,yerr=std, fmt = 'o', ecolor='g', capthick=1.0)
plt.title("comparison in exploration time for symmetric and asymmetric maps")
plt.xlabel("number of agents")
plt.ylabel("exploration time")
plt.legend()
#plt.show()
plt.savefig('exploredead'+'new.png',dpi=100)
	


		



