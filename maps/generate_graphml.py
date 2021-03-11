import os
import optparse
import codecs
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
#from collections import OrderedDict
import re
pos = {}


def e_distance (x,y):
    sum = 0
    for r in range(len(x)-1):
        sum += np.sqrt((x[r+1]-x[r])**2 + (y[r+1]-y[r])**2 )
    return sum

pos = {}
G = nx.DiGraph()

optParser = optparse.OptionParser(usage="usage: %prog --input=file.osm [options]")
optParser.add_option("--input_edg", dest="inFile_edg", default="grid_5_5_final.edg.xml", help="specifies the edge file to open")
optParser.add_option("--input_nod", dest="inFile_nod", default="grid_5_5_final.nod.xml", help="specifies the node file to open")
optParser.add_option("--output", dest="outFile", default="gird_5_5_final.graphml", help="specifies the name of the graphml file generated")

options, args = optParser.parse_args()

# Deal with required argument (1)
if not os.path.isfile(options.inFile_edg):
    optParser.error("Invalid edg input file.")

if not os.path.isfile(options.inFile_nod):
    optParser.error("Invalid nod input file.")

with codecs.open(options.inFile_nod, 'r', 'utf-8') as f:
    lines = f.read().splitlines()
    for line in lines:
        # If-statement after search() tests if it succeeded
        if "<node id" in line:
          value =  re.findall(r'([\w\.-]+=\"(.*?)\")', line)
          if 'id' in value[0][0]:
              key_value = value[0][1]
          if 'x' in value[1][0]:
              x_value = float(value[1][1])
          if 'y' in value[2][0]:
              y_value = float(value[2][1])
          pos[key_value] =(x_value, y_value)
        else:
          pass
f.close()
#print (pos.items())
for key in pos:
    G.add_node(key)
for node,value in pos.items():
    #print (node, value)
    G.node[node]['x']=value[0]
    G.node[node]['y']=value[1]

#for key, values in pos.items():
#	print key, values, values[0], values[1]

with codecs.open(options.inFile_edg, 'r', 'utf-8') as f:
    lines = f.read().splitlines()
    for line in lines:
        #print (line)
        # If-statement after search() tests if it succeeded
        if "<edge id" in line:
          x, y = [],[]
          value = re.findall(r'([\w\.-]+=\"(.*?)\")', line)
          for r in range(len(value)):
              if 'id=' in value[r][0]:
                  id_val = value[r][1]
              if 'from' in value[r][0]:
                  from_key = value[r][1]
              if 'to' in value[r][0]:
                  to_key = value[r][1]
              if 'shape=' in value[r][0]:
                  shape_cord = value[r][1]
                  #print ('shape_coordinates:',value[r][1])
                  shape_cord = shape_cord.split(' ')
                  shape_cord = [i for i in shape_cord if i]
                  for i in range (len(shape_cord)):
                      co_ord = shape_cord[i].split(',')
                      x.append(float(co_ord[0]))
                      y.append(float(co_ord[1]))
          if "shape" not in line:
            p1 = pos[from_key]
            p2 = pos[to_key]
            distance = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
            G.add_edge(from_key, to_key, name=id_val, length = float(distance))
          else:
            distance = float(e_distance (x,y))
            G.add_edge(from_key, to_key, name=id_val, length = distance)		
		
		
				
	  
		
		#print (distance)
		

f.close()


#nx.draw(G,pos=pos,with_labels=True)
#plt.show()
nx.write_graphml(G, options.outFile)
print("Sucess..........")

