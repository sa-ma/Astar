import heapq
from common.grid import create_grid, generate_obstacles
from common.visualization import visualize_grid
from common.node import Node

def get_neighbors(grid, node):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rows = len(grid)
    columns = len(grid[0])
    neighbors = []
    
    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < columns:
            neighbor_node = grid[nx][ny]
            if neighbor_node.is_walkable:
                neighbors.append(neighbor_node)
                
    return neighbors

def reconstruct_path(node):
    path = []
    current_node = node
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    path.reverse()
    return path

def ucs_pathfind_graph_traversal(start_node, goal_node, grid):
    open_set = []
    closed_set = {}
    start_node.cost = 0 
    heapq.heappush(open_set, (0, start_node))
    
    while open_set:
        current_cost, parent_node = heapq.heappop(open_set)
        
        if parent_node.state == goal_node.state:
            return reconstruct_path(parent_node)
        
        closed_set[parent_node.state] = parent_node
        
        for neighbor in get_neighbors(grid, parent_node):
            new_cost = parent_node.cost + neighbor.cost
            if neighbor.state not in closed_set:
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                heapq.heappush(open_set, (neighbor.cost, neighbor))
    
    return None

def ucs_pathfind_tree_traversal(start_node, goal_node, grid):
    open_set = []
    start_node.cost = 0
    heapq.heappush(open_set, (0, start_node))
    
    while open_set:
        current_cost, parent_node = heapq.heappop(open_set)
        
        if parent_node.state == goal_node.state:
            return reconstruct_path(parent_node)
        
        for neighbour in get_neighbors(grid, parent_node):
            new_cost = parent_node.cost + neighbour.cost
            
            in_open_set = any(neighbour == node[1] for node in open_set)
            if(not in_open_set or new_cost < neighbour.cost):
                neighbour.cost = new_cost
                neighbour.parent = parent_node
                heapq.heappush(open_set, (neighbour.cost, neighbour))

def main():
    grid = create_grid(9, 9)
    generate_obstacles(grid, [(0, 7), (1, 7), (3, 2), (2, 2), (4, 3), (6, 6), (6, 5)])
    
    start_node = grid[0][0]
    goal_node = grid[5][5]
    path = ucs_pathfind_graph_traversal(start_node, goal_node, grid)
    
    if path:
        print("Path found:", path)
        visualize_grid(start_node, goal_node, grid, path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()