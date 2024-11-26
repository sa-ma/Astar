from UCS_Node import UCS_Node
import heapq

def CreateGrid(rows, columns):
    # Creates a 2D Array while assuming every cost to enter the node is 1.
    grid = []
    for x in range(rows):
        row = []
        for y in range(columns):
            # Every Node is Walkable during Grid Creation.
            row.append(UCS_Node(x, y, True))
        grid.append(row)
    return grid

def GenerateObstaclesTest1(grid):
    grid[0][7].isWalkable = False
    grid[1][7].isWalkable = False
    grid[3][2].isWalkable = False
    grid[2][2].isWalkable = False
    grid[4][3].isWalkable = False
    grid[6][6].isWalkable = False
    grid[6][5].isWalkable = False
    #grid[0][0].isWalkable = False
    

def ShowGridText(grid):
    # The Reverse Function ensures that (0, 0) starts at the bottom left.
    # Row is the Y-Axis
    # Column is the X-Axis
    for row in reversed(grid):
        print(" ".join("#" if not node.isWalkable else "." for node in row))
        
def GetNeighbors4n(grid, node):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rows = len(grid)
    columns = len(grid[0])
    neighbours = []
    
    for dx, dy in directions:
        nx = node.x + dx
        ny = node.y + dy
        # Bound Checking
        if(0 <= nx < rows and 0 <= ny < columns):
            neighbour_node = grid[nx][ny]
            if(neighbour_node.isWalkable):
                neighbours.append(neighbour_node)
                
    return neighbours

def ReconstructPath(node):
    path = []
    current_node = node
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    
    # Reverse to get start to goal.
    path.reverse()
    return path

def UCSPathFind(start_node, goal_node, grid):
    open_set = []
    closed_set = {}
    # Adds Node into open set with priority value 0.
    # heapq automatically sorts the node with highest priority.
    # Starting node always have cost 0.
    start_node.cost = 0 
    heapq.heappush(open_set, (0, start_node))
    
    while open_set:
        current_cost, parent_node = heapq.heappop(open_set)
        
        if(parent_node.state == goal_node.state):
            return ReconstructPath(parent_node)
            #return parent_node
        
        closed_set[parent_node.state] = parent_node
        
        for neighbours in GetNeighbors4n(grid, parent_node):
            
            # Skip non-walkable neighbours.
            if not neighbours.isWalkable:
                continue
            
            new_cost = parent_node.cost + neighbours.cost
            
            is_in_open_set = False
            for node in open_set:
                # Each element in open_set is a tuple (cost, UCS_Node), node[1] accesses the Node class.
                if(neighbours.state == node[1].state):
                    is_in_open_set = True
                    break
            
            # If the neighbour is not in the closed set and not in the open set.
            if(neighbours.state not in closed_set and not is_in_open_set):
                neighbours.cost = new_cost
                neighbours.parent = parent_node
                heapq.heappush(open_set, (neighbours.cost, neighbours))
            
            # Neighbour is in closed set but not in open set
            elif(neighbours.state not in closed_set):
                for i, (cost, node) in enumerate(open_set):
                    # Check if there are cheaper costs to reach a discovered node in the open_set.
                    if(node.state == neighbours.state and new_cost < node.cost):
                        # Update the cost and the parent. (Replaces the old tuple).
                        open_set[i] = (new_cost, neighbours)
                        neighbours.cost = new_cost
                        # Update the parent of neighbour to the current parent_node to show that a new path was found using this parent_node.
                        neighbours.parent = parent_node
                        # Reorganize the open set.
                        heapq.heapify(open_set)
                        break
        
        # first tuple value popped is the priority value, second value is the node itself.
        # current_priority, current_node = heapq.heappop(open_set)
        # print(f"Exploring node {current_node} with priority {current_priority}")
    
    return None

def main():
    grid = CreateGrid(8, 8)
    GenerateObstaclesTest1(grid)
    ShowGridText(grid)
    
    start_node = grid[0][0]
    goal_node = grid[5][5]
    path = UCSPathFind(start_node, goal_node, grid)
    
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
    
    # Idea:
    # Randomly generate obstacles and node costs then save them into text or excel, so that results can be replicated.
    # RECHECK UCA CODE
    # Make 2 versions of UCS, One with and another without loop check.
    # Make Visuals.

if __name__ == "__main__":
    main()