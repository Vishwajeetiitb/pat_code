import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
rootdir ='../data/'
for subdir, dirs, files in os.walk(rootdir):
    if os.path.exists(subdir+'/'+'run.xlsx'):
        path = subdir+'/'
        figName = path+'startings/starting.png'
        run = np.load(path+'startings/run_starting.npy')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        x = run[0][1:400]
        y = run[1][1:400]-1
        for i in range(y.shape[0]):
            plt.annotate(y[i], (x[i], y[i]),
                         textcoords="offset points", xytext=(0, 0), ha='center')
        ax.plot(x, y)
        ax.plot(x, y, 'o', color='r')
        fig.set_size_inches(19.20, 10.80)
        plt.xlabel('time step')
        plt.ylabel('node id')
        minor_ticks = np.arange(0, 24, 50)
        ax.set_xticks(minor_ticks, minor=True)
        plt.grid()
        plt.tight_layout()
        plt.title('run starting pattern')
        # ax.set
        plt.savefig(figName, dpi=100, bbox_inches='tight')
        # fig.clear()
        # print(path)

