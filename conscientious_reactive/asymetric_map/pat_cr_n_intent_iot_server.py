# RL Environment for Patrolling
__author__='dikshant & vishwajeet'
  
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import os
import sys
import optparse
import time
import random
from collections import deque, namedtuple
import socket
import xlsxwriter
from numpy.random import default_rng
rng = default_rng()
cars = int(sys.argv[1])
no_of_failed_devices = int(sys.argv[2])
# dead_node = rng.choice([i for i in range(28)],no_of_failed_devices,replace=False)
dead_node = [10]
# print(dead_node)
# dead_node = []    
run_id = int(sys.argv[3])
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary

sys.path.append(os.path.join('c:', os.sep, 'whatever', 'path', 'to', 'sumo', 'tools'))
sumoBinary = checkBinary("sumo-gui")
map_path = "../../maps/asymmetric/"
map_name = "complex_final"

# sumoCmd = [sumoBinary, "-c", "../maps/grid_5_5.sumocfg",
        #    "--tripinfo-output", "../maps/tripinfo.xml"]
sumoCmd = [sumoBinary, "-c", str(map_path)+str(map_name)+".sumocfg", "--tripinfo-output", str(map_path)+"tripinfo.xml"] 
import traci

class rl_env(object):

    def __init__(self):
        global cars
        # self.nrow, self.ncol= 5, 5
        self.stateSpace=np.array([i for i in range(28)])
        self.actionSpace = [0, 1, 2, 3]
        #Action space= {'0': 'North', '1': 'South', '2': 'East', '3': 'West'}
        self.state=[0 for i in range(cars)]
        self.nA = 4
        self.nS = 28
        self.reward=[0 for i in range(cars)] #change

    def sample(self):
        action_node = random.choice(self.adj_nodes)
        return action_node

    def check_step(self, curr_state, next_state, idle, action_node, i):
        if curr_state==next_state[i]:
            action_node=self.sample()
            self.state, self.reward, action_node=self.step(action_node, idle, i)
        return self.state, self.reward, action_node

    def step(self, action_node, idle, i):
        curr_state=self.state[i]
        
        self.state[i]=action_node
        # print('cur and next: ', curr_state, self.state)
        self.reward[i]=idle[self.state[i]]
        self.state, self.reward, action_node=self.check_step(curr_state, self.state, idle, action_node, i)
        return self.state[i], self.reward, action_node


    def reward_out(self, idle, prev_node, i):
        self.reward[i] = idle[prev_node]
        return self.reward[i]

    def reset(self, routes): #change
        global cars,startings
        self.state= startings
        self.reward=[0 for i in range(cars)]
        traci.start(sumoCmd)
        for car_no in range(cars):
            traci.route.add('rou_'+str(car_no), [routes[car_no]])
            traci.vehicle.add(vehID = 'veh'+str(car_no),routeID = 'rou_'+str(car_no), typeID = "car1")
        return self.state
#end of class

def eval_met(idle, v_idle,sumo_step, n):

    avg_v_idl=np.zeros((28,1))
    max_v_idl=np.zeros((28,1))
    var_v_idl=np.zeros((28,1))
    #avg idleness
    for i in range(n):
        if v_idle[i]:
            avg_v_idl[i]=np.sum(np.square(v_idle[i]))/(2*sumo_step)
    glo_v_idl=np.mean(avg_v_idl)
    glo_idl= np.mean(idle)
    #max idleness
    for i in range(n):
        if v_idle[i]:
            max_v_idl[i]=np.max(v_idle[i])
    glo_max_idl=np.max(idle)
    glo_max_v_idl=np.max(max_v_idl)
    #var,stdev and glob stdev
    for i in range(n):
        if v_idle[i]:
            var_v_idl[i]=(np.sum(np.power(v_idle[i],3))/(3*sumo_step))-avg_v_idl[i]
    sd_v_idl=np.sqrt(var_v_idl)
    glo_sd_v_idl=np.mean(sd_v_idl)
    return avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl
#end of fn

def CR_patrol(idle, c, env,existing_action):

    global adj_nodes,all_routes
    all_routes = extract_routes()
    adj_nodes = [s.split("to")[1] for s in all_routes if s.startswith(str(c)+"to")]
    adj_idle = []
    # print("yo",adj_nodes,c)
    temp_adj = np.setdiff1d(adj_nodes,existing_action)
    if len(temp_adj)!=0:
        for node in temp_adj:
            adj_idle.append(idle[int(node)])
        action_node = int(temp_adj[adj_idle.index(max(adj_idle))])
    else:
        for node in adj_nodes:
            adj_idle.append(idle[int(node)])
        action_node = int(adj_nodes[adj_idle.index(max(adj_idle))])


    return action_node

#end of fn

def run(env):
    global cars,all_routes,dead_node, workbook, run_id, adj_nodes
    worksheet = workbook.add_worksheet('run'+str(run_id))
    rou_curr= all_routes
    env.reset(rou_curr)
    sumo_step=1.0
    cr = [0 for i in range(cars)]
    rl_step=1.0
    idle=[np.zeros((28,1)) for _ in range(cars)]
    global_idl=np.zeros((28,1))
    global_v_idl=[[] for _ in range(28)]
    v_idle=[[[] for _ in range(28)] for _ in range(cars)]
    edge = [0 for i in range(cars)]
    prev_node=env.state
    curr_node=[0 for i in range(cars)]
    temp_n=[0 for i in range(cars)]
    temp_p=[0 for i in range(cars)]
    ga=[]
    ma_ga=deque(maxlen=3000)
    gav=[]
    ss=[]
    num_steps = 30000
    cloud_array = np.zeros([28,cars,28,1])
    idle_2d = np.zeros([num_steps, 28])
    action_list = [28+1 for i in range(cars)]
    # check = np.random.randint(1000, 3000)
    while traci.simulation.getMinExpectedNumber()>0:
        # if sumo_step == check:
        # 8)],no_of_failed_devices)
        idle_2d[int(sumo_step)-1] = np.transpose(global_idl)
        traci.simulationStep()
        for i in range(cars):
            idle[i]+=1
            cloud_array[:,i,:]+=1
        global_idl+=1
        for car_no in range(cars): 
            edge[car_no] = traci.vehicle.getRoadID('veh'+str(car_no))
        #print('veh edge data_3: ',edge)
        for i, ed in enumerate(edge):
            if ed and (ed[0]!=':'):
                curr_node[i]= ed.split('to')
                curr_node[i]=int(curr_node[i][1])
            elif ed[0]==':':
                curr_node[i]=ed[1:].split('_')
                curr_node[i]=int(curr_node[i][0])
        env.state=curr_node.copy()
        # print('p_node:',prev_node, 'c_node:',curr_node, 'temp_p: ', temp_p, 'temp_n: ', temp_n)
        # Action decision on new edge
        for i in range(cars):
            if prev_node[i]!=curr_node[i]:        
                temp_p[i]=prev_node[i]
                # print(':::::::::::::to next node for', i, '::::::::::::::::')

                # print('Veh angle: ', traci.vehicle.getAngle('veh'+str(i)))
                rou_step=[]
                glo_reward=env.reward_out(global_idl, prev_node[i], i)[0]
                # print(cloud_array[curr_node[i],i,:],idle[i])
                prev_reward=env.reward_out(cloud_array[prev_node[i],i,:], prev_node[i], i)[0]
                # print('reward on prev step: ', prev_reward)
                v_idle[i][int(prev_node[i])].append(prev_reward.copy())
                global_v_idl[int(prev_node[i])].append(glo_reward.copy())
                avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(global_idl, global_v_idl,sumo_step, 28)
                # print('global avg node visit idleness: ', glo_v_idl, '\nglobal max node visit idleness: ', glo_max_v_idl)
                # print('global avg instant idleness: ', glo_idl, '\nglobal max instant idleness: ', glo_max_idl)
                #print(np.array(v_idle).reshape(5,5))
                
                cr[i]+=prev_reward
                #acr=cr/sumo_step
                #print('acr: ', acr)
                    

                # print()
                cloud_array[prev_node[i],i,prev_node[i]]=0
                # print(dead_node)
                if (prev_node[i] not in dead_node):
                    cloud_array[:,i,prev_node[i]]=0
                global_idl[int(prev_node[i])]=0
                # print('agent_', i, 'idleness:\n',idle[i].reshape(5,5))
                # print('global idleness:\n',global_idl.reshape(5,5))
                # fa=[[True, True, True, True], [True, True, True, True]]
                # bool_f, j=forb_action(    temp_p, curr_node, temp_n)
                # if j==0 or j==1:
                #     fa[j]= bool_f
                # print(fa)
                print("current node ",curr_node[i],"dead_node ",dead_node)
                if (prev_node[i] not in dead_node):
                    print("yo") 
                    action_list[i]=CR_patrol(cloud_array[curr_node[i],i],curr_node[i],env,np.array(action_list))
                else :
                    all_routes = extract_routes()
                    adj_nodes = [s.split("to")[1] for s in all_routes if s.startswith(str(curr_node[i])+"to")]
                    action_list[i]= int(random.choice(adj_nodes))
                next_state, reward, action_list[i] = env.step(action_list[i], cloud_array[curr_node[i],i], i)
                temp_n[i]=next_state
                # print('action: ', action, 'next_state: ', next_state, 'reward: ', reward)
                #print('curr_node after step: ',curr_node, env.state)
                rou_new=str(curr_node[i])+'to'+str(next_state)
                rou_step.append(rou_curr[i])
                rou_step.append(rou_new)

                # print('next_route: ', rou_step)
                traci.vehicle.setRoute(vehID = 'veh'+str(i), edgeList = rou_step)
                rou_curr[i]=rou_new
                
        avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(global_idl, global_v_idl,sumo_step, 28)
        ma_ga.append(glo_idl)
        gav.append(np.mean(ma_ga))
        ga.append(glo_idl)
        ss.append(sumo_step)
        sumo_step+=1

   
        prev_node=curr_node.copy()
        #print('curr route: ',rou_curr)
        if sumo_step ==num_steps:
            break

    plt.plot(ss,ga, "-r", linewidth=0.6,label="Global Average Idleness")
    plt.plot(ss,gav, "-b", linewidth=4, label="Global Average Node Visit Idleness")
    plt.legend(loc="lower right")
    up=np.ceil(max(ga)/10)*10
    plt.yticks(np.linspace(0,up,int((up/10)+1), endpoint=True))
    plt.xlabel('Unit Time')
    plt.ylabel('Idleness')
    plt.title('Performance')
    plt.savefig('./check3/cr'+str(cars)+'/'+str(no_of_failed_devices)+'devices_failed/run'+str(run_id)+'/'+'run'+str(run_id)+'.png')
    peaks = []
    steps = []
    node_id = 0
    previous_element = None
    index = 0
    for element in idle_2d[:, node_id]:
        if element == 0 and previous_element is not None:
            peaks.append(previous_element)
            steps.append(index)
        previous_element = element
        index = index + 1
    # plt.plot(steps, peaks)
    for col, data_3 in enumerate(np.transpose(idle_2d)):
        worksheet.write_column(0, col+1, data_3)
    worksheet.write_column(0, 0, range(num_steps))
    global s
    message = 'q'
    s.send(message.encode('utf-8'))
    time.sleep(0.1)
    traci.close()
    # plt.show()
    sys.stdout.flush()
#end of fn

def extract_routes():
    routes = []
    with open(map_path+map_name+".edg.xml","r") as route_file:
        next(route_file)
        for line in route_file:
            if '<edge id=' in line:
                x_temp = []
                y_temp = []
                word = (line.split(' '))
                for r in range(len(word)):
                    if 'id=' in word[r]:
                        route_id = word[r].split('=')[1].strip('"')
                        routes.append(route_id)
    route_file.close()
    return routes
#end of fn


if __name__ == '__main__':
    host = socket.gethostname()  # get local machine name
    port = 8060  # Make sure it's within the > 1024 $$ <65535 range
    os.system('rm -rf ' +'./check3/cr'+str(cars)+'/'+str(no_of_failed_devices)+'devices_failed/run'+str(run_id)+'/')
    os.system('mkdir '+'./check3/cr'+str(cars)+'/'+str(no_of_failed_devices)+'devices_failed/run'+str(run_id)+'/')
    workbook = xlsxwriter.Workbook('./check3/cr'+str(cars)+'/'+str(no_of_failed_devices)+'devices_failed/run'+str(run_id)+'/'+'run.xlsx')
    s = socket.socket()
    s.connect((host, port))
    all_routes = extract_routes()
    startings = []
    # print(all_routes)
    random.shuffle(all_routes)
    for i in range(cars):
        startings.append(int(all_routes[i].split('to')[0]))
    env=rl_env()
    run(env)
    workbook.close()
    np.save('./check3/cr'+str(cars)+'/'+str(no_of_failed_devices)+'devices_failed/run'+str(run_id)+'/dead',dead_node)
    s.close()

    # startings = [all_routes.split('to')]
    # print(startings)

    
#end of main

#end of code