
# coding: utf-8

# In[68]:


import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import pandas as pd
import random as rd
from copy import deepcopy
from sys import exit
from sklearn.cluster import KMeans
import math


def generate_circular_points(h,k,l,r,number):
    points = []
    for i in range(number):
        points.append((h + math.cos(2*math.pi/number*i)*r, k + math.sin(2*math.pi/number*i)*r , l))
    return points

def create_circular_graph(points):
    graph = {}
    node= range(len(points))
    for i in range(len(points)-1):
        graph[node[i]] = ([points[i]],[points[i+1]])
    graph[len(points)-1] = ([points[len(points)-1]],[points[0]])
    return graph

def euclid_dist(test_point,X):
    x1 = test_point[0]
    y1 = test_point[1]
    z1 = test_point[2] 
    x2 = X[0]
    y2 = X[1]
    z2 = X[2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)



def create_dist_matrix(G):
    size = len(G)
    D = np.zeros((size,size), dtype=int)
    for i in range(size):
        for j in range(size):
            D[i][j] = abs(G.keys()[i]-G.keys()[j])
    return D

def calc_nearest_to_X(points,X):
    dist = 99999
    argmin = -1
    for i in range(len(points)):
        dist_i = euclid_dist(points[i],X)
        if (dist_i < dist):
            dist = dist_i
            argmin = i
    return argmin
            
    
def update(points,winner,X,D,Tmax,t):
    #inverse of time
    eta = 1 - (t/float(Tmax))
    
    #constant
    #eta = 0.3
    
    #power series
    #eta = 0.7 * math.exp(t/float(Tmax))
    
    sigma = math.exp (-(t/float(Tmax)))
    #mul = []
    for j in range(len(points)):
        multiplier = eta * math.exp(-((D[winner][j])/float(2 * sigma)))
        #mul.append(multiplier)
        points[j] = points[j] + multiplier * (X - points[j])
    #print max(mul)
    return points


def draw_figure(data, points):
    
    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    
    ax.scatter(data[:,0], data[:,1], data[:,2], c="Black",marker=".",alpha = 0.7)
    ax.scatter(*zip(*points),s=100,c="red",marker="o",alpha=1)
    #ax.plot(*zip(*points),c="red")
    
    plt.rcParams["figure.figsize"] = [16,9]
    plt.show()
    

def SOM(data,no_of_points,Tmax,radius):
    
    #randomly choose x,y,z coordinates of a circle within data coordinate limits
    circle_x = rd.uniform(np.max(data[0]),np.min(data[0]))
    circle_y = rd.uniform(np.max(data[1]),np.min(data[1]))
    circle_z = rd.uniform(np.max(data[2]),np.min(data[2]))
    
    #gather k sequential circumference points of a circle centered at (x,y,z)
    points = np.array(generate_circular_points(circle_x,circle_y,circle_z,radius,no_of_points))
    initial_points = points
    
    #generate a circular graph G out of these points
    G = create_circular_graph(points)
    
    #generate the distance matrix for the vertices of G
    D = create_dist_matrix(G)
    
    #iterate Tmax times to fit the graph to the data points
    for t in range(Tmax):
        X = data[np.random.randint(data.shape[0]),:]
        winner = calc_nearest_to_X(points,X)
        points = update(points,winner,X,D,Tmax,t)
        G = create_circular_graph(points) 
        
    iterable_points = list(map(tuple,points))
    draw_figure(data, iterable_points)
    
    return G, iterable_points    


def compute_activities(data):
    activities = []
    for j in range(len(data)-1):
        activities.append(data[j+1] - data[j])
    return np.array(activities)

def actions_clusters(activities, no_of_clusters):    
    kmeans = KMeans(n_clusters=no_of_clusters)
    kmeans.fit(activities)
    y_kmeans = kmeans.predict(activities)
    centers = kmeans.cluster_centers_
    """    
    fig1 = plt.figure()
    ax1 = p3.Axes3D(fig1)
    ax1.scatter(activities[:, 0], activities[:, 1], activities[:, 2], c=y_kmeans, s=50)
    ax1.scatter(centers[:, 0], centers[:, 1], centers[:,2], c='red', s=300, alpha=1)
    """
    return y_kmeans,centers

def loc_clusters(data,SOM_centers):    
    y_SOM = []
    for j in range(len(data)):
        y_SOM.append(calc_nearest_to_X(SOM_centers,data[j]))

    return y_SOM

def calc_quant_error(data,y_SOM,loc_dict):    
    quant_error = []
    N = len(data)
    for j in range(N):        
        quant_error.append(euclid_dist(data[j],np.array(loc_dict[y_SOM[j]])))
    return(sum(quant_error)/float(N))

def map_act_num_to_coord(k_means_centers):
    activity_dict = {}
    for j in range(len(k_means_centers)):
        activity_dict[j] = k_means_centers[j]
    return activity_dict

def map_loc_num_to_coord(SOM_centers):
    loc_dict = {}
    for j in range(len(SOM_centers)):
        loc_dict[j] = SOM_centers[j]
    return loc_dict

def compute_prev_action(y_kmeans, no_of_act_clusters):
    #rows = previous actions, columns = present action
    prev_act_matrix = np.zeros((no_of_act_clusters,no_of_act_clusters))
    for i in range(1,len(y_kmeans)):
        prev_act_matrix[y_kmeans[i-1]][y_kmeans[i]] += 1
    for i in range(no_of_act_clusters):
        prev_act_matrix[i] = np.divide(prev_act_matrix[i], np.sum(prev_act_matrix[i]))  
    return prev_act_matrix


def conditional_probab_act(probab_matrix,prev_act_matrix, loc, prev_act, no_of_act_clusters):
    max_cond_probab = np.zeros((no_of_act_clusters,1))
    for i in range(no_of_act_clusters):
        max_cond_probab[i] = (probab_matrix[loc][i]*prev_act_matrix[prev_act][i])/float(np.sum(prev_act_matrix[prev_act])*np.sum(probab_matrix[loc]))

    return np.argmax(max_cond_probab) 
    

def compute_probab_matrix(y_SOM, no_of_loc_clusters, y_kmeans, no_of_act_clusters):

    probab_matrix = np.zeros((no_of_loc_clusters,no_of_act_clusters))
    for i in range(len(y_kmeans)):
        probab_matrix[y_SOM[i],y_kmeans[i]] += 1
    for i in range(no_of_loc_clusters):
        probab_matrix[i] = np.divide(probab_matrix[i], np.sum(probab_matrix[i]))     
    return probab_matrix

def mid_point(test_point,X):
    x1 = test_point[0]
    y1 = test_point[1]
    z1 = test_point[2] 
    x2 = X[0]
    y2 = X[1]
    z2 = X[2]
    return ((x1 + x2)/float(2), (y1 + y2)/float(2), (z1 + z2)/float(2))


def trajectory(data, probab_matrix, SOM_centers, activity_dict, Tmax):
    
    X = data[np.random.randint(data.shape[0]),:]
    learnt_trajectory = X
    
    for i in range(Tmax):
        a = calc_nearest_to_X(SOM_centers,X)
        b = np.argmax(probab_matrix[a])
        X = X + activity_dict[b]
        learnt_trajectory = np.vstack((learnt_trajectory, X))
    
    return learnt_trajectory


def trajectory1(data, probab_matrix, SOM_centers, activity_dict, loc_dict, no_of_loc_clusters, Tmax, G):
    
    X = data[np.random.randint(data.shape[0]),:]
    initial = X
    learnt_trajectory = X
    
    for i in range(Tmax):
        a = calc_nearest_to_X(SOM_centers,X)
        b = np.argmax(probab_matrix[a])
        c = G[a][1][0]
        X = mid_point(X + activity_dict[b], c)
        learnt_trajectory = np.vstack((learnt_trajectory, X))
    
    return initial, learnt_trajectory


def trajectory2(data, probab_matrix, prev_act_matrix, SOM_centers, activity_dict, loc_dict, no_of_loc_clusters, Tmax, G):
    
    X = data[np.random.randint(data.shape[0]),:]
    initial = X
    learnt_trajectory = X
    #initial prev_act = max of probab matrix
    prev_act = np.argmax(probab_matrix[calc_nearest_to_X(SOM_centers,X)])
    
    for i in range(Tmax):
        a = calc_nearest_to_X(SOM_centers,X)
        b = conditional_probab_act(probab_matrix,prev_act_matrix, a, prev_act, no_of_act_clusters)
        prev_act = b
        c = G[a][1][0]
        X = mid_point(X + activity_dict[b], c)
        learnt_trajectory = np.vstack((learnt_trajectory, X))
    
    return initial, learnt_trajectory



# Main 
if __name__ == '__main__':
    
    
    # Reading the data from a CSV file using pandas
    trajectory = pd.read_csv('q3dm1-path1.csv',sep=',',header=None)
    data = np.array((trajectory[0].values, trajectory[1].values, trajectory[2].values))
    data = data.transpose()
    
    no_of_loc_clusters = 50 
    no_of_act_clusters = 50 
    Tmax = 10000

    G , b = SOM(data,no_of_loc_clusters,Tmax,50)
    activities = compute_activities(data) 
    y_kmeans,centers = actions_clusters(activities, no_of_act_clusters) 
    y_SOM = loc_clusters(data, b) 
    loc_dict = map_loc_num_to_coord(b)
    activity_dict = map_act_num_to_coord(centers) 
    quant_error = calc_quant_error(data,y_SOM,loc_dict) 
    PM = compute_probab_matrix(y_SOM, no_of_loc_clusters, y_kmeans, no_of_act_clusters)
    PAM = compute_prev_action(y_kmeans, no_of_act_clusters)

    #LT = trajectory(data, PM , b , activity_dict, Tmax) 
    #X, LT = trajectory1(data, PM, b, activity_dict, loc_dict, no_of_loc_clusters, Tmax, G)
    X, LT = trajectory2(data, PM, PAM, b, activity_dict, loc_dict, no_of_loc_clusters, Tmax, G)

    fig = plt.figure() 
    ax = p3.Axes3D(fig) 
    ax.scatter(data[:,0], data[:,1], data[:,2], c="Black",marker=".",alpha = 0.7) 
    #ax.scatter(*zip(*LT),c="red",marker="o",alpha=1,s=80)
    ax.plot(*zip(*LT),c="red")
    ax.scatter(X[0],X[1],X[2],c="Blue",marker="*",alpha=1,s=300) 
    plt.rcParams["figure.figsize"] = [16,9] 
    plt.show()

