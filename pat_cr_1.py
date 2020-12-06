# RL Environment for Patrolling
import xlsxwriter
import traci
from sumolib import checkBinary
from collections import deque, namedtuple
import random
import time
import optparse
import sys
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import socket
import os
__author__ = 'meghdeep'

sns.set()


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


sys.path.append(os.path.join('c:', os.sep, 'whatever',
                             'path', 'to', 'sumo', 'tools'))
sumoBinary = checkBinary("sumo-gui")
sumoCmd = [sumoBinary, "-c", "./maps/grid_5_5.sumocfg",
           "--tripinfo-output", "./maps/tripinfo.xml"]
# sumoCmd = [sumoBinary, "-c", "./maps/asym/asym.sumocfg",
#            "--tripinfo-output", "./maps/asym/tripinfo.xml"]



class rl_env(object):

    def __init__(self):
        self.nrow, self.ncol = 5, 5
        self.stateSpace = np.array([i for i in range(25)])
        self.actionSpace = [0, 1, 2, 3]
        #Action space= {'0': 'North', '1': 'South', '2': 'East', '3': 'West'}
        self.state = 0
        self.nA = 4
        self.nS = 25
        self.reward = 0

    def sample(self):
        action = random.choice(self.actionSpace)
        return action

    def check_step(self, curr_state, next_state, idle, action):
        if curr_state == next_state:
            action = self.sample()
            self.state, self.reward, action = self.step(action, idle)
        return self.state, self.reward, action

    def step(self, action, idle):
        curr_state = self.state
        row = curr_state//5
        col = curr_state % 5
        if action == 3:
            col = max(col-1, 0)
        elif action == 0:
            row = min(row+1, self.nrow-1)
        elif action == 2:
            col = min(col+1, self.ncol-1)
        elif action == 1:
            row = max(row-1, 0)
        self.state = row*5+col
        # print('cur and next: ', curr_state, self.state)
        self.reward = idle[self.state]
        self.state, self.reward, action = self.check_step(
            curr_state, self.state, idle, action)
        return self.state, self.reward, action

    def reward_out(self, idle, prev_node):
        self.reward = idle[prev_node]
        return self.reward

    def reset(self, route0):
        rou_curr = []
        rou_curr.append(route0)
        self.state = 0
        self.reward = 0
        traci.start(sumoCmd)
        traci.route.add('rou_0', rou_curr)
        traci.vehicle.add(vehID='veh99', routeID='rou_0', typeID="car1")
        return self.state
#end of class


def eval_met(idle, v_idle, sumo_step, n):
    avg_v_idl = np.zeros((25, 1))
    max_v_idl = np.zeros((25, 1))
    var_v_idl = np.zeros((25, 1))
    #avg idleness
    for i in range(n):
        if v_idle[i]:
            avg_v_idl[i] = np.sum(np.square(v_idle[i]))/(2*sumo_step)
    glo_v_idl = np.mean(avg_v_idl)
    glo_idl = np.mean(idle)
    #max idleness
    for i in range(n):
        if v_idle[i]:
            max_v_idl[i] = np.max(v_idle[i])
    glo_max_idl = np.max(idle)
    glo_max_v_idl = np.max(max_v_idl)
    #var,stdev and glob stdev
    for i in range(n):
        if v_idle[i]:
            var_v_idl[i] = (np.sum(np.power(v_idle[i], 3)) /
                            (3*sumo_step))-avg_v_idl[i]
    sd_v_idl = np.sqrt(var_v_idl)
    glo_sd_v_idl = np.mean(sd_v_idl)
    return avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl
#end of fn


def CR_patrol(idle, c, env):

    row = c//5
    col = c % 5
    neigh = [idle[min(row+1, env.nrow-1)*5+col], idle[max(row-1, 0)*5+col],
             idle[row*5+min(col+1, env.ncol-1)], idle[row*5+max(col-1, 0)]]
    if c == 0:
        neigh[1], neigh[3] = 0, 0
    elif c == 20:
        neigh[0], neigh[3] = 0, 0
    elif c == 24:
        neigh[0], neigh[2] = 0, 0
    elif c == 4:
        neigh[1], neigh[2] = 0, 0
    elif c == 21 or c == 22 or c == 23:
        neigh[0] = 0
    elif c == 1 or c == 2 or c == 3:
        neigh[1] = 0
    elif c == 9 or c == 14 or c == 19:
        neigh[2] = 0
    elif c == 5 or c == 10 or c == 15:
        neigh[3] = 0
    # print(neigh)
    m = max(neigh)
    idx = [i for i, j in enumerate(neigh) if j == m]
    # print('idx: ', idx)
    np.random.seed(0)
    action = random.choice(idx)
    # action = idx[0]
    # print('action', action)
    if action == 3:
        col = max(col-1, 0)
    elif action == 0:
        row = min(row+1, env.nrow-1)
    elif action == 2:
        col = min(col+1, env.ncol-1)
    elif action == 1:
        row = max(row-1, 0)
    n = row*5+col
    # print('cur and next: ', c, n)
    if c == n:
        action = CR_patrol(idle, c, env)
    return action

#end of fn

 
def run(env, run_id):
    global workbook,path
    # workbook = xlsxwriter.Workbook('./data/cr1/centre/'+'run'+str(run_id)+'.xlsx')
    np.random.seed(0)
    worksheet = workbook.add_worksheet('run'+str(run_id))
    rou_corner = "0to"+str(random.choice([1, 5]))
    rou_centre = "12to"+str(random.choice([11, 13, 17, 7]))
    rou_edge_centre = "2to"+str(random.choice([7]))
    rou_curr = rou_centre
    env.reset(rou_curr)
    sumo_step = 1.0
    cr = 0.0
    rl_step = 1.0
    idle = np.zeros((25, 1))
    v_idle = [[] for _ in range(25)]
    edge = [0, 0]
    prev_node = env.state
    ga = []
    ma_ga = deque(maxlen=3000)
    gav = []
    ss = []
    num_steps = 20000
    idle_2d = np.zeros([num_steps, 25])
    while traci.simulation.getMinExpectedNumber() > 0:
        idle_2d[int(sumo_step)-1] = np.transpose(idle)
        traci.simulationStep()
        idle += 1
        edge = traci.vehicle.getRoadID('veh99')
        if edge and (edge[0] != ':'):
            curr_node = edge.split('to')
            curr_node = int(curr_node[1])
        elif edge[0] == ':':
            curr_node = edge[1:].split('_')
            curr_node = int(curr_node[0])
        env.state = curr_node

        # Action decision on new edge
        if prev_node != curr_node:
            # print(edge)
            # print('p_node:', prev_node, 'c_node:', curr_node)
            # print('Veh angle: ', traci.vehicle.getAngle('veh99'))
            rou_step = []
            prev_reward = env.reward_out(idle, prev_node)[0]
            # print('reward on prev step: ', prev_reward)
            v_idle[int(prev_node)].append(prev_reward.copy())

            avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(
                idle, v_idle, sumo_step, 25)
            # print('global avg node visit idleness: ', glo_v_idl,
            #       '\nglobal max node visit idleness: ', glo_max_v_idl)
            # print('global avg instant idleness: ', glo_idl,
            #       '\nglobal max instant idleness: ', glo_max_idl)

            rl_step += 1
            cr += prev_reward
            acr = cr/sumo_step
            # print('acr: ', acr)
            # print('')
            idle[int(prev_node)] = 0
            # print(idle.reshape(5, 5))
            lane = traci.vehicle.getLaneID('veh99')
            # print(lane)
            links = traci.lane.getLinks(lane, extended=False)
            #print(links)
            s_lanes = [i[0] for i in links]
            # print(s_lanes)
            action = CR_patrol(idle, curr_node, env)
            next_state, reward, action = env.step(action, idle)
            # print('action: ', action, 'next_state: ',
            #       next_state, 'reward: ', reward)
            rou_new = str(curr_node)+'to'+str(next_state)
            rou_step.append(rou_curr)
            rou_step.append(rou_new)
            # print('next_route: ', rou_step)
            # print(':::::::::::::to next node::::::::::::::::')
            # print(rou_step)
            traci.vehicle.setRoute(vehID='veh99', edgeList=rou_step)
            rou_curr = rou_new

        avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(
            idle, v_idle, sumo_step, 25)
        ma_ga.append(glo_idl)
        gav.append(np.mean(ma_ga))
        ga.append(glo_idl)
        ss.append(sumo_step)

        prev_node = curr_node
        sumo_step += 1
        if sumo_step == num_steps:
            break
    os.system('rm -rf '+path+'global_data/run'+str(run_id))
    os.system('mkdir '+path+'global_data/run'+str(run_id))
    np.save(path+'global_data/run'+str(run_id)+"/gav",np.array(gav))
    np.save(path+'global_data/run'+str(run_id)+"/ga",np.array(ga))
    np.save(path+'global_data/run'+str(run_id)+"/ss",np.array(ss))
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
    plt.plot(steps, peaks)
    for col, data in enumerate(np.transpose(idle_2d)):
        worksheet.write_column(0, col+1, data)
    worksheet.write_column(0, 0, range(num_steps))
    global s
    message = 'q'
    s.send(message.encode('utf-8'))
    traci.close()
    sys.stdout.flush()
#end of fn


if __name__ == '__main__':
    env = rl_env()
    f = open("./path_name.txt", "r")
    path = './data/' + f.read()
    os.system('rm -rf '+path+'global_data')
    os.system('mkdir '+path+'global_data')
    # fig, axs = plt.subplots(3, 3)
    workbook = xlsxwriter.Workbook(path+'runs.xlsx')
    host = socket.gethostname()  # get local machine name
    port = 8000  # Make sure it's within the > 1024 $$ <65535 range
    s = socket.socket()
    s.connect((host, port))
    n_runs = 10
    for i in range(n_runs):
        run(env, i)
        print("current run", i)
    plt.legend(["run0", "run1", "run2", "run3", "run4", "run5",
                "run6", "run7", "run8"], loc="lower right")
    plt.show()
    workbook.close()

#end of main

#end of code
