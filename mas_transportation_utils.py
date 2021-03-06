import networkx as nx
import random as random
import matplotlib.pyplot as plt
import math
import numpy as np

# fonction permettant de générer un graphe en grille aléatoire avec perturbation d'arête
# n indique le nombre de noeuds au carré
# la variable coef suppr détermine le coefficient de suppression des arêtes
# la variable show indique si il faut afficher le graphe ou non
def generate_2D_graph(n, coef_suppr=False, show=False):
    graph = nx.grid_2d_graph(n, n)  # n x n grid

    if coef_suppr != False:
        nb_suppr = int(len(list(graph.nodes)) * coef_suppr)

        random_edge(graph, nb_suppr, delete=True)

    pos = nx.spring_layout(graph, iterations=100)

    graph.remove_nodes_from(list(nx.isolates(graph)))
    graph = graph.to_directed()

    if show:
        nx.draw(graph, pos, node_color='b', node_size=20, with_labels=False)
        plt.title("Road network")
        plt.show()

    return graph


# ajoute ou supprime un nombre d'arêtes dans un graphe
def random_edge(graph, nb_edges, delete=True):
    edges = list(graph.edges)
    nonedges = list(nx.non_edges(graph))

    # random edge choice
    if delete:
        # delete chosen edge
        chosen_edges = random.sample(edges, nb_edges)
        for edge in chosen_edges:
            graph.remove_edge(edge[0], edge[1])
    # add new edge
    else:
        chosen_nonedges = random.sample(nonedges, nb_edges)
        for non_edge in chosen_nonedges:
            graph.add_edge(non_edge[0], non_edge[1])

    return graph

def print_user_perception(user, G, step_by_step=False):
    
    pos = nx.spring_layout(G, iterations=1000)  # positions for all nodes
    # nodes
    options = {"node_size": 300, "alpha": 0.8}
    colors = ['orange','pink','yellow','cyan','purple']
    if step_by_step == True :
        for i in range(len(user.node_ranges)):
            color = colors[i]
            nx.draw_networkx_nodes(G, pos, nodelist=list(user.node_ranges[i]), node_color=color, **options)

            nx.draw_networkx_nodes(G, pos, nodelist=[user.v_r], node_color="g", **options)
            nx.draw_networkx_nodes(G, pos, nodelist=[user.v_arr], node_color="r", **options)
            nx.draw(G, pos, node_color='black', node_size=20, with_labels=False)
            plt.title("Road network")
            plt.show()
    else :
        for i in range(len(user.node_ranges)):
            color = colors[i]
            nx.draw_networkx_nodes(G, pos, nodelist=list(user.node_ranges[i]), node_color=color, **options)

        nx.draw_networkx_nodes(G, pos, nodelist=[user.v_r], node_color="g", **options)
        nx.draw_networkx_nodes(G, pos, nodelist=[user.v_arr], node_color="r", **options)
        nx.draw(G, pos, node_color='black', node_size=20, with_labels=False)
        plt.title("Road network")
        plt.show()

def compute_shortest_path_distance(G, SP):
    SPd = 0
    for i in range(len(SP)-1):
        node1 = SP[i]
        node2 = SP[i+1]
        SPd += G.get_edge_data(node1,node2)[0]['length']
    return SPd

def compute_shortest_path_time(G, SP):
    SPt = 0
    for i in range(len(SP)-1):
        node1 = SP[i]
        node2 = SP[i+1]
        SPt += G.get_edge_data(node1,node2)[0]['travel_time']
    return SPt

def compute_euclidian_aggregate_distance(q_coords,p_bbox):
    de_agg = 0
    for q_coord in q_coords:
        de_agg+=compute_min_dist(q_coord,p_bbox)
    
    return de_agg     
    
def compute_min_dist(q_coord,p_bbox):
    #retourne la distance euclidienne minimale en mètres
    p_min_lon,p_min_lat,p_max_lon,p_max_lat = p_bbox
    q_min_lon,q_min_lat = q_coord
    ref_lon, ref_lat = q_min_lon, q_min_lat
    
    if q_min_lon < p_min_lon :
        ref_lon = p_min_lon
    elif q_min_lon > p_max_lon:
        ref_lon = p_max_lon
        
    if q_min_lat < p_min_lat:
        ref_lat = p_min_lat
    elif q_min_lat > p_max_lat:
        ref_lat = p_max_lat

    min_dist = math.sqrt(np.power(q_min_lon-ref_lon,2)+np.power(q_min_lat-ref_lat,2))*111000 #valeur approchée mais suffisante sinon utiliser cosinus et sinus...
    return min_dist


#fonction utile pour plus tard
#recupere tout les chemins d'un noeud à un autre avec un cutoff de w basé sur la valeur des arretes
'''def all_paths(G, source, target, weight_name, w):
    cutoff = len(G)-1
    visited = [source]
    stack = [iter(G[source])]
    weight = 0
    while stack:
        children = stack[-1]
        child = next(children, None)
        if child is None:
            stack.pop()
            visited.pop()
        elif len(visited) < cutoff:
            if child == target:
                if (visited[-1],child) in G.nodes():
                    temp = G[visited[-1]][child][0][weight_name]
                else:
                    temp = G[child][visited[-1]][0][weight_name]
                if weight+temp <= w:
                    yield visited + [target]
            elif child not in visited:
                if (visited[-1],child) in G.nodes():
                	print(
                    weight += G[visited[-1]][child][0][weight_name]
                else:
                    weight += G[child][visited[-1]][0][weight_name]
                visited.append(child)
                stack.append(iter(G[child]))
        else: 
            if child == target or target in children:
                if (visited[-1],child) in G.nodes():
                    temp = G[visited[-1]][child][0][weight_name]
                else:
                    temp = G[child][visited[-1]][0][weight_name]
                if weight+temp <= w:
                    yield visited + [target]
            stack.pop()
            visited.pop()'''
