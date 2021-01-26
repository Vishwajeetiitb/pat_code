# RL Environment for Patrolling
__author__='meghdeep'

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
        self.nrow, self.ncol= 5, 5
        self.stateSpace=np.array([i for i in range(25)])
        self.actionSpace = [0, 1, 2, 3]
        #Action space= {'0': 'North', '1': 'South', '2': 'East', '3': 'West'}
        self.state=0
        self.nA = 4
        self.nS = 25
        self.reward=0

    def sample(self):
        action_node = random.choice(adj_nodes)
        return action_node

    def check_step(self, curr_state, next_state, idle, action):
        if curr_state==next_state:
            action=self.sample()
            self.state, self.reward, action=self.step(action, idle)
        return self.state, self.reward, action

    def step(self, action_node, idle):
        curr_state=self.state
        self.state=action_node
        # print('cur and next: ', curr_state, self.state)
        self.reward=idle[self.state]
        self.state, self.reward, action_node=self.check_step(curr_state, self.state, idle, action_node)
        return self.state, self.reward, action_node

    def reward_out(self, idle, prev_node):
        self.reward = idle[prev_node]
        return self.reward

    def reset(self, route0):
        rou_curr=[]
        rou_curr.append(route0)
        self.state=0
        self.reward=0
        traci.start(sumoCmd)
        traci.route.add('rou_0', rou_curr)
        traci.vehicle.add(vehID = 'veh0',routeID = 'rou_0', typeID = "car1")
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
    global adj_nodes
    adj_nodes = [s.split("to")[1] for s in routes if s.startswith(str(c)+"to")]
    adj_idle = []
    print("yo",adj_nodes,c)
    for node in adj_nodes:
        adj_idle.append(idle[int(node)])
    action_node = int(adj_nodes[adj_idle.index(max(adj_idle))])
    return action_node

#end of fn

def run(env):

    rou_curr= "0to1"
    # rou_curr= "12to"+str(random.choice([11,13,17,7]))
    env.reset(rou_curr)
    sumo_step=1.0
    cr=0.0
    rl_step=1.0
    idle=np.zeros((28,1))
    v_idle=[[] for _ in range(28)]
    edge=[0,0]
    prev_node=env.state
    ga=[]
    ma_ga=deque(maxlen=3000)
    gav=[]
    ss=[]
    while traci.simulation.getMinExpectedNumber()>0:

        traci.simulationStep()
        idle+=1
        edge=traci.vehicle.getRoadID('veh0')
        if edge and (edge[0]!=':'):
            curr_node= edge.split('to')
            curr_node=int(curr_node[1])
        elif edge[0]==':':
            curr_node=edge[1:].split('_')
            curr_node=int(curr_node[0])
        env.state=curr_node

        # Action decision on new edge
        if prev_node!=curr_node:
            print(edge)
            print('p_node:',prev_node, 'c_node:',curr_node)
            print('Veh angle: ', traci.vehicle.getAngle('veh0'))
            rou_step=[]
            prev_reward=env.reward_out(idle, prev_node)[0]
            print('reward on prev step: ', prev_reward)
            v_idle[int(prev_node)].append(prev_reward.copy())

            avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(idle, v_idle,sumo_step, 25)
            print('global avg node visit idleness: ', glo_v_idl, '\nglobal max node visit idleness: ', glo_max_v_idl)
            print('global avg instant idleness: ', glo_idl, '\nglobal max instant idleness: ', glo_max_idl)

            rl_step+=1
            cr+=prev_reward
            acr=cr/sumo_step
            print('acr: ', acr)
            print('')
            idle[int(prev_node)]=0
            # print(idle.reshape(5,5))
            lane = traci.vehicle.getLaneID('veh0')
            print(lane)
            links = traci.lane.getLinks(lane, extended=False)
            #print(links)
            s_lanes = [i[0] for i in links]
            print(s_lanes)
            action_node=CR_patrol(idle,curr_node,env)
            next_state, reward, action = env.step(action_node, idle)
            print('action: ', action, 'next_state: ', next_state, 'reward: ', reward)
            rou_new=str(curr_node)+'to'+str(next_state)
            rou_step.append(rou_curr)
            rou_step.append(rou_new)
            print('next_route: ', rou_step)
            print(':::::::::::::to next node::::::::::::::::')
            traci.vehicle.setRoute(vehID = 'veh0', edgeList = rou_step)
            rou_curr=rou_new

        avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(idle, v_idle,sumo_step, 25)
        ma_ga.append(glo_idl)
        gav.append(np.mean(ma_ga))
        ga.append(glo_idl)
        ss.append(sumo_step)

        prev_node=curr_node
        sumo_step+=1
        if sumo_step ==5000:
            break

    plt.plot(ss,ga, "-r", linewidth=0.6,label="Instantaneous Graph Idleness")
    # plt.plot(ss,gav, "-b", linewidth=4, label="Global Average Node Visit Idleness")
    # plt.legend(loc="lower right")
    plt.legend()
    up=np.ceil(max(ga)/10)*10
    plt.yticks(np.linspace(0,up,int((up/20)+1), endpoint=True))
    plt.xlabel('sumo step')
    plt.ylabel('instantaneous graph idleness')
    plt.title('Performance')
    traci.close()
    plt.show()
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
if __name__ == '__main__':
    adj_nodes = []
    routes = extract_routes()
    env=rl_env()
    run(env)
#end of main

#end of code
