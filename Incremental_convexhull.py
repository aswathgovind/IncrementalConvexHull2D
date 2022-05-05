# import matplotlib.pyplot as plt
import csv
import math
import sys
import numpy as np
import time
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from collections import namedtuple
from sympy import Triangle

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

Point = namedtuple('Point', ['x', 'y'])

CoOrd = []

def Average(lst):
    return sum(lst) / len(lst)

def SepPoints(data):
    xpoints = []
    ypoints = []

    for i in range(len(data)):
        xpoints.append((data[i][0]))
        ypoints.append((data[i][1]))
       
    return xpoints,ypoints

def isOnRight(p0, p1, p2):
    v1 = [p1[0] - p0[0], p1[1] - p0[1]]
    v2 = [p2[0] - p0[0], p2[1] - p0[1]]
    det = v1[0] * v2[1] - v1[1] * v2[0]
    if det >= 0:
        return False
    else:
        return True

def XOR_Gate (a, b):
    if a != b:
        return 1
    else:
        return 0

def verify_transition_point(prev_point,point,next_point,pt):
    prev_pointComp = isOnRight(pt,prev_point,point)
    next_pointComp = isOnRight(pt,point,next_point)
    if(XOR_Gate(prev_pointComp,next_pointComp)):
        if(prev_pointComp == False and next_pointComp == True):
            return True,0
        elif(prev_pointComp == True and next_pointComp == False):
            return True,1
    else:
        return False,2

def check_hull(Hull_Vertices,Point):
    left_chain = []
    left_vertex = []

    right_chain = []
    prev_tangency_point = 0
    lower_tangentVertices = 0
    upper_tangentVertices = 0
    is_inside = True

    curr_edge = [0,0]
    point_of_tangency = []

    for count in range(0,len(Hull_Vertices),1):
        if(count+1 == len(Hull_Vertices)):
            curr_edge = [Hull_Vertices[count],Hull_Vertices[0]]
            flag,loc = verify_transition_point(Hull_Vertices[count-1],Hull_Vertices[count],Hull_Vertices[0],Point)
            if(flag):
                point_of_tangency.append((Hull_Vertices[count],loc))
                #print("Note==>",point_of_tangency)

        else:
            curr_edge = [Hull_Vertices[count],Hull_Vertices[count+1]]
            flag,loc = verify_transition_point(Hull_Vertices[count-1],Hull_Vertices[count],Hull_Vertices[count+1],Point)
            if(flag):
                point_of_tangency.append((Hull_Vertices[count],loc))
                #print("Note==>",point_of_tangency)

        if(isOnRight(Point,curr_edge[0],curr_edge[1]) != True):
            left_chain.append([curr_edge[0],curr_edge[1]])
            left_vertex.append(curr_edge[0])
        else:
            is_inside = False
            right_chain.append([curr_edge[0],curr_edge[1]])

    #print("left Chain:",left_chain)
    #print("right Chain:",right_chain)

    if (is_inside == False):
        if(point_of_tangency[0][1] == 0):
            lower_tangentVertices = point_of_tangency[0][0] 
            upper_tangentVertices = point_of_tangency[1][0]
        else:
            upper_tangentVertices = point_of_tangency[0][0] 
            lower_tangentVertices = point_of_tangency[1][0] 

        prev_tangency_point = Hull_Vertices[(Hull_Vertices.index(lower_tangentVertices)- 1) % len(Hull_Vertices)]

        #print("Initial Hull",Intial_hull)
        #print("Transition Vertex 1:",lower_tangentVertices)
        #print("Transition Vertex 2:",upper_tangentVertices)
        #print("TransitionVertices1 index:",Hull_Vertices.index(lower_tangentVertices))
        #print("TransitionVertices2 index:",Hull_Vertices.index(upper_tangentVertices))
        #print("Prev_point of lower tangency",Hull_Vertices.index(lower_tangentVertices),prev_tangency_point)

    return is_inside,left_chain,right_chain,lower_tangentVertices,upper_tangentVertices,left_vertex,prev_tangency_point

def collinearity_check(x1, y1, x2, y2, x3, y3):
    a = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
 
    if (a == 0):
        return True
    else:
        return False

# Driver code 
if __name__=="__main__":
      
    # with open('Input_37.txt') as f:
    #     reader = csv.reader(f)
    #     for count, (c1, c2) in enumerate(reader):
    #         CoOrd.append((float(c1),float(c2)))
    
    

    no_of_points = 1000000 
    for i in range(0, no_of_points):
        CoOrd.append((np.random.randint(low=-79005000, high=39700000), np.random.randint(low=-333000, high=7370000)))

    x_pts,y_pts = SepPoints(CoOrd)

    start_time = time.time()

    if(collinearity_check(CoOrd[0][0],CoOrd[0][1],CoOrd[1][0],CoOrd[1][1],CoOrd[2][0],CoOrd[2][1])):
        #print("Initial points are collinear. Run Again")
        sys.exit()
    else:
        Intial_hull = [CoOrd[0],CoOrd[1],CoOrd[2]]

    global polygon1
    times= []
    leftvertices = []

    plt.scatter(x_pts,y_pts,c='violet')
    for i in range(3,len(CoOrd),1):
        # plt.clf()
        # plt.scatter(x_pts,y_pts,c='violet')
        
        point = CoOrd[i]         

        
        point_flag,left_vertex_chain,right_vertex_chain,tangent1,tangent2,leftvertices,prev_Tangpoint = check_hull(Intial_hull,point)
        polygon3 = Polygon(Intial_hull)
        x, y = polygon3.exterior.xy
        # plt.plot(x, y, c="cyan")
    
        # if(point_flag):
        #     print("Point is inside. So don't do anything")
        #     # plt.scatter(point[0], point[1], c="green")
        # else:
        if(point_flag == False):
            #print("Point is outside. So Update hull")
            prev_point_idx = leftvertices.index(prev_Tangpoint)
            leftvertices.insert(prev_point_idx+1,tangent1)
            tanpoint_idx = leftvertices.index(tangent1)
            leftvertices.insert(tanpoint_idx+1,point)
            Intial_hull = leftvertices
            # plt.scatter(point[0], point[1], c="red")
            #print(" Initial hull in process ",Intial_hull)
            # plt.pause(0.3)

        # elapsed_time = time.time() - start_time
        # times.append(elapsed_time)
        # print("Time elasped to process a point:",elapsed_time)
        # print("left vertices==>",leftvertices)
        #print("Hull ==>",Intial_hull)

        # polygon2 = Polygon(Intial_hull)
        # x, y = polygon2.exterior.xy
        # plt.plot(x, y, c="yellow")
        # plt.pause(0.5)

    # plt.clf()
    # plt.scatter(x_pts,y_pts,c='violet')

    print("--- Time taken to form a convex hull for %s points is %s seconds ---" % (no_of_points,(time.time() - start_time)))

    polygon1 = Polygon(leftvertices)
    x, y = polygon1.exterior.xy
    plt.plot(x, y, c="green",linewidth=2)

    # average = Average(times)


  
    print("Done ")

    plt.show()