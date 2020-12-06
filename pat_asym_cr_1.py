# RL Environment for Patrolling
import socket
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import optparse
import time
import random
from collections import deque, namedtuple
from sumolib import checkBinary
import traci
import xlsxwriter
__author__ = 'meghdeep'

# RL Environment for Patrolling

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


sys.path.append(os.path.join('c:', os.sep, 'whatever',
                             'path', 'to', 'sumo', 'tools'))
sumoBinary = checkBinary("sumo-gui")
sumoCmd = [sumoBinary, "-c", "./maps/asym/grid_asym.sumocfg",
           "--tripinfo-output", "tripinfo.xml"]


class rl_env(object):

    def __init__(self):
        self.nrow, self.ncol = 6, 6
        self.stateSpace = np.array([i for i in range(36)])
        self.actionSpace = [0, 1, 2, 3]
        #Action space= {'0': 'North', '1': 'South', '2': 'East', '3': 'West'}
        self.state = 6
        self.nA = 4
        self.nS = 36
        self.reward = 0.0

    def sample(self, nn):
        act_idx = random.choice([i for i in range(len(nn))])
        return act_idx

    def set_actionSpace(self, n_edges):
        self.actionSpace = n_edges

    def step(self, next_state, idle):
        self.state = next_state
        # print('cur and next: ', curr_state, self.state)
        self.reward = idle[self.state]
        return self.state, self.reward

    def reward_out(self, idle, prev_node):
        self.reward = idle[prev_node]
        return self.reward

    def reset(self, route0):
        rou_curr = []
        rou_curr.append(route0)
        self.state = 6
        self.reward = 0.0
        traci.start(sumoCmd)
        traci.route.add('rou_0', rou_curr)
        traci.vehicle.add(vehID='veh0', routeID='rou_0', typeID="car1")
        return self.state
#end of class


def eval_met(idle, v_idle, sumo_step, n):

    avg_v_idl = np.zeros((36, 1))
    max_v_idl = np.zeros((36, 1))
    var_v_idl = np.zeros((36, 1))
    #avg idleness
    for i in range(n):
        if v_idle[i]:
            avg_v_idl[i] = np.sum(np.square(v_idle[i]))/(2*sumo_step)
    glo_v_idl = np.sum(avg_v_idl)/30
    glo_idl = np.sum(idle)/30
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
    glo_sd_v_idl = np.sum(sd_v_idl)/30
    return avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl
#end of fn


def CR_patrol(idle, c, env, an):

    neigh = [idle[i] for i in an]
    # print(neigh)
    m = max(neigh)
    idx = [i for i, j in enumerate(neigh) if j == m]
    # print('idx: ', idx)
    act_idx = random.choice(idx)
    action_node = an[act_idx]
    # print('cur and next: ', c, action_node)
    if c == action_node:
        act_idx = CR_patrol(idle, c, env, an)
    return act_idx
#end of fn


def run(env,run_id):

    global workbook
    # workbook = xlsxwriter.Workbook('./data/cr1/centre/'+'run'+str(run_id)+'.xlsx')
    np.random.seed(0)
    worksheet = workbook.add_worksheet('run'+str(run_id))
    rou_corner = "5to"+str(random.choice([11, 4]))
    rou_centre = "14to"+str(random.choice([8,15, 13, 20]))
    rou_edge_centre = "2to"+str(random.choice([7]))
    rou_curr = rou_centre
    env.reset(rou_curr)
    sumo_step = 1.0
    bn = [0, 17, 30, 31, 32, 33]
    cr = 0.0
    rl_step = 1.0
    idle = np.zeros((36, 1))
    global_idl = np.zeros((36, 1))
    global_v_idl = [[] for _ in range(36)]
    v_idle = [[] for _ in range(36)]
    edge = 0
    prev_node = env.state
    curr_node = []
    temp_n = 0
    temp_p = 6
    ga = []
    ma_ga = deque(maxlen=3000)
    gav = []
    ss = []
    num_steps = 20000
    idle_2d = np.zeros([num_steps, 36])
    while traci.simulation.getMinExpectedNumber() > 0:
        idle_2d[int(sumo_step)-1] = np.transpose(idle)
        traci.simulationStep()
        idle += 1
        global_idl += 1
        for i in bn:
            global_idl[i] = 0
            idle[i] = 0
        ed = traci.vehicle.getRoadID('veh0')
        #print('veh edge data: ',ed)
        if ed and (ed[0] != ':'):
            curr_node = ed.split('to')
            #print(curr_node)
            curr_node = int(curr_node[1])
        elif ed[0] == ':':
            curr_node = ed[1:].split('_')
            #print(curr_node)
            curr_node = int(curr_node[0])
        env.state = curr_node
        #print('p_node:',prev_node, 'c_node:',curr_node, 'temp_p: ', temp_p, 'temp_n: ', temp_n)
        # Action decision on new edge
        if prev_node != curr_node:
            temp_p = prev_node
            # print(':::::::::::::to next node::::::::::::::::')

            # print('Veh angle: ', traci.vehicle.getAngle('veh0'))
            rou_step = []
            # print(idle[prev_node])
            prev_reward = env.reward_out(idle, prev_node)[0]
            # print('reward on prev step: ', prev_reward)
            v_idle[int(prev_node)].append(prev_reward)
            glo_reward = env.reward_out(global_idl, prev_node)[0]
            global_v_idl[int(prev_node)].append(glo_reward)
            # print(global_v_idl)
            avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(
                global_idl, global_v_idl, sumo_step, 36)
            # print('global avg node visit idleness: ', glo_v_idl, '\nglobal max node visit idleness: ', glo_max_v_idl)
            # print('global avg instant idleness: ', glo_idl, '\nglobal max instant idleness: ', glo_max_idl)
            #print(np.array(v_idle).reshape(5,5))

            cr += prev_reward
            #acr=cr/sumo_step
            #print('acr: ', acr)
            idle[int(prev_node)] = 0
            global_idl[int(prev_node)] = 0
            # print('agent_', i, 'idleness:\n',idle.reshape(6,6))
            # print('global idleness:\n',global_idl.reshape(6,6))

            links = traci.lane.getLinks(
                traci.vehicle.getLaneID('veh0'), extended=False)
            s_lanes = [i[0] for i in links]
            n_edges = []
            n_nodes = []
            for nodes in s_lanes:
                n_edges.append(nodes.split('_')[0])
            for edges in n_edges:
                n_nodes.append(int(edges.split('to')[1]))
            # print(n_edges, n_nodes)
            env.set_actionSpace(n_edges)
            act_idx = CR_patrol(idle, curr_node, env, n_nodes)
            action = n_edges[act_idx]
            next_state, reward = env.step(n_nodes[act_idx], idle)
            temp_n = next_state
            # print('action: ', action, 'next_state: ', next_state, 'reward: ', reward)
            #print('curr_node after step: ',curr_node, env.state)
            rou_new = action
            rou_step.append(rou_curr)
            rou_step.append(rou_new)
            # print('next_route: ', rou_step)
            traci.vehicle.setRoute(vehID='veh0', edgeList=rou_step)
            rou_curr = rou_new

        avg_v_idl, max_v_idl, sd_v_idl, glo_v_idl, glo_max_v_idl, glo_sd_v_idl, glo_idl, glo_max_idl = eval_met(
            global_idl, global_v_idl, sumo_step, 36)
        ma_ga.append(glo_idl)
        gav.append(np.mean(ma_ga))
        ga.append(glo_idl)
        ss.append(sumo_step)

        prev_node = curr_node
        #print('curr route: ',rou_curr)
        sumo_step += 1
        if sumo_step >= num_steps:
            break

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
    path = './data/cr1/' + f.read()
    # fig, axs = plt.subplots(3, 3)
    workbook = xlsxwriter.Workbook(path+'runs2.xlsx')
    host = socket.gethostname()  # get local machine name
    port = 8000  # Make sure it's within the > 1024 $$ <65535 range
    s = socket.socket()
    s.connect((host, port))
    n_runs = 1
    for i in range(n_runs):
        run(env, i)
        print("current run", i)
    plt.legend(["run0", "run1", "run2", "run3", "run4", "run5",
                "run6", "run7", "run8"], loc="lower right")
    plt.show()
    workbook.close()
