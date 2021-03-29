import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir1 ='/home/dikshant/github/pat_code/conscientious_reactive/dual_failure_random_dead/data_3/'
rootdir2 = '/home/dikshant/github/pat_code/conscientious_reactive/dual_failure_random_dead/updated_data/'

cars =  [1,3]#,6,9,12]
deads = [0, 12]#,25]
num_runs = 3
fig, axes = plt.subplot()
colors = ['r','g','b']
styles = ['-','-.']
check = 0
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir1+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
		runs = []
		instantaneous_node_idleness =[]
		for i in range(num_runs):
			# print(path+'run'+str(i)+'/run.xlsx')
			runs.append(np.array(pd.read_excel(pd.ExcelFile(path+'run'+str(i)+'/run.xlsx'))))
			runs[i] = runs[i][0:][:,1:]
			instantaneous_node_idleness.append(np.mean(runs[i],axis=1))
		graph_idlness = np.mean(instantaneous_node_idleness,axis=1)
		avg.append(np.mean(graph_idlness))
		# std.append(np.std(graph_idlness))
	print(avg)
	if check == 0:
		ax.plot(cars,avg, c=colors[check], ls=styles[0])
	elif check == 1:
		ax.plot(cars,avg,  c=colors[check], ls=styles[0])
	else:
		ax.plot(cars,avg,  c=colors[2], ls=styles[0])
	check += 1
	# plt.draw()
check = 0
for dead in deads:
	avg = []
	std = []
	for car in cars:
		path = rootdir2+'cr'+str(car)+'/'+str(dead)+'devices_failed/'
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
	if check == 0:
		ax.plot(cars,avg, c=colors[check], ls=styles[1])
	elif check == 1:
		ax.plot(cars,avg, c=colors[check], ls=styles[1])
	else:
		ax.plot(cars,avg, c=colors[2], ls=styles[1])
	check += 1
	# plt.draw()
# plt.plot(cars,avg, 'b--')
# for i in range(len(avgs)):
# 	plt.plot(cars, avgs[i], label ="no of device failures ="+str(i*2))
# plt.errorbar(cars, avg,yerr=std,  fmt='o', ecolor='g', capthick=1.0)
ax.title("Map A")
ax.legend(loc=1)
ax2.legend(loc=3)
plt.xlabel("# cars")
plt.ylabel("Graph Idleness")
# plt.legend()
# ax.show()
plt.savefig('intent3.png', dpi = 100)
# ax.savefig('dead'+str(dead)+'_new.png', dpi = 100)
	


		



