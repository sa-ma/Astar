import time
from common.grid import read_grid
from common.visualization import visualize_grid

def dfs_graph(start, goal, grid):
    """
    Depth-First (Graph) Search implementation.
    """
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
            execution_time = time.perf_counter() - start_time
            path = reconstruct_path(current_node)
            return path, nodes_expanded, execution_time

        # Explore neighbors
        for neighbor in get_neighbors(current_node, grid):
            if neighbor.state not in visited and neighbor.is_walkable:
                neighbor.parent = current_node
                visited.add(neighbor.state)
                stack.append(neighbor)

    # If no path is found
    execution_time = time.perf_counter() - start_time
    return [], nodes_expanded, execution_time


def dfs_tree(start, goal, grid):
    """
    Depth-First (Tree) Search implementation.
    """
    start_time = time.perf_counter()
    nodes_expanded = 0

    # Reset parents (Tree Search assumption: no repeated states if you don't revisit the parent)
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
            execution_time = time.perf_counter() - start_time
            path = reconstruct_path(current_node)
            return path, nodes_expanded, execution_time

        # Explore neighbors
        for neighbor in get_neighbors(current_node, grid):
            # If neighbor has no parent, it hasn't been visited yet in Tree Search
            if neighbor.is_walkable and neighbor.parent is None:
                # Optionally skip going directly back to the parent
                if current_node.parent is not None and neighbor == current_node.parent:
                    continue
                neighbor.parent = current_node
                stack.append(neighbor)

    # If no path is found
    execution_time = time.perf_counter() - start_time
    return [], nodes_expanded, execution_time


def reconstruct_path(goal_node):
    path = []
    current = goal_node
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]


def get_neighbors(node, grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dx, dy in directions:
        new_x, new_y = node.x + dx, node.y + dy
        if 0 <= new_x < rows and 0 <= new_y < cols:
            neighbors.append(grid[new_x][new_y])

    return neighbors


def main():
    start_node, goal_node, grid, grid_shape = read_grid("common/maze_50x50_4directions.xlsx")

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
    path, nodes_expanded, execution_time = dfs(start_node, goal_node, grid)

    # Display performance metrics
    print(f"Path: {path}")
    print(f"Path Length: {len(path)}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Execution Time: {execution_time:.4f} seconds")

    # Visualize the result
    visualize_grid(start_node, goal_node, grid, path, algorithm=search_type)


if __name__ == "__main__":
    main()
