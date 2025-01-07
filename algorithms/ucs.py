import heapq
from common.grid import read_grid
from common.visualization import visualize_grid
from common.node import Node
from common.get_neighbors import get_neighbors
from common.performance import track_performance
import time
import tracemalloc

def reconstruct_path(node):
    path = []
    current_node = node
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    path.reverse()
    return path

def ucs_graph_pathfind(start_node, goal_node, grid):
    start_time = time.perf_counter()
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
            execution_time = time.perf_counter() - start_time
            return reconstruct_path(parent_node), nodes_expanded, execution_time
        
        closed_set[parent_node.state] = parent_node
        
        for neighbor, move_cost in get_neighbors(grid, parent_node):
            new_cost = parent_node.cost + neighbor.cost + move_cost
            if neighbor.state not in closed_set and (neighbor.state not in best_cost or new_cost < best_cost[neighbor.state]):
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                best_cost[neighbor.state] = new_cost
                heapq.heappush(open_set, (neighbor.cost, neighbor))
    
    return [], nodes_expanded, time.perf_counter() - start_time

def ucs_tree_pathfind(start_node, goal_node, grid):
    start_time = time.perf_counter()
    nodes_expanded = 0
    
    open_set = []
    best_cost = {}
    
    start_node.cost = 0
    heapq.heappush(open_set, (0, start_node))
    best_cost[start_node.state] = 0
    
    while open_set:
        nodes_expanded += 1
        current_cost, parent_node = heapq.heappop(open_set)
        
        if parent_node.state == goal_node.state:
            execution_time = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            return reconstruct_path(parent_node), nodes_expanded, execution_time
        
        for neighbor, move_cost in get_neighbors(grid, parent_node):
            new_cost = parent_node.cost + neighbor.cost + move_cost
            if neighbor.state not in best_cost or new_cost < best_cost[neighbor.state]:
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                best_cost[neighbor.state] = new_cost
                heapq.heappush(open_set, (neighbor.cost, neighbor))
                
    return [], nodes_expanded, time.perf_counter() - start_time

def main():    
    #generate_obstacles(grid, obstacle_count = 5)
    maze_file_path = "common/mirror_maze_50x50_2.xlsx"
    cost_file_path = "common/node_costs_50x50.xlsx"
    #start_node, goal_node, grid, grid_shape = read_grid(maze_file_path, cost_file_path)
    
    algorithm = input("Select UCS version (tree/graph): ").strip().lower()
    
    if algorithm not in ["tree", "graph"]:
        print("Invalid choice! Exiting.")
        return

    runs = 1
    total_execution_time = 0

    for _ in range(runs):
        start_node, goal_node, grid, grid_shape = read_grid(maze_file_path, cost_file_path)
        if algorithm == "tree":
            path, nodes_expanded, execution_time = ucs_graph_pathfind(start_node, goal_node, grid)
        elif algorithm == "graph":
            path, nodes_expanded, execution_time = ucs_tree_pathfind(start_node, goal_node, grid)

        path_length = len(path)
        total_execution_time += execution_time

    avg_execution_time = total_execution_time / runs

    print(f"Path Length: {path_length}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Average Execution Time: {avg_execution_time * 1000:.3f} milliseconds")
        
    #visualize_grid(start_node, goal_node, grid, path, algorithm = algorithm_name)

if __name__ == "__main__":
    main()