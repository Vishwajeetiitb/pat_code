import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
f = open("./path_name.txt", "r")
path = './data/' + f.read()
os.system('rm -rf '+path+'individual/runs/')
os.system('mkdir '+path+'individual/runs/')
xls = pd.ExcelFile(path+'runs.xlsx')
for i in range(10):
    df = np.array(pd.read_excel(xls,'run' +  str(i)))
    np.save(path+'individual/runs/'+'run'+ str(i),df,True)
