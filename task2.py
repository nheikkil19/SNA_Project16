import matplotlib.pyplot as plt
import numpy as np
import csv
import networkx as nx
import math
import random



G = nx.DiGraph()
k = 1000

print("Creating edges...")
fh = open("active_followers_converted.csv", "rb")
G = nx.read_edgelist(fh, delimiter=',', nodetype=int, create_using=nx.DiGraph)
print("reached the end of the link-creating process.")

print("Creating nodes from csv file...")
with open('distinct_users_from_search_table_real_map.csv', newline='') as csvfile:
    i=0
    distinctusers = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in distinctusers:
        if i > 0:
            id = int(row[0].split(",")[0])
            G.add_node(id)
        i += 1
    print("reached the end of the node-creating process.")
    
sampled_nodes = random.sample(G.nodes, k)
SG = G.subgraph(sampled_nodes)

def getListFromDegreeView(dict):
    ls = []
    for i in dict:
        ls.append(i[1])
    return ls
   
degree = G.degree()
indegree = G.in_degree()
outdegree = G.out_degree()

degreels = getListFromDegreeView(degree)
indegreels = getListFromDegreeView(indegree)
outdegreels = getListFromDegreeView(outdegree)

a = []
squarexylen = int(np.sqrt(len(degreels))) + 1

print(squarexylen)
index = 0
for i in range(squarexylen):
    x = []
    for j in range(squarexylen):
        try:
            x.append(degreels[index])
        except IndexError: # This is a terrible and hacky way to do this but it's going to have to do for now
            x.append(0)
        index += 1
    a.append(x)
    
plt.imshow(a, cmap='hot', interpolation='nearest')
#print(a)
plt.show()
