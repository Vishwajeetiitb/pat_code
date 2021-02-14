import os
import time
agents = [1, 2, 4, 5, 6, 7, 8, 10, 12]
no_fails = [0,5,12,20,25]
runs = 8
os.system('rm -rf ./data/')
os.system('mkdir ./data/')

for i in agents:
	os.system('rm -rf ./data/cr'+str(i)+'/')
	os.system('mkdir ./data/cr'+str(i)+'/')
	for fail_no in no_fails:
		os.system('rm -rf ./data/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
		os.system('mkdir  ./data/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
for no_agents in agents:
	for fail_no in no_fails:
		for run_id in range(runs):
			print(no_agents,'cars ',fail_no, ' devices are failed ','run id is ',str(run_id))
			time.sleep(5)
			os.system('python3 server_cr_n_dual_failure.py '+str(no_agents)+' '+str(fail_no)+' '+str(run_id))
			time.sleep(2)
