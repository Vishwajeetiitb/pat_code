import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data/'

cars = [4,6,10]
deads = [26]
num_runs = 5
for dead in deads:
	for car in cars:
		path = rootdir+'cr'+str(car)+'/'+str(dead)+'dead/'
		runs = []
		run_exploration_time =[]
		print(path)
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
		print(run_exploration_time)
		plt.figure()
		plt.plot(range(num_runs),run_exploration_time,  '-o')
		plt.title("exploration with varying runs")
		plt.xlabel("Run id")
		plt.ylabel("Exploration cycle")
		plt.show()
		plt.savefig(str(dead)+'_dead_'+str(car)+'_cars.png',dpi=100)
	


		


