
from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        # you write this part
        self.state = state
        self.parent = parent

    def get_state(self): # Helper fx for self state
        return self.state
    
    def get_parent(self): # Helper fx for parent
        return self.parent


# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions

def backchain(node):
    path = [] # Init path
    curr_node = node
    while (curr_node):
        curr_state = curr_node.get_state() # State of curr node
        path.append(curr_state) # add state to path
        curr_node = curr_node.get_parent() # move to parent node
    
    solution = [] # solution path from start to goal state
    i = len(path) - 1
    while (i >= 0):
        solution.append(path[i])
        i -= 1 # aka i = i-1
    return solution # this is basically a reversed version of path


def bfs_search(search_problem):
    start_node = SearchNode(search_problem.start_state) # start node
    frontier = deque() # deque for FIFO
    frontier.append(start_node)

    visited = set() # store visited states
    visited.add(search_problem.start_state)

    solution = SearchSolution(search_problem, "BFS") # Init SearchSolution obj

    while frontier:
        curr_node = frontier.popleft() # get first added state, FIFO
        curr_state = curr_node.get_state()
        
        if search_problem.goal_test(curr_state): # check if we reached goal
            solution.path = backchain(curr_node) # success
            solution.nodes_visited = len(visited)
            return solution
        
        children = search_problem.get_successors(curr_state) # get successors
        for child in children:
            if child not in visited:
                visited.add(child)
                child_node = SearchNode(child, curr_node) # create successor node to add to frontier
                frontier.append(child_node)
    
    solution.nodes_visited = len(visited)
    return solution # failure

# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

def path_checking(check_node, curr_node):
    # check if the nodes are the same
    if check_node.get_state() == curr_node.get_state():
        return True

    # if we reached the end of the path, i.e. got to the start
    # then there are no other duplicate nodes
    elif curr_node.get_parent() is None:
        return False
    
    # recurse until we either reach the start_state or until we find duplicate check_node
    return path_checking(check_node, curr_node.get_parent())

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # you write this part
    curr_state = node.get_state() # Get curr state
    solution.path.append(curr_state) # Add to path
    solution.nodes_visited += 1

    # base case 1: Hit the depth limit
    if len(solution.path) > depth_limit: # terminate dfs
        solution.path.pop() # remove last added state bc it exceeds depth limit
        return solution
    
    # base case 2: current node is goal
    if search_problem.goal_test(curr_state):
        return solution
    
    # get successors of node added to path
    children = search_problem.get_successors(curr_state)
    for child in children:
        child_node = SearchNode(child, node) 

        if not path_checking(child_node, node):
            # visit child node
            solution = dfs_search(search_problem, depth_limit, child_node, solution)

            # child led us to goal, return path so far
            if search_problem.goal_test(solution.path[-1]):
                return solution
            
    solution.path.pop() # failure
    return solution



def ids_search(search_problem, depth_limit=100):
    # you write this part
    curr_limit = 0
    node = SearchNode(search_problem.start_state, None)
    solution = SearchSolution(search_problem, "IDS")

    while curr_limit < depth_limit:
        solution = dfs_search(search_problem, curr_limit, node, solution)

        # if we received a valid solution, return it
        if len(solution.path) > 0 and search_problem.goal_test(solution.path[-1]):
            return solution
        curr_limit += 1

    # if no valid solution was found after depth_limit exceeded, return findings
    return solution
