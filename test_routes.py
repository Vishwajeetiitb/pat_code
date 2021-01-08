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