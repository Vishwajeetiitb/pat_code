import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
f = open("./path_name.txt", "r")
path = './data/' + f.read()
os.system('rm -rf '+path+'individual/startings/')
os.system('mkdir '+path+'individual/startings/')
xls = pd.ExcelFile(path+'runs.xlsx')
for i in range(10):
    df = np.array(pd.read_excel(xls,'run' +  str(i)))
    nodes = np.where(df==0)
    print(nodes)
    plt.plot(nodes[0][0:1000],nodes[1][0:1000])
    np.save(path+'individual/startings/'+'run'+str(i)+'_starting',nodes)
plt.show()