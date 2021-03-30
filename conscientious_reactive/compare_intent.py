import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
import itertools

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])
rootdir1 ='./asymetric_map/data_2/'
rootdir2 = './asymetric_map/final_data/'
	
cars =  [1,2,6,10]#,6,9,12]
deads = [0,14,28]#,25]
num_runs = 2
plt.figure()
ax = plt.subplot(111)
# fig, axes = plt.subplot()
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
		ax.plot(cars,avg, c=colors[check], ls=styles[0],label= str(dead)+" w/o intent")
	elif check == 1:
		ax.plot(cars,avg,  c=colors[check], ls=styles[0],label= str(dead)+" w/o intent")
	else:
		ax.plot(cars,avg,  c=colors[2], ls=styles[0],label= str(dead)+" w/o intent")
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
		ax.plot(cars,avg, c=colors[check], ls=styles[1],label= str(dead)+" w intent")
	elif check == 1:
		ax.plot(cars,avg, c=colors[check], ls=styles[1],label= str(dead)+" w intent")
	else:
		ax.plot(cars,avg, c=colors[2], ls=styles[1],label= str(dead)+" w intent")
	check += 1
	# plt.draw()
# plt.plot(cars,avg, 'b--')
# for i in range(len(avgs)):
# 	plt.plot(cars, avgs[i], label ="no of device failures ="+str(i*2))
# plt.errorbar(cars, avg,yerr=std,  fmt='o', ecolor='g', capthick=1.0)
plt.title("Map C")
# ax.legend(loc=1)
# ax2.legend(loc=3)
plt.xlabel("# cars")
plt.ylabel("Graph Idleness")
handles, labels = ax.get_legend_handles_labels()
plt.legend(ncol=2)
# plt.legend()
# plt.show()
plt.savefig('./intent_asymetric_map.png', dpi = 100)

# plt.legend(flip(handles, 2), flip(labels, 2), loc=9, ncol=2)
# ax.savefig('dead'+str(dead)+'_new.png', dpi = 100)


		



