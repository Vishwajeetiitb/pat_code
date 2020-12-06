import os
import time 
scripts = ['get_peaks.py','create_folder.py','split_runs.py','pattern_graphs.py','get_starting.py','starting_graphs.py','grid_graphs.py']
tic  = time.time()
for element in scripts:
    print(element+' started')
    os.system('python3 '+element)
    print(element+' ended')
 