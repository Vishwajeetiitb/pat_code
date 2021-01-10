import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir1 ='./data/'
rootdir2 ='./no_dead_data/'

cars = [1,2,4,6,10]
deads = [0,2,12]
no_deads = [26]
num_runs = 5
avg = []
avg2 = []
for dead in deads:
	avg1 = []
	for car in cars:
		path1 = rootdir1+'cr'+str(car)+'/'+str(dead)+'dead/'
		runs1 = []
		run_exploration_time1 = []
			
		for i in range(num_runs):
			node_list1 = [i for i in range(25)]
			runs1.append(np.array(pd.read_excel(pd.ExcelFile(path1+'run'+str(i)+'/run.xlsx'))))
			runs1[i] = runs1[i][0:][:,:]
			for step in runs1[i]:
				visited_node1 = np.where(step[1:] == 0)[0]
				if len(visited_node1) is not 0:
					visited_node1 = visited_node1[0]
					if visited_node1 in node_list1:
						node_list1.remove(visited_node1)
				if len(node_list1)==0:
					run_exploration_time1.append(step[0])
					break		
		avg1.append(np.mean(run_exploration_time1))
		avg.append(avg1)
for dead in no_deads:
	for car in cars:
		path2 = rootdir2+'cr'+str(car)+'/'+str(dead)+'dead/'
		runs2 = []
		run_exploration_time2 = []
			
		for i in range(num_runs):
			node_list2 = [i for i in range(25)]
			runs2.append(np.array(pd.read_excel(pd.ExcelFile(path2+'run'+str(i)+'/run.xlsx'))))
			runs2[i] = runs2[i][0:][:,:]
			for step in runs2[i]:
				visited_node2 = np.where(step[1:] == 0)[0]
				if len(visited_node2) is not 0:
					visited_node2 = visited_node2[0]
					if visited_node2 in node_list2:
						node_list2.remove(visited_node2)
				if len(node_list2)==0:
					run_exploration_time2.append(step[0])
					break
		avg2.append(np.mean(run_exploration_time2))

for dead in deads: 
	plt.figure()
	plt.plot(cars, avg[dead], label = "practical")
	plt.plot(cars, avg2, label = "ideal")
	plt.legend()
	# plt.errorbar(cars, avg,yerr=std, fmt = 'o', ecolor='g', capthick=1.0)
	plt.title("ideal vs practical")
	plt.xlabel("number of agents")
	plt.ylabel("exploration time")
	#plt.show()
	plt.savefig('exploredead'+str(dead)+'.png',dpi=100)
	


		


