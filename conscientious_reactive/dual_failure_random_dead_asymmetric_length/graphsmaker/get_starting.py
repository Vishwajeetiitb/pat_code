import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


rootdir ='../data/'
for subdir, dirs, files in os.walk(rootdir):
    if os.path.exists(subdir+'/'+'run.xlsx'):
        path =subdir+'/'
        os.system('rm -rf '+path+'startings/')
        os.system('mkdir '+path+'startings/')
        xls = pd.ExcelFile(path+'run.xlsx')
        df = np.array(pd.read_excel(xls))
        nodes = np.where(df==0)
        plt.plot(nodes[0][0:1000],nodes[1][0:1000])
        np.save(path+'startings/'+'run_starting',nodes)
        print(path)
