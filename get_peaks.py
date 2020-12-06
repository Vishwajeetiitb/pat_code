import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
f = open("./path_name.txt", "r")
path = './data/' + f.read()
xls = pd.ExcelFile(path+'runs.xlsx')
for i in range(10):
    df = np.array(pd.read_excel(xls, 'run' + str(i)))
    os.system('rm -rf '+path+'run'+str(i)+'_peaks')
    os.system('mkdir '+path+'run'+str(i)+'_peaks')
    workbook = xlsxwriter.Workbook(path+'run'+str(i)+'_peaks/'+'run'+str(i)+'_peaks.xlsx')
    worksheet = workbook.add_worksheet('peaks')
    colId = 0
    for col in np.transpose(df[:, 1:]):
        steptime = np.where(col == 0)[0]-1
        peaks = col[steptime]
        worksheet.write_column(0, 3*colId, steptime)
        worksheet.write_column(0, 3*colId+1, peaks)
        colId += 1
    workbook.close()
