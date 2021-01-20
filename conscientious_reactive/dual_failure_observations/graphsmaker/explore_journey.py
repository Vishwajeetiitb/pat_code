import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data/'
os.system("rm -rf explore_journey2")
os.system("mkdir explore_journey2")
cars = [2,4,6,10]
deads = [0,2,12]
num_runs = 5
for dead in deads:
	for car in cars:
		path = rootdir+'cr'+str(car)+'/'+str(dead)+'dead/'
		runs = []

		print(path)
		for i in range(num_runs):
			run_exploration_time =[]
			node_list = [i for i in range(25)]
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][0:][:,:]
			k = 0
			for step in runs[i]:
				visited_node = np.where(step[1:] == 0)[0]
				if len(visited_node) is not 0:
					visited_node = visited_node[0]
					if visited_node in node_list:
						node_list.remove(visited_node)
				if len(node_list)==0:
					if k ==0:
						if step[0]>500:
							run_exploration_time.append(step[0])
							k = k+1
					else:
						run_exploration_time.append(step[0]-last_step[0])
						k = k+1	
					last_step = step
					node_list = [i for i in range(25)]
			print(run_exploration_time)
			# fig=plt.figure()
			plt.plot(run_exploration_time,  '-o')
			plt.title("exploration times of single run")
			plt.xlabel("progress")
			plt.ylabel("Exploration cycle")
			# plt.show()
			plt.savefig('explore_journey2/'+str(dead)+'_dead_'+str(car)+'_cars_run'+str(i)+'.png',dpi=100)
			plt.close()
	


		


