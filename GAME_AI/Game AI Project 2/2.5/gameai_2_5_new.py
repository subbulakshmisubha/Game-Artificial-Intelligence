from collections import deque
from heapq import heappush, heappop
import argparse

import sys
from copy import deepcopy

import numpy as np
import networkx as nx
import PySide.QtGui as QtGui

from gameai_2_5_gui_new import GridGUi
INF = float('inf')
#the function to find the euclidean distance needed by a star algorithm
def euclidean_distance(a, b):
    x_coordinate, y_coordinate = a
    x1_coordinate, y1_coordinate = b
    return ((x_coordinate - x1_coordinate) ** 2 + (y_coordinate - y1_coordinate) ** 2) ** 0.5


## dijikstra algorithm to find the path given the source and destination
def dijkstra_algorithm(lattice_grid,src,dest):
     
    fringe, closed = [(0, src)], set()
    distances, parents = {src: 0}, {}
    while fringe:
        r, u = heappop(fringe)
        if u not in closed:
            closed.add(u)
            if u == dest: break
            for v in nx.all_neighbors(lattice_grid, u):
                d = distances.get(u, INF) + 1
                if d < distances.get(v, INF):
                    distances[v] = d
                    parents[v] = u
                heappush(fringe, (distances[v], v))  
       
  
    path = deque([])
    while dest in parents:
        path.appendleft(dest)
        dest = parents[dest]
    path.appendleft(src)
    return path
#the arguments parser is the function for parsing and extracting the arguments provided from the command line
def argumentParser():
    parser = argparse.ArgumentParser()
   
    parser.add_argument('-m', '--matrixfile')
    parser.add_argument('-src', '--source')
    parser.add_argument('-dest', '--dest')
    parser.add_argument('-r', '--rotated', default=1, type=int)
    
    return parser.parse_args()


def main():
    args = argumentParser()
    #Source node is loaded from the matrix file
    src_nodes = np.loadtxt(args.matrixfile, dtype=int)
    rotated = bool(args.rotated)
    
    if rotated:
        working_array = np.rot90(src_nodes, 3)
    else:
        working_array = deepcopy(src_nodes)

    #the wall nodes are the nonzero elements of the map.those are extracted .
    wall_nodes = map(lambda e: tuple(e),
                     np.transpose(np.nonzero(working_array)))
    
    ##extracting grid width and height from the matrix
    grid_width, grid_height = src_nodes.shape
    
    #source node and target nodes are extracted from the input argument which the user has provided
    input_source_node = tuple(map(int, args.source.split(',')))
    input_target_node = tuple(map(int, args.dest.split(',')))
    
    #for the networkx implementation of the algorithms it requires the input to be in the form of 2d grid to find the path hence making a 2d grid 
    lattice = nx.grid_2d_graph(grid_width, grid_height)

    ##the wall nodes should not be a part of the path hence it is being removed.
    lattice.remove_nodes_from(wall_nodes)
    assert len(lattice.nodes()) == (grid_width * grid_height - len(wall_nodes))
    print args.source.split(',')
    print map(int, args.source.split(','))
   

    print tuple(map(int, args.source.split(',')))
   
    if not rotated:
       #calculation the source and destination nodes based on the used input	
        source_node = (grid_height - 1 - input_source_node[1], input_source_node[0])
        target_node = (grid_height -1 - input_target_node[1], input_target_node[0])
    else:
        source_node, target_node = input_source_node, input_target_node
    
    #finding the dijkstra path using the shortest path....
    path_dijkstra = dijkstra_algorithm(lattice, source_node, target_node)
    
    #finding the aStar path using networkX implementation
    path_astar = nx.astar_path(lattice, source_node, target_node, euclidean_distance)

    
    qt_app = QtGui.QApplication(sys.argv)
    
    ##Gui of the dijkstra path
    window_dijkstra = GridGUi(num=1,_map=src_nodes, path=path_dijkstra,rotated=args.rotated)
    ##Gui of the Astar path
    window_astar = GridGUi(num=2,_map=src_nodes, path=path_astar,rotated=args.rotated)
    
	
	##to display the window for dijkstra algorithm
    window_dijkstra.show()
	##to display the window for Astar algorithm
    window_astar.show()
    
    window_dijkstra.raise_()
    window_astar.raise_()
    
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    main()
