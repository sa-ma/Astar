import heapq
from common.grid import read_grid
from common.visualization import visualize_grid
from common.node import Node
from common.get_neighbors import get_neighbors
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
    tracemalloc.start()
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
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return reconstruct_path(parent_node), nodes_expanded, execution_time, peak - current
        
        closed_set[parent_node.state] = parent_node
        
        for neighbor, move_cost in get_neighbors(grid, parent_node):
            new_cost = parent_node.cost + neighbor.cost + move_cost
            if neighbor.state not in closed_set and (neighbor.state not in best_cost or new_cost < best_cost[neighbor.state]):
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                best_cost[neighbor.state] = new_cost
                heapq.heappush(open_set, (neighbor.cost, neighbor))
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return [], nodes_expanded, time.perf_counter() - start_time, peak - current

def ucs_tree_pathfind(start_node, goal_node, grid):
    tracemalloc.start()
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
            tracemalloc.stop()
            return reconstruct_path(parent_node), nodes_expanded, execution_time, peak - current
        
        for neighbor, move_cost in get_neighbors(grid, parent_node):
            new_cost = parent_node.cost + neighbor.cost + move_cost
            if neighbor.state not in best_cost or new_cost < best_cost[neighbor.state]:
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                best_cost[neighbor.state] = new_cost
                heapq.heappush(open_set, (neighbor.cost, neighbor))
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return [], nodes_expanded, time.perf_counter() - start_time, peak - current

def main():    
    #generate_obstacles(grid, obstacle_count = 5)
    maze_file_path = "common/grids/mirror_maze_50x50_2.xlsx"
    cost_file_path = "common/grids/node_costs_50x50.xlsx"
    
    # Ask the user which UCS version to run
    algorithm = input("Select UCS version (tree/graph): ").strip().lower()
    
    if algorithm not in ["tree", "graph"]:
        print("Invalid choice! Exiting.")
        return

    runs = 1
    total_path_length = 0
    total_nodes_expanded = 0
    total_execution_time = 0
    total_path_cost = 0
    total_memory_usage = 0

    for _ in range(runs):
        start_node, goal_node, grid, grid_shape = read_grid(maze_file_path, cost_file_path)
        if algorithm == "tree":
            path, nodes_expanded, execution_time, memory_usage = ucs_tree_pathfind(start_node, goal_node, grid)
        elif algorithm == "graph":
            path, nodes_expanded, execution_time, memory_usage = ucs_graph_pathfind(start_node, goal_node, grid)

        total_path_length += len(path)
        total_nodes_expanded += nodes_expanded
        total_execution_time += execution_time
        total_memory_usage += memory_usage
        total_path_cost += path[-1].cost if path else None

    avg_path_length = total_path_length / runs
    avg_nodes_expanded = total_nodes_expanded / runs
    avg_execution_time = total_execution_time / runs
    avg_path_cost = total_path_cost / runs
    avg_memory_usage = total_memory_usage / runs

    print(f"Average Path Length: {avg_path_length}")
    print(f"Average Path Cost: {avg_path_cost}")
    print(f"Average Nodes Expanded: {avg_nodes_expanded}")
    print(f"Average Execution Time: {avg_execution_time * 1000:.3f} milliseconds")
    print(f"Average Memory Usage: {avg_memory_usage / 1024:.2f} KB")
    
    visualize_grid(start_node, goal_node, grid, path, algorithm)

if __name__ == "__main__":
    main()