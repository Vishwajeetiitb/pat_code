import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import os
rootdir ='../data/'
for subdir, dirs, files in os.walk(rootdir):
    if os.path.exists(subdir+'/'+'run.xlsx'):
        path = subdir+'/'
        os.system('rm -rf '+path+'run_peaks')
        xls = pd.ExcelFile(path+'run.xlsx')
        df = np.array(pd.read_excel(xls))
        os.system('mkdir '+path +'run_peaks')
        print(path)
        workbook = xlsxwriter.Workbook(path+'run'+'_peaks/'+'run'+'_peaks.xlsx')
        worksheet = workbook.add_worksheet('peaks')
        colId = 0
        for col in np.transpose(df[:, 1:]):
            steptime = np.where(col == 0)[0]-1
            peaks = col[steptime]
            worksheet.write_column(0, 3*colId, steptime)
            worksheet.write_column(0, 3*colId+1, peaks)
            colId += 1
        workbook.close()
                    
    


                    
