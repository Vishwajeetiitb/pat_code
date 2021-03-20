import os
import time
agents = [1,5]#[1,2, 5,8,12]
no_fails = [4]#[0, 4, 10, 14, 21, 28]
runs = 2
# agents = [14]
# no_fails = [10]
# runs = 1
os.system('rm -rf ./check3/')
os.system('mkdir ./check3/')

for i in agents:
	os.system('rm -rf ./check3/cr'+str(i)+'/')
	os.system('mkdir ./check3/cr'+str(i)+'/')
	for fail_no in no_fails:
		os.system('rm -rf ./check3/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
		os.system('mkdir  ./check3/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
for no_agents in agents:
	for fail_no in no_fails:
		for run_id in range(runs):
			print(no_agents,'cars ',fail_no, ' devices are failed ','run id is ',str(run_id))
			time.sleep(5)
			os.system('python3 pat_cr_n_iot_server.py '+str(no_agents)+' '+str(fail_no)+' '+str(run_id))
			time.sleep(2)
