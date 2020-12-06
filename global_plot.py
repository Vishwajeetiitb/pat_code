import matplotlib.pyplot as plt
import numpy as np
import os
f = open("./path_name.txt", "r")
path = './data/' + f.read()
os.system('rm -rf '+path+'global_data/all')
os.system('mkdir '+path+'global_data/all')
runs = 10
for i in range(runs):
    ga = np.load(path+'global_data/run'+str(i)+'/ga.npy')
    gav = np.load(path+'global_data/run'+str(i)+'/gav.npy')
    ss = np.load(path+'global_data/run'+str(i)+'/ss.npy')
    fig = plt.figure()
    fig.set_size_inches(19.20, 10.80)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ss, ga, "-r", linewidth=0.6, label="Global Average Idleness")
    ax.plot(ss, gav, "-b", linewidth=4,
             label="Global Average Node Visit Idleness")
    plt.legend(loc="lower right")
    up = np.ceil(max(ga)/10)*10
    plt.yticks(np.linspace(0, up, int((up/10)+1), endpoint=True))
    plt.xlabel('Unit Time')
    plt.ylabel('Idleness')
    plt.title('Performance')
    plt.savefig(path+'global_data/all''/run'+str(i)+'_global.png', dpi=100)
    plt.cla()
    plt.clf()
    plt.close()
fig, ax = plt.subplots(2,5)
for i in range(runs):
    ga = np.load(path+'global_data/run'+str(i)+'/ga.npy')
    gav = np.load(path+'global_data/run'+str(i)+'/gav.npy')
    ss = np.load(path+'global_data/run'+str(i)+'/ss.npy')
    a = int(i/5)
    b = i - 5*a
    ax[a,b].plot(ss, ga, "-r", linewidth=0.6, label="Global Average Idleness")
    ax[a,b].plot(ss, gav, "-b", linewidth=4,
             label="Global Average Node Visit Idleness")
    ax[a,b].legend(loc="lower right")
    up = np.ceil(max(ga)/10)*10
    # ax[a,b].yticks(np.linspace(0, up, int((up/10)+1), endpoint=True))
    plt.xlabel('Unit Time')
    plt.ylabel('Idleness')
    plt.title('Performance')
fig.set_size_inches(19.20, 10.80)
plt.savefig(path+'global_data/all/all.png', dpi=100)
# plt.show()

