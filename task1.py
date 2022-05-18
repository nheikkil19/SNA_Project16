import networkx as nx
import statistics
import numpy as np
import csv
import sqlite3
import random
import timeit
import statistics
from itertools import chain



start = timeit.default_timer()

G = nx.DiGraph()
k = 1000

print("Creating edges...")
fh = open("active_followers_converted.csv", "rb")
G = nx.read_edgelist(fh, delimiter=',', nodetype=int, create_using=nx.DiGraph)
print("reached the end of the link-creating process.")
stop = timeit.default_timer()
print('Time: ', stop - start)

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
stop = timeit.default_timer()
print('Time: ', stop - start)  

    
sampled_nodes = random.sample(G.nodes, k)
print("random nodes sampled.")
SG = G.subgraph(sampled_nodes)
print("Subgraph created.")
stop = timeit.default_timer()
print('Time: ', stop - start)





def getAverageFromDict(dict):
    sum = 0
    avg = 0
    for key,value in dict.items():
        sum += value
    avg = sum/len(dict)
    return avg
        
def getVarianceFromDict(dict):
    lis = []
    for key,value in dict.items():
        lis.append(value)
    arr = np.array(lis)
    var = statistics.variance(arr, xbar=None)
    return var
    

    
def getAverageFromDegreeView(dict):
    sum = 0
    avg = 0
    for i in dict:
        sum += i[1]
    avg = sum/len(dict)
    return avg    

def getVarianceFromDegreeView(dict):
    lis = []
    for i in dict:
        lis.append(i[1])
    var = statistics.variance(lis, xbar=None)
    return var

    
def getDataFromGraph(g):
    non = g.number_of_nodes()
    noe = g.number_of_edges()

    return non, noe
    
def calc_degree_centrality(g):
    degree = g.degree()
    avg_degree = getAverageFromDegreeView(degree)
    avg_degree_vari = getVarianceFromDegreeView(degree)
    return avg_degree, avg_degree_vari
    
def calc_inbetween_centrality(g):
    inbetween = nx.algorithms.centrality.betweenness_centrality(g)
    with open('inbetweencentralities_data.csv', 'w', newline='') as file:
        writer = csv.writer(file,escapechar=' ',quoting=csv.QUOTE_NONE)
        for key,value in inbetween.items():
            ls = []
            ls.append(key)
            ls.append(value)
            writer.writerow(tuple(ls))
    avg_betw = getAverageFromDict(inbetween)
    avg_betw_vari = getVarianceFromDict(inbetween)
    
    return avg_betw, avg_betw_vari
    
def calc_closeness_centrality(g):
    closeness = nx.algorithms.centrality.closeness_centrality(g)
    with open('closenesscentralities_data.csv', 'w', newline='') as file:
        writer = csv.writer(file,escapechar=' ',quoting=csv.QUOTE_NONE)
        for key,value in closeness.items():
            ls = []
            ls.append(key)
            ls.append(value)
            writer.writerow(tuple(ls))
    avg_closeness = getAverageFromDict(closeness)
    avg_closeness_vari = getVarianceFromDict(closeness)
    return avg_closeness, avg_closeness_vari
    
def calc_pgrank_centrality(g):
    pgrank = nx.pagerank(g)
    avgpgrank = getAverageFromDict(pgrank)
    avgpgrankvari = getVarianceFromDict(pgrank)
    return avgpgrank,  avgpgrankvari
    
def calc_clustering_and_shortest_path(g):
    avg_clustering = nx.average_clustering(g)
    print("Average Clustering: ", avg_clustering)
   # avg_shortest_path = nx.shortest_path_length(g)
    path_lengths = (x.values() for x in nx.shortest_path_length(g).values())
    avg_shortest_path = statistics.average(chain.from_iterable(path_lengths))
    shortest_path_vari = 0 ##This is still missing!!!!!!!    

    return avg_clustering, avg_shortest_path, shortest_path_vari

def calc_giantcomp(g):
    giant = sorted(nx.connected_components(g), key = len, reverse=True)
    g0 = g.subgraph(giant[0])
    size = g0.number_of_nodes()
    return size

undirG = G.to_undirected();
giant = calc_giantcomp(undirG)
##print("Average Shortest Path variance: ", shortest_path_vari)
print("Giant Component size: ", giant)
print("Starting data calculation...")

n, e = getDataFromGraph(SG);
print("Number Of Nodes: ", n)
print("Number Of Edges: ", e)
stop = timeit.default_timer()
print('Time: ', stop - start)

avgd, vari = calc_degree_centrality(SG)
print("Average Degree centrality: ", avgd)
print("Variance of Degree centrality: ", vari)
stop = timeit.default_timer()
print('Time: ', stop - start)

avgpgrank, avgpgrankvari = calc_pgrank_centrality(SG)
print("Average Pagerank centrality: ", avgpgrank)
print("Variance of Pagerank centrality: ",  avgpgrankvari )
stop = timeit.default_timer()
print('Time: ', stop - start)



avgbetwnectr, avgbetwcentrvari = calc_inbetween_centrality(SG)
print("Average Betweenness centrality: ", avgbetwnectr)
print("Variance of Betweenness centrality: ", avgbetwcentrvari)
stop = timeit.default_timer()
print('Time: ', stop - start)


avgclosenesscentr, avgclosenesscentrvari = calc_closeness_centrality(SG)
print("Average Closeness centrality: ", avgclosenesscentr)
print("Variance of closeness centrality: ", avgclosenesscentrvari)
stop = timeit.default_timer()
print('Time: ', stop - start)



avg_clustering, avg_shortest_path, shortest_path_vari = calc_clustering_and_shortest_path(SG)
print("Average Clustering: ", avg_clustering)
print("Average Shortest Path: ", avg_shortest_path)
print("Average Shortest Variance: ", shortest_path_vari)
stop = timeit.default_timer()
print('Time: ', stop - start)

undirG = G.to_undirected();
giant = calc_giantcomp(undirG)
##print("Average Shortest Path variance: ", shortest_path_vari)
print("Giant Component size: ", len(giant))


print("Clustering coefficient: ", avg_clustering)
print("Average Shortest Path: ", avg_shortest_path)


