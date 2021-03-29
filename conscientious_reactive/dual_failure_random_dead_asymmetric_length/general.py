import os
import time
agents = [1,3,6,9,12]
no_fails = [0,5,12,20,25]
runs = 3
# agents = [3]
# no_fails = [22]
# runs = 1
os.system('rm -rf ./data_2/')
os.system('mkdir ./data_2/')

for i in agents:
	os.system('rm -rf ./data_2/cr'+str(i)+'/')
	os.system('mkdir ./data_2/cr'+str(i)+'/')
	for fail_no in no_fails:
		os.system('rm -rf ./data_2/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
		os.system('mkdir  ./data_2/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
for no_agents in agents:
	for fail_no in no_fails:
		for run_id in range(runs):
			print(no_agents,'cars ',fail_no, ' devices are failed ','run id is ',str(run_id))
			time.sleep(5)
			os.system('python3 server_cr_n_dual_failure.py '+str(no_agents)+' '+str(fail_no)+' '+str(run_id))
			time.sleep(2)
