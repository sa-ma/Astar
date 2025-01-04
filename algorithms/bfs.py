from queue import Queue
import time
from common.grid import read_grid
from common.visualization import visualize_grid


def bfs_graph(start, goal, grid):
    """
    Breadth-First Search implementation with Graph Search.
    """

    start_time = time.time()
    nodes_expanded = 0

    # BFS initialization
    queue = Queue()
    queue.put(start)
    visited = set()
    visited.add(start.state)

    while not queue.empty():
        current_node = queue.get()
        nodes_expanded += 1

        if current_node.state == goal.state:
            execution_time = time.time() - start_time
            path = reconstruct_path(current_node)
            return path, nodes_expanded, execution_time

        # Explore neighbors
        neighbors = get_neighbors(current_node, grid)
        for neighbor in neighbors:
            if neighbor.state not in visited and neighbor.is_walkable:
                neighbor.parent = current_node
                visited.add(neighbor.state)
                queue.put(neighbor)

    # If no path is found
    execution_time = time.time() - start_time
    return [], nodes_expanded, execution_time


def bfs_tree(start, goal, grid):
    """
        Breadth-First Search implementation with Tree Search.
    """

    start_time = time.time()
    nodes_expanded = 0

    for row in grid:
        for node in row:
            node.parent = None

    queue = Queue()
    start.parent = None
    queue.put(start)

    while not queue.empty():
        current_node = queue.get()
        nodes_expanded += 1

        if current_node.state == goal.state:
            execution_time = time.time() - start_time
            path = reconstruct_path(current_node)
            return path, nodes_expanded, execution_time

        for neighbor in get_neighbors(current_node, grid):
            if neighbor.is_walkable and neighbor.parent is None:
                if current_node.parent is not None and neighbor == current_node.parent:
                    continue
                neighbor.parent = current_node
                queue.put(neighbor)

    execution_time = time.time() - start_time
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
        if 0 <= new_x < rows and 0 <= new_y < cols:  # Boundary check
            neighbors.append(grid[new_x][new_y])
    return neighbors


def main():
    start_node, goal_node, grid, grid_shape = read_grid("common/maze_50x50_4directions.xlsx")

    # Ask the user which BFS version to run
    algorithm = input("Select BFS version (tree/graph): ").strip().lower()

    if algorithm == "tree":
        path, nodes_expanded, execution_time = bfs_tree(start_node, goal_node, grid)
        algo_name = "BFS Tree Search"
    elif algorithm == "graph":
        path, nodes_expanded, execution_time = bfs_graph(start_node, goal_node, grid)
        algo_name = "BFS Graph Search"
    else:
        print("Invalid choice! Exiting.")
        return

    # Display performance metrics
    print(f"Path: {path}")
    print(f"Path Length: {len(path)}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Execution Time: {execution_time:.4f} seconds")

    # Visualize the result
    visualize_grid(start_node, goal_node, grid, path, algorithm=algo_name)


if __name__ == "__main__":
    main()
