#! /bin/python

from aberway_background_code import create, update, main_loop
import time

ColourFlip = False

    
screen, bg, lineList, nodeList = create(ColourFlip)
update(None, screen, bg, lineList, nodeList, None, None, None, None, 0)


# --- SET THESE VALUES TO AN EXAMPLE ---

# startPos = 0
# listOfNodesToPass = [10,11,14]
# length = 676.75
# error = 0.07
# Example C
startPos = 53
listOfNodesToPass = [54, 51, 38, 36]
length = 1038.42
error = 0.07
# [53, 54, 51, 41, 38, 37, 36]
# Example D

# startPos = 47
# listOfNodesToPass = [34,19,0,12]
# length = 2044.79
# error = 0.14

from aima.search import Problem, astar_search
import math



def path_update():
    ListOfNodeId = [] #set the value of this to the nodes that your path takes
    start = time.time_ns() # for timing your algorithm
    # ---------- ---------- YOUR CODE GOES HERE ---------- ----------
    def euclidean_distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    nodedict = {'activenode':[], 'connectednode': [], 'distance':[]}
    for line in lineList:
        try:
            # print(line)
            nodedict['activenode'].append(line[4][0])
            nodedict['connectednode'].append(line[4][1])
            if line[1] != None:
                nodedict['distance'].append(euclidean_distance(line[0], line[1]))
            else:
                nodedict['distance'].append(euclidean_distance(line[0][0], line[0][-1]))
                
            # For reverse path
            nodedict['activenode'].append(line[4][1])
            nodedict['connectednode'].append(line[4][0])
            if line[1] != None:
                nodedict['distance'].append(euclidean_distance(line[0], line[1]))
            else:
                nodedict['distance'].append(euclidean_distance(line[0][0], line[0][-1]))
            
                
        except Exception as e:
            print(line)
            break
        
    
    # print(nodedict)

    from collections import deque
    # Define the starting node
    start_node = startPos

    # Define the list of goal nodes
    goal_nodes = listOfNodesToPass

    # Define the maximum distance constraint
    max_distance = length

    
    def bfs(graph, start_node, goal_nodes, max_distance):
        queue = deque([(start_node, 0, [start_node], set([start_node]))])  # (node, distance from start, path, visited_nodes)
        
        while queue:
            current_node, distance, path, visited_nodes = queue.popleft()
            
            # Check if all goal nodes are in the path
            if all(node in path for node in goal_nodes):
                print("All goal nodes reached:", goal_nodes)
                return path
            
            for neighbor, neighbor_distance in get_neighbors(graph, current_node):
                if neighbor not in visited_nodes and distance + neighbor_distance <= max_distance:
                    new_path = path + [neighbor]
                    new_visited_nodes = visited_nodes.copy()
                    new_visited_nodes.add(neighbor)
                    queue.append((neighbor, distance + neighbor_distance, new_path, new_visited_nodes))
        
        print("No path found within the distance constraint.")
        return None

    def get_neighbors(graph, node):
        neighbors = []
        for i, n in enumerate(graph['activenode']):
            if n == node:
                neighbors.append((graph['connectednode'][i], graph['distance'][i]))
        return neighbors
    # Call the bfs function with the provided parameters
    path = bfs(nodedict, start_node, goal_nodes, max_distance)
    print(path)
    # ---------- ---------- ---------- ---------- ---------- ---------- ----------
    # end = time.time_ns()
    # update(ListOfNodeId, screen, bg, lineList, nodeList, startPos, listOfNodesToPass, length, error, end - start)

path_update()
main_loop()
