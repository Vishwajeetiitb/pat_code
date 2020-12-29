# RL Environment for Patrolling
__author__='dikshant'

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

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary

sys.path.append(os.path.join('c:', os.sep, 'whatever', 'path', 'to', 'sumo', 'tools'))
sumoBinary = checkBinary("sumo-gui")
sumoCmd = [sumoBinary, "-c", "../maps/grid_5_5.sumocfg",
           "--tripinfo-output", "../maps/tripinfo.xml"]


import traci

class rl_env(object):

    def __init__(self):
        global cars
        self.nrow, self.ncol= 5, 5
        self.stateSpace=np.array([i for i in range(25)])
        self.actionSpace = [0, 1, 2, 3]
        #Action space= {'0': 'North', '1': 'South', '2': 'East', '3': 'West'}
        self.state=[0 for i in range(cars)]
        self.nA = 4
        self.nS = 25
        self.reward=[0 for i in range(cars)] #change

    def sample(self):
        action = random.choice(self.actionSpace)
        return action

    def check_step(self, curr_state, next_state, idle, action, i):
        if curr_state==next_state[i]:
            action=self.sample()
            self.state, self.reward, action=self.step(action, idle, i)
        return self.state, self.reward, action

    def step(self, action, idle, i):
        curr_state=self.state[i]
        row=curr_state//5
        col=curr_state%5
        if action == 3:
            col = max(col-1, 0)
        elif action == 0:
            row = min(row+1,self.nrow-1)
        elif action == 2:
            col = min(col+1,self.ncol-1)
        elif action == 1:
            row = max(row-1,0)
        self.state[i]=row*5+col
        # print('cur and next: ', curr_state, self.state)
        self.reward[i]=idle[self.state[i]]
        self.state, self.reward, action=self.check_step(curr_state, self.state, idle, action, i)
        return self.state[i], self.reward, action

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

    avg_v_idl=np.zeros((25,1))
    max_v_idl=np.zeros((25,1))
    var_v_idl=np.zeros((25,1))
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

def CR_patrol(idle, c, env):

    row=c//5
    col=c%5
    neigh=[idle[min(row+1,env.nrow-1)*5+col], idle[max(row-1,0)*5+col], idle[row*5+min(col+1,env.ncol-1)], idle[row*5+max(col-1, 0)]]
    if c==0:
        neigh[1], neigh[3]=0,0
    elif c==20:
        neigh[0], neigh[3]=0,0
    elif c==24:
        neigh[0], neigh[2]=0,0
    elif c==4:
        neigh[1], neigh[2]=0,0
    elif c==21 or c==22 or c==23:
        neigh[0]=0
    elif c==1 or c==2 or c==3:
        neigh[1]=0
    elif c==9 or c==14 or c==19:
        neigh[2]=0
    elif c==5 or c==10 or c==15:
        neigh[3]=0

    m = max(neigh)
    idx= [i for i, j in enumerate(neigh) if j == m]
    # print('idx: ', idx)
    # action=random.choice(idx)
    action = idx[0]
    if action == 3:
        col = max(col-1, 0)
    elif action == 0:
        row = min(row+1,env.nrow-1)
    elif action == 2:
        col = min(col+1,env.ncol-1)
    elif action == 1:
        row = max(row-1,0)
    n=row*5+col
    # print('cur and next: ', c, n)
    if c==n:
            action=CR_patrol(idle,c,env)
    return action

#end of fn

def run(env):
    global cars,all_routes
    # rou_curr = []
    # for i in range(n):
    #     rou_curr.append("rou_curr{}".format(i))
    rou_curr0= "0to"+str(random.choice([1,5]))
    rou_curr1= "24to"+str(random.choice([19,23]))
    rou_curr2= "12to"+str(random.choice([11,13, 7,17]))
    rou_curr3 = "17to"+str(random.choice([16,18, 12,22]))
    rou_curr= all_routes
    env.reset(rou_curr)
    sumo_step=1.0
    cr = [0 for i in range(cars)]
    rl_step=1.0
    idle=[np.zeros((25,1)) for _ in range(cars)]
    global_idl=np.zeros((25,1))
    global_v_idl=[[] for _ in range(25)]
    v_idle=[[[] for _ in range(25)] for _ in range(cars)]
    edge = [0 for i in range(cars)]
    prev_node=env.state
    curr_node=[0 for i in range(cars)]
    temp_n=[0 for i in range(cars)]
    temp_p=[0 for i in range(cars)]
    ga=[]
    ma_ga=deque(maxlen=3000)
    gav=[]
    ss=[]
    while traci.simulation.getMinExpectedNumber()>0:

        traci.simulationStep()
        for i in range(cars):
            idle[i]+=1
        global_idl+=1
        for car_no in range(cars):
            edge[car_no] = traci.vehicle.getRoadID('veh'+str(car_no))
        #print('veh edge data: ',edge)
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
                prev_reward=env.reward_out(idle[i], prev_node[i], i)[0]
                # print('reward on prev step: ', prev_reward)
                v_idle[i][int(prev_node[i])].append(prev_reward.copy())
                global_v_idl[int(prev_node[i])].append(glo_reward.copy())
                avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(global_idl, global_v_idl,sumo_step, 25)
                # print('global avg node visit idleness: ', glo_v_idl, '\nglobal max node visit idleness: ', glo_max_v_idl)
                # print('global avg instant idleness: ', glo_idl, '\nglobal max instant idleness: ', glo_max_idl)
                #print(np.array(v_idle).reshape(5,5))
                
                cr[i]+=prev_reward
                #acr=cr/sumo_step
                #print('acr: ', acr)
                idle[i][int(prev_node[i])]=0
                global_idl[int(prev_node[i])]=0
                # print('agent_', i, 'idleness:\n',idle[i].reshape(5,5))
                # print('global idleness:\n',global_idl.reshape(5,5))
                # fa=[[True, True, True, True], [True, True, True, True]]
                # bool_f, j=forb_action(temp_p, curr_node, temp_n)
                # if j==0 or j==1:
                #     fa[j]= bool_f
                # print(fa)
                action=CR_patrol(idle[i],curr_node[i],env)
                next_state, reward, action = env.step(action, idle[i], i)
                temp_n[i]=next_state
                # print('action: ', action, 'next_state: ', next_state, 'reward: ', reward)
                #print('curr_node after step: ',curr_node, env.state)
                rou_new=str(curr_node[i])+'to'+str(next_state)
                rou_step.append(rou_curr[i])
                rou_step.append(rou_new)
                # print('next_route: ', rou_step)
                traci.vehicle.setRoute(vehID = 'veh'+str(i), edgeList = rou_step)
                rou_curr[i]=rou_new

        avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(global_idl, global_v_idl,sumo_step, 25)
        ma_ga.append(glo_idl)
        gav.append(np.mean(ma_ga))
        ga.append(glo_idl)
        ss.append(sumo_step)

        prev_node=curr_node.copy()
        #print('curr route: ',rou_curr)
        sumo_step+=1
        if sumo_step ==40000:
            break

    plt.plot(ss,ga, "-r", linewidth=0.6,label="Global Average Idleness")
    plt.plot(ss,gav, "-b", linewidth=4, label="Global Average Node Visit Idleness")
    plt.legend(loc="lower right")
    up=np.ceil(max(ga)/10)*10
    plt.yticks(np.linspace(0,up,int((up/10)+1), endpoint=True))
    plt.xlabel('Unit Time')
    plt.ylabel('Idleness')
    plt.title('Performance')
    plt.savefig('./cr'+str(cars)+'.png', dpi=100)
    global s
    message = 'q'
    s.send(message.encode('utf-8'))
    traci.close()
    # plt.show()
    sys.stdout.flush()
#end of fn

if __name__ == '__main__':
    no_agents = [1,2,4,6,10]
    cars = 6
    host = socket.gethostname()  # get local machine name
    port = 8050  # Make sure it's within the > 1024 $$ <65535 range
    s = socket.socket()
    s.connect((host, port))
    with open('./routes.txt') as f:
        all_routes = f.read().splitlines()
    # route_file = open("./routes.txt", "r")
    # all_routes = route_file.readlines()
    # print(all_routes[3])
    startings = []
    for i in range(cars):
        startings.append(int(all_routes[i].split('to')[0]))
    # startings = [all_routes.split('to')]
    # print(startings)
    env=rl_env()
    for k in no_agents:
        cars = k
        run(env)
#end of main

#end of code