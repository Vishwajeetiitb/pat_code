import matplotlib.pyplot as plt
from matplotlib import axes

import pandas as pd
import numpy as np
import os
colors = ['b',"#2E7F18","#45731E","#675E24","#8D472B","#B13433","#C82538","#1C6FF8","#27BBE0",'y','c','b','#a87332','#a832a8','#a832a8','#32a889','#92a832','#92a832']
# NodeId = int(input('enter node id \n'))
size = 5
rootdir ='../data/'
for subdir, dirs, files in os.walk(rootdir):
    if os.path.exists(subdir+'/'+'run.xlsx'):
        path = subdir+'/'
        os.system('rm -rf '+path+'grids_img')
        os.system('mkdir '+path+'grids_img')
        fig, axs = plt.subplots(size, size)
        plt.setp(axs,ylim=(50,500))
        fig.set_size_inches(19.20, 10.80)
        RunPath = path+'run_peaks/'
        xls = pd.ExcelFile(RunPath+'run_peaks.xlsx')
        df = np.array(pd.read_excel(xls))
        errr = []
        for NodeId in range(size*size):
            idlness = df[:, 3*NodeId+1]
            steptime = df[:, 3*NodeId]
            a = int(NodeId/size)
            b = NodeId - size*a
            idlness_size = idlness.shape[0]
            # print(idlness_size)
            x = steptime[25:idlness_size-40]
            y = idlness[25:idlness_size-40]
            sample  = x[0:10]
            errr.append([NodeId,max(y[10:20])-min(y[10:20])])

        dd = np.array(errr)
        # print(dd[0,0],'yo')
        dd = dd[dd[:,1].argsort()]
        # print(dd)
        d = 0
        g = 0
        temp = dd[0,1]
        for NodeId in dd[:,0]:
            # print(dd[d,0])
            if(abs(temp-dd[d,1])<10):
                # print(,temp-dd[d,1])
                lol = True
            else:
                g = g+1
                temp=dd[d,1]
            NodeId = int(NodeId)  
            idlness = df[:, 3*NodeId+1]
            steptime = df[:, 3*NodeId]
            a = int(NodeId/size)
            b = NodeId - size*a
            idlness_size = idlness.shape[0]
            # print(idlness_size)
            x = steptime[25:idlness_size-40]
            y = idlness[25:idlness_size-40]
            sample  = x[0:10]
            errr.append([NodeId,max(y[10:20])-min(y[10:20])])
            # freq  = []
            # for i in range(sample.shape[0]-2):
            #     freq.append(sample[i+2]-sample[i])

            # print(NodeId,freq,y[0:10])
            axs[size-a-1, b].plot(x,y,color=colors[0])
            axs[size-a-1,b].set_ylabel('node'+str(NodeId)+' idlness')
            axs[size-a-1,b].set_xlabel('time step')
            d = d+1
            # NodeId += 1
        # plt.xlabel('time step')
        # plt.ylabel('idlness')
        # plt.ylim([2,5])
        plt.title('grid')
        plt.savefig(path+'grids_img/rungrid.png',bbox_inches = 'tight', dpi=100)
        
