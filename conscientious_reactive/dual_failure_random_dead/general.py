import os
import time
agents = [1,2,3,4,5,6,7,8,9,10]
no_fails = [0]
runs = 10
os.system('rm -rf ./data1/')
os.system('mkdir ./data1/')

for i in agents:
	os.system('rm -rf ./data1/cr'+str(i)+'/')
	os.system('mkdir ./data1/cr'+str(i)+'/')
	for fail_no in no_fails:
		os.system('rm -rf ./data1/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
		os.system('mkdir  ./data1/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
for no_agents in agents:
	for fail_no in no_fails:
		for run_id in range(runs):
			print(no_agents,'cars ',fail_no, ' devices are failed ','run id is ',str(run_id))
			os.system('python3 server_cr_n_dual_failure.py '+str(no_agents)+' '+str(fail_no)+' '+str(run_id))
			time.sleep(2)
