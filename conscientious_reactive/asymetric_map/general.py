import os
import time
agents = [1,2, 5,8,12]
no_fails = [0, 4, 10, 14, 21, 28]
runs = 3

agents = [14]
no_fails = [10]
runs = 1
os.system('rm -rf ./data_intent/')
os.system('mkdir ./data_intent/')

for i in agents:
	os.system('rm -rf ./data_intent/cr'+str(i)+'/')
	os.system('mkdir ./data_intent/cr'+str(i)+'/')
	for fail_no in no_fails:
		os.system('rm -rf ./data_intent/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
		os.system('mkdir  ./data_intent/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
for no_agents in agents:
	for fail_no in no_fails:
		for run_id in range(runs):
			print(no_agents,'cars ',fail_no, ' devices are failed ','run id is ',str(run_id))
			time.sleep(5)
			os.system('python3 pat_cr_n_intent_iot_server.py '+str(no_agents)+' '+str(fail_no)+' '+str(run_id))
			time.sleep(2)
