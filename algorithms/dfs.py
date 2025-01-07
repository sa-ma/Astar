import os
import time
import tracemalloc
from common.grid import read_grid
from common.visualization import visualize_grid
from common.get_neighbors import get_neighbors  # Updated import statement


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
            return path, nodes_expanded, end_time - start_time, peak - current

        # Explore neighbors
        for neighbor, _ in get_neighbors(grid, current_node):  # Unpack neighbor and move_cost
            if neighbor.state not in visited and neighbor.is_walkable:
                neighbor.parent = current_node
                visited.add(neighbor.state)
                stack.append(neighbor)

    # If no path is found
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return [], nodes_expanded, end_time - start_time, peak - current


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
            return path, nodes_expanded, end_time - start_time, peak - current

        # Explore neighbors
        for neighbor, _ in get_neighbors(grid, current_node):
            if neighbor.is_walkable and neighbor.parent is None:
                if current_node.parent is not None and neighbor == current_node.parent:
                    continue
                neighbor.parent = current_node
                stack.append(neighbor)

    # If no path is found
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return [], nodes_expanded, end_time - start_time, peak - current


def reconstruct_path(goal_node):
    path = []
    current = goal_node
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]


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

    # Run DFS
    path, nodes_expanded, exec_time, memory_usage = dfs(start_node, goal_node, grid)

    # Display performance metrics
    print(f"Execution Time: {exec_time:.6f} seconds")
    #print(f"Path: {path}")
    print(f"Path Length: {len(path)}")
    #print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Memory usage: {memory_usage / 1024:.2f} KB")

    # Visualize the result
    visualize_grid(start_node, goal_node, grid, path, algorithm=search_type)


if __name__ == "__main__":
    main()
