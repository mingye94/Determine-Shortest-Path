"""6.009 Lab 5 -- Don't Turn Left!"""

# NO ADDITIONAL IMPORTS
def convert(shortest):
    if shortest != []:
        road_list = []
        for i in range(len(shortest) - 1):
            diction = {}
            diction['start'] = shortest[i]
            diction['end'] = shortest[i+1]
            road_list.append(diction)
        print(road_list)
        return road_list
    else:
        return None

def shortest_path(edges, start, end):
    """
    Finds a shortest path from start to end using the provided edges

    Args:
        edges: a list of dictionaries, where each dictionary has two items. 
            These items have keys `"start"` and `"end"` and values that are 
            tuples (two integers), to specify grid locations.
        start: a tuple representing our initial location.
        end: a tuple representing the target location.

    Returns:
        A list containing the edges taken in the resulting path if one exists, 
            None if there is no path

        formatted as:
            [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    # generate the graph
    graph = {}
    for edge in edges:
        s = edge['start']
        e = edge['end']
        if s in graph:
            graph[s].append(e)
        else:
            graph[s] = [e]
    # build up a queue for BFS
    path_total = []
    # append initial node to the queue
#    path_total.append([{'start':start}])
    path_total.append([start])
    # build up a set for recording if the node has been visited
    visited = set()
    # record the curent index
    current_i = 0
    while current_i < len(path_total):
#        print(path_total, visited)
        path = path_total[current_i] 
#        current_pos = path[-1]['end'] if len(path[-1]) > 1 else path[-1]['start']
        current_pos = path[-1]
        if current_pos not in visited and current_pos in graph:
            visited.add(current_pos)
            edges_from_current = graph[current_pos]
            for source in edges_from_current:
                if source in visited:
                    continue
                else:
                    shortest = path.copy()
#                    shortest.append({'start':current_pos, 'end':source})
                    shortest.append(source)
#                    path.append(source)
                    # if reach the target node, return the path
                    if source == end:
#                        print(shortest)
                         result = convert(shortest)
#                        return shortest[1:]
                         return result
                    path_total.append(shortest)
        current_i += 1
        
    return None
    
# a helper function used to determine the relation between two vectors
def direction(v1, v2):
    cross = v1[0]*v2[1] - v1[1]*v2[0]
    if cross == 0:
        dot = v1[0]*v2[0] + v1[1]*v2[1]
        if dot < 0:
            return 'U turn'
        else:
            return 'straight'
    elif cross < 0:
        return 'left'
    else:
        return 'right'


def shortest_path_no_lefts(edges, start, end):
    """
    Finds a shortest path without any left turns that goes
        from start to end using the provided edges. 
        (reversing turns are also not allowed)

    Args:
        edges: a list of dictionaries, where each dictionary has two items. 
            These items have keys `"start"` and `"end"` and values that are 
            tuples (two integers), to specify grid locations.
        start: a tuple representing our initial location.
        end: a tuple representing the target location.

    Returns:
        A list containing the edges taken in the resulting path if one exists, 
            None if there is no path

        formatted as:
            [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    # build up the graph; the key is an edge, the value is a list of edges connecting to it
    graph = {}
    current_start_nodes = {}
    current_end_nodes = {}
    for edge in edges:
        s = edge['start']
        e = edge['end']
        # v1 = (e[0] - s[0], e[1] - s[1])
        if s in current_start_nodes:
            current_start_nodes[s].add((s, e))
        else:
            current_start_nodes[s] = set([(s, e)])
        if e in current_end_nodes:
            current_end_nodes[e].add((s, e))
        else:
            current_end_nodes[e] = set([(s, e)])
            
        if (s, e) not in graph:
            graph[(s, e)] = []
        if e in current_start_nodes:
            for s1, e1 in current_start_nodes[e]:
                graph[(s, e)].append((s1, e1))
        if s in current_end_nodes:
            for s0, e0 in current_end_nodes[s]:
                graph[(s0, e0)].append((s, e))
#    print(len(graph))
    
    # find the edges connecting to starting point
    start_trans = []
    for edge in graph:
        if edge[0] == start:
            start_trans.append(edge)
#    print(start_trans)
    
    # explore the graph from each edge conntecting to the starting node
    for i in start_trans:
#        print('xxxxxxxxxxxxxx')
#        print(i)
        path_total = []
        path_total.append([i])
        current_i = 0
        visited = set()
        while current_i < len(path_total):
            path = path_total[current_i]
            current_trans = path[-1]
            # obtain the vector representing the current edge
            v_current = (current_trans[1][0] - current_trans[0][0], current_trans[1][1] - current_trans[0][1])
            # if the current edge is not visited
            if current_trans not in visited and current_trans in graph:
                visited.add(current_trans)
                trans_from_current = graph[current_trans]
                # for each neighboring edges of current edge
                for edge in trans_from_current:
                    if edge in visited:
                        continue
                    # if the edge is not visited, obtain the vector representing this edge
                    v_edge = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
                    # determine if the direction is valid
                    d = direction(v_current, v_edge)
                    if d == 'left' or d == 'U turn':
                        continue
                    shortest = path.copy()
                    shortest.append(edge)
                    if edge[1] == end:
#                            print('yyyyyyyyyyyes')
                        return [{'start':e[0],'end':e[1]} for e in shortest]
                    path_total.append(shortest) 
            current_i += 1
            
    return None
   

def shortest_path_k_lefts(edges, start, end, k):
    """
    Finds a shortest path with no more than k left turns that 
        goes from start to end using the provided edges.
        (reversing turns are also not allowed)

    Args:
        edges: a list of dictionaries, where each dictionary has two items. 
            These items have keys `"start"` and `"end"` and values that are 
            tuples (two integers), to specify grid locations.
        start: a tuple representing our initial location.
        end: a tuple representing the target location.
        k: the max number of allowed left turns.

    Returns:
        A list containing the edges taken in the resulting path if one exists, 
            None if there is no path

        formatted as:
            [{"start":(x1,y1), "end":(x2,y2)}, {"start":(x2,y2), "end":(x3,y3)}]
    """
    # build up the graph; the key is an edge, the value is a list of edges connecting to it
    graph = {}
    current_start_nodes = {}
    current_end_nodes = {}
    for edge in edges:
        s = edge['start']
        e = edge['end']
        # v1 = (e[0] - s[0], e[1] - s[1])
        if s in current_start_nodes:
            current_start_nodes[s].add((s, e))
        else:
            current_start_nodes[s] = set([(s, e)])
        if e in current_end_nodes:
            current_end_nodes[e].add((s, e))
        else:
            current_end_nodes[e] = set([(s, e)])
            
        if (s, e) not in graph:
            graph[(s, e)] = []
        if e in current_start_nodes:
            for s1, e1 in current_start_nodes[e]:
                graph[(s, e)].append((s1, e1))
        if s in current_end_nodes:
            for s0, e0 in current_end_nodes[s]:
                graph[(s0, e0)].append((s, e))
#    print(len(graph))
    
    start_trans = []
    for edge in graph:
        if edge[0] == start:
            start_trans.append((edge, k))
#    print(start_trans)
    
    # initialize the shortest path and its length
    current_shortest = None
    current_len = float('inf')
    for start_edge in start_trans:
#        print('xxxxxxxxxxxxxx')
#        print(i)
        path_total = [[start_edge]]
        current_i = 0
        visited = {}
        while current_i < len(path_total):
            path = path_total[current_i]
            current_trans, current_k = path[-1]
#            print('current')
#            print(current_trans)
            v_current = (current_trans[1][0] - current_trans[0][0], current_trans[1][1] - current_trans[0][1])
            # if the edge is not visited, condition is true
            if current_trans not in visited:
                cond = True
            # if the edge is visited but reaching it with less left turns, contidion is true
            elif visited[current_trans] < current_k:
                cond = True
            else:
                cond = False
            
            # if condition is true
            if cond and current_trans in graph:
                visited[current_trans] = current_k
                # visited_set.add(path[-1])
                trans_from_current = graph[current_trans]
                for edge in trans_from_current:
                    # record how many remaining left turns 
                    new_k = current_k
#                    print('edge')
#                    print(edge)
#                    print('x' + 1)
                    # if edge in visited:
                    #     continue
                    v_edge = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
                    d = direction(v_current, v_edge)
                    if d == 'U turn':
                        continue
                    
                    # if the direction is left, see if there is remaining left turns, if yes, turn left
                    if d == 'left':
                        if current_k < 1:
                            continue
                        else:
                            new_k -= 1
                    shortest = path.copy()
                    shortest.append((edge, new_k))
                    if edge[1] == end:
#                        print('yyyyyyyyyyyes')
                        # print([{'start':e[0][0],'end':e[0][1]} for e in shortest])
                        if len(shortest) < current_len:
                            current_len = len(shortest)
                            current_shortest = shortest
                        # return [{'start':e[0][0],'end':e[0][1]} for e in shortest]
                    path_total.append(shortest) 
            current_i += 1
            
    if current_shortest != None:
        return [{'start':e[0][0],'end':e[0][1]} for e in current_shortest] 
    else:
        return


if __name__ == "__main__":
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used for testing.
    pass


