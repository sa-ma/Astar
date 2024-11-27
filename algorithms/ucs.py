import heapq
from common.grid import create_grid, generate_obstacles
from common.visualization import visualize_grid
from common.node import Node

def get_neighbours_4d(grid, node, is_varied_cost):
    
    # Costs for moving!
    # Right = 1
    # Left = 2
    # Up = 3
    # Down = 4
    directions = [(0, 1, 1), (0, -1, 2), (1, 0, 3), (-1, 0, 4)]
    rows = len(grid)
    columns = len(grid[0])
    neighbours = []
    
    for dx, dy, dc in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < columns:
            neighbour_node = grid[nx][ny]
            if neighbour_node.is_walkable:
                if is_varied_cost:
                    neighbours.append((neighbour_node, dc))
                else:
                    neighbours.append((neighbour_node, 1))
                
    return neighbours

def reconstruct_path(node):
    path = []
    current_node = node
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    path.reverse()
    return path

def ucs_pathfind_graph_traversal(start_node, goal_node, grid, is_varied_cost):
    open_set = []
    closed_set = {}
    start_node.cost = 0
    heapq.heappush(open_set, (0, start_node))
    
    while open_set:
        current_cost, parent_node = heapq.heappop(open_set)
        
        if parent_node.state == goal_node.state:
            return reconstruct_path(parent_node)
        
        closed_set[parent_node.state] = parent_node
        
        for neighbour, move_cost in get_neighbours_4d(grid, parent_node, is_varied_cost):
            new_cost = parent_node.cost + move_cost
            if neighbour.state not in closed_set:
                # This if statement with 'in_open_set' ensures that the neighbour nodes already in the open_set will have an updated node if a shorter/lower cost path is found.
                # Values inside open_set is a tuple. (cost, Node)
                # node[1] returns the node.
                in_open_set = any(neighbour.state == node[1].state for node in open_set)
                if(not in_open_set or new_cost < neighbour.cost):
                    neighbour.cost = new_cost
                    neighbour.parent = parent_node
                    heapq.heappush(open_set, (neighbour.cost, neighbour))
    
    return None

# Tree traversals don't have loop checks! Make sure grid given is a tree.
def ucs_pathfind_tree_traversal(start_node, goal_node, grid, is_varied_cost):
    open_set = []
    start_node.cost = 0
    heapq.heappush(open_set, (0, start_node))
    
    while open_set:
        current_cost, parent_node = heapq.heappop(open_set)
        
        if parent_node.state == goal_node.state:
            return reconstruct_path(parent_node)
        
        for neighbour, move_cost in get_neighbours_4d(grid, parent_node, is_varied_cost):
            new_cost = parent_node.cost + move_cost
            
            in_open_set = any(neighbour == node[1] for node in open_set)
            if(not in_open_set or new_cost < neighbour.cost):
                neighbour.cost = new_cost
                neighbour.parent = parent_node
                heapq.heappush(open_set, (neighbour.cost, neighbour))

def main():
    
    grid_x = 9
    grid_y = 9
    grid = create_grid(grid_x, grid_y)
    generate_obstacles(grid, [(0, 7), (1, 7), (3, 2), (2, 2), (4, 3), (6, 6), (6, 5)])
    
    start_node = grid[8][0]
    goal_node = grid[3][6]
    is_varied_move_cost = False
    path = ucs_pathfind_graph_traversal(start_node, goal_node, grid, is_varied_move_cost)
    path_cost = path[-1].cost
    
    if path:
        print("Path found:", path)
        visualize_grid(start_node, goal_node, grid, path, path_cost)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()