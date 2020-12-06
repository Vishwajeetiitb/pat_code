import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
# RunId = input('enter run id\n')
# RunId = int(RunId)
RunId = 0
# ignore = [0,17,30,31,32,33]
f = open("./path_name.txt", "r")
path = './data/' + f.read()
os.system('rm -rf '+path+'individual/patterns_img')
os.system('mkdir '+path+'individual/patterns_img')
for i in range(10):
    figName = path+'individual/patterns_img/run' + \
        str(RunId) + ' pattern.png'
    run = np.load(path+'individual/runs/run'+str(RunId)+'.npy')
    # for k in ignore:
    #     run[:,k+1]=1
    df = np.where(run == 0)
    print(run)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x = df[0][400:500]
    y = df[1][400:500]-1
    print(len(df[1]))
    for i in range(y.shape[0]):
        plt.annotate(y[i], (x[i], y[i]),
                     textcoords="offset points", xytext=(0, 0), ha='center')
    ax.plot(x, y)
    ax.plot(x, y, 'o', color='r')
    fig.set_size_inches(19.20, 10.80)
    plt.xlabel('time step')
    plt.ylabel('node id')
    # minor_ticks = np.arange(0, 25, 50)
    # ax.set_xticks(minor_ticks, minor=True)
    plt.grid()
    # plt.tight_layout()
    plt.title('run'+str(RunId)+' pattern')
    # ax.set
    plt.savefig(figName, dpi=100,bbox_inches = 'tight')
    # fig.clear()
    print('run' + str(RunId)+' done')
    RunId +=1
fig, axs = plt.subplots(2,5)
RunId  = 0
for i in range(10):
    run = np.load(path+'individual/runs/run'+str(RunId)+'.npy')
    df = np.where(run == 0)
    a = int(RunId/4)
    b = RunId - a*4
    # print(a,b)
    x = df[0][400:500]
    y = df[1][400:500]-1

    for i in range(y.shape[0]):
        axs[a,b].annotate(y[i], (x[i], y[i]),
                     textcoords="offset points", xytext=(0, 0), ha='center')
    axs[a,b].plot(x, y)
    axs[a,b].plot(x, y, 'o', color='r')
    plt.xlabel('time step')
    plt.ylabel('node id')
    minor_ticks = np.arange(0, 25, 50)
    axs[a,b].set_xticks(minor_ticks, minor=True)
    plt.grid()
    plt.title('run'+str(RunId)+' pattern')
    # fig.clear()
    print('run' + str(RunId)+' done')
    RunId +=1
fig.set_size_inches(19.20, 10.80)
# plt.tight_layout()
plt.savefig(path+'individual/patterns_img/run pattern.png',bbox_inches = 'tight', dpi=500)
# plt.show()
