import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
rootdir ='../data/'
for subdir, dirs, files in os.walk(rootdir):
    if os.path.exists(subdir+'/'+'run.xlsx'):
        path =subdir+'/'
        os.system('rm -rf '+path+'patterns_img/')
        os.system('mkdir '+path+'patterns_img/')
        figName = path+'patterns_img/pattern.png'
        run = np.load(path+'numpy/run.npy')
        df = np.where(run == 0)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        x = df[0][100:500]
        y = df[1][100:500]-1
        print(len(df[1]))
        for i in range(y.shape[0]):
            plt.annotate(y[i], (x[i], y[i]),
                         textcoords="offset points", xytext=(0, 0), ha='center')
        ax.plot(x, y)
        ax.plot(x, y, 'o', color='r')
        fig.set_size_inches(19.20, 10.80)
        plt.xlabel('time step')
        plt.ylabel('node id')
        plt.grid()
        # plt.tight_layout()
        plt.title('run pattern')
        # ax.set
        plt.savefig(figName, dpi=100,bbox_inches = 'tight')
        # fig.clear()
