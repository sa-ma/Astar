import heapq
from common.grid import create_grid, generate_obstacles, generate_fixed_obstacles
from common.visualization import visualize_grid
from common.node import Node
import time

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

def ucs_pathfind(start_node, goal_node, grid):
    start_time = time.time()
    nodes_expanded = 0
    
    open_set = []
    closed_set = {}
    best_cost = {}
    
    start_node.cost = 0 
    heapq.heappush(open_set, (0, start_node))
    best_cost[start_node.state] = 0
    
    while open_set:
        nodes_expanded += 1
        current_cost, parent_node = heapq.heappop(open_set)
        
        if parent_node.state == goal_node.state:
            execution_time = time.time() - start_time
            return reconstruct_path(parent_node), nodes_expanded, execution_time
        
        closed_set[parent_node.state] = parent_node
        
        for neighbor in get_neighbors(grid, parent_node):
            new_cost = parent_node.cost + neighbor.cost
            if neighbor.state not in closed_set and (neighbor.state not in best_cost or new_cost < best_cost[neighbor.state]):
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                best_cost[neighbor.state] = new_cost
                heapq.heappush(open_set, (neighbor.cost, neighbor))
    
    return [], nodes_expanded, time.time() - start_time

def main():
    grid = create_grid(100, 100)
    generate_obstacles(grid, obstacle_count = 1000)
    # generate_fixed_obstacles(grid, [(0, 7), (1, 7), (3, 2), (2, 2), (4, 3), (6, 6), (6, 5)])
    
    start_node = grid[0][0]
    #goal_node = grid[5][5]
    goal_node = grid[99][99]
    path, nodes_expanded, execution_time = ucs_pathfind(start_node, goal_node, grid)
    
    print(f"UCS Path Length: {len(path)}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Execution Time: {execution_time:.6f} seconds")
    
    visualize_grid(start_node, goal_node, grid, path, algorithm="UCS")

if __name__ == "__main__":
    main()