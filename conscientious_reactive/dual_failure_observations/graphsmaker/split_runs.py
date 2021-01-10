import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
rootdir ='../data/'
for subdir, dirs, files in os.walk(rootdir):
    if os.path.exists(subdir+'/'+'run.xlsx'):
    	path =subdir +'/'
    	xls = pd.ExcelFile(path+'run.xlsx')
    	os.system('rm -rf '+path+'numpy/')
    	os.system('mkdir '+path+'numpy/')
    	df = np.array(pd.read_excel(xls))
    	np.save(path+'numpy/run',df,True)
    	print(path+'numpy/')
