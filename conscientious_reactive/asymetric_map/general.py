import os
import time
<<<<<<< HEAD
agents = [1,2, 5,8,12]
no_fails = [0, 4, 10, 14, 21, 28]
runs = 2

# agents = [14]
# no_fails = [10]
# runs = 1
os.system('rm -rf ./final_data/')
os.system('mkdir ./final_data/')

for i in agents:
	os.system('rm -rf ./final_data/cr'+str(i)+'/')
	os.system('mkdir ./final_data/cr'+str(i)+'/')
	for fail_no in no_fails:
		os.system('rm -rf ./final_data/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
		os.system('mkdir  ./final_data/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
=======
agents = [1,2, 6, 10, 14]
no_fails = [0, 4, 10, 14, 21, 28]
runs = 3
# agents = [14]
# no_fails = [10]
# runs = 1
os.system('rm -rf ./data_4/')
os.system('mkdir ./data_4/')

for i in agents:
	os.system('rm -rf ./data_4/cr'+str(i)+'/')
	os.system('mkdir ./data_4/cr'+str(i)+'/')
	for fail_no in no_fails:
		os.system('rm -rf ./data_4/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
		os.system('mkdir  ./data_4/cr'+str(i)+'/'+str(fail_no)+'devices_failed')
>>>>>>> ee0012c882939738aaef49973f02a4aaecbf5d10
for no_agents in agents:
	for fail_no in no_fails:
		for run_id in range(runs):
			print(no_agents,'cars ',fail_no, ' devices are failed ','run id is ',str(run_id))
			time.sleep(5)
			os.system('python3 pat_cr_n_iot_server.py '+str(no_agents)+' '+str(fail_no)+' '+str(run_id))
			time.sleep(2)
