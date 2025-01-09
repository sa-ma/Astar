import os
import time
import tracemalloc
from common.grid import read_grid
from common.visualization import visualize_grid
from common.get_neighbors import get_neighbors


def dfs_graph(start, goal, grid):
    """
    Depth-First (Graph) Search implementation.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    nodes_expanded = 0
    # Initialize stack and visited set
    stack = [start]
    visited = {start.state}

    while stack:
        current_node = stack.pop()
        nodes_expanded += 1

        # Check if goal is found
        if current_node.state == goal.state:
            path = reconstruct_path(current_node)
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_cost = calculate_total_path_cost(path)
            return path, nodes_expanded, end_time - start_time, peak - current, total_cost

        # Explore neighbors
        for neighbor, move_cost in get_neighbors(grid, current_node):
            if neighbor.state not in visited and neighbor.is_walkable:
                neighbor.parent = current_node
                neighbor.move_cost = move_cost
                visited.add(neighbor.state)
                stack.append(neighbor)

    # If no path is found
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return [], nodes_expanded, end_time - start_time, peak - current, 0


def dfs_tree(start, goal, grid):
    """
    Depth-First (Tree) Search implementation.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    nodes_expanded = 0
    # Reset parents
    for row in grid:
        for node in row:
            node.parent = None

    # Initialize stack
    stack = [start]

    while stack:
        current_node = stack.pop()
        nodes_expanded += 1

        # Check if goal is found
        if current_node.state == goal.state:
            path = reconstruct_path(current_node)
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_cost = calculate_total_path_cost(path)
            return path, nodes_expanded, end_time - start_time, peak - current, total_cost

        # Explore neighbors
        for neighbor, move_cost in get_neighbors(grid, current_node):
            if neighbor.is_walkable and neighbor.parent is None:
                if current_node.parent is not None and neighbor == current_node.parent:
                    continue
                neighbor.parent = current_node
                neighbor.move_cost = move_cost
                stack.append(neighbor)

    # If no path is found
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return [], nodes_expanded, end_time - start_time, peak - current, 0 


def reconstruct_path(goal_node):
    path = []
    current = goal_node
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]

def calculate_total_path_cost(path):
    total_cost = 0
    for i in range(1, len(path)):
        node = path[i]
        parent = path[i - 1]
        # Cost of entering the node
        total_cost += node.cost
        # Movement cost from the parent to this node
        total_cost += getattr(node, "move_cost", 0)  
    return total_cost

def main():
    # Grid selection
    excel_files = [f for f in os.listdir("common") if f.endswith(".xlsx")]

    if not excel_files:
        print("No .xlsx files found in the 'common' folder.")
    else:
        # Print them with indexes
        for i, f in enumerate(excel_files):
            print(f"{i}: {f}")

        # Ask user to pick grid
        choice = input("Enter the number of the file you want to open: ")

        # Convert to integer
        try:
            choice_index = int(choice)
            chosen_file = excel_files[choice_index]
            chosen_path = os.path.join("common", chosen_file)

            print(f"You chose: {chosen_path}")
        except (ValueError, IndexError):
            print("Invalid choice!")

    cost_file_path = "common/node_costs_50x50.xlsx"
    start_node, goal_node, grid, grid_shape = read_grid(chosen_path, cost_file_path)

    # Ask the user which algorithm to run
    algorithm = input("Select DFS algorithm (tree/graph): ").strip().lower()

    if algorithm == "tree":
        print("Running tree search.")
        dfs = dfs_tree
        search_type = "DFS Tree Search"
    elif algorithm == "graph":
        print("Running graph search.")
        dfs = dfs_graph
        search_type = "DFS Graph Search"
    else:
        print("Running graph search as default.")
        dfs = dfs_graph
        search_type = "DFS Graph Search"

    # Test over 100 runs
    total_time = 0
    total_memory = 0
    total_nodes_expanded = 0
    total_path_length = 0
    num_runs = 1000

    # for _ in range(num_runs):
    path, nodes_expanded, exec_time, memory_usage, path_cost = dfs(start_node, goal_node, grid)
    total_time += exec_time
    total_memory += memory_usage
    total_nodes_expanded += nodes_expanded
    total_path_length += len(path)
    print(f"Start Node is: {start_node}")
    print(f"Goal Node is: {goal_node}")

    # Calculate averages
    # avg_time = total_time / num_runs
    # avg_memory = total_memory / num_runs
    # avg_nodes_expanded = total_nodes_expanded / num_runs
    # avg_path_length = total_path_length / num_runs

    # Display results
    # print(f"Results over {num_runs} runs:")
    # print(f"Average Execution Time: {avg_time:.6f} seconds")
    # print(f"Average Memory Usage: {avg_memory / 1024:.2f} KB")
    # print(f"Average Nodes Expanded: {avg_nodes_expanded:.2f}")
    # print(f"Average Path Length: {avg_path_length:.2f}")
    
    #print(f"Results over {num_runs} runs:")
    print(f" Execution Time: {exec_time:.6f} seconds")
    print(f" Memory Usage: {memory_usage / 1024:.2f} KB")
    print(f" Nodes Expanded: {nodes_expanded:.2f}")
    print(f" Path Length: {len(path):.2f}")    
    print(f"Path Cost: {path_cost}")
    

    # Visualize the result
    visualize_grid(start_node, goal_node, grid, path, algorithm=search_type)


if __name__ == "__main__":
    main()
