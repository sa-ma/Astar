from queue import Queue
import time
from common.grid import read_grid
from common.visualization import visualize_grid
from common.get_neighbors import get_neighbors


def bfs_graph(start, goal, grid):
    start_time = time.time()
    nodes_expanded = 0

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
        neighbors = get_neighbors(grid, current_node)
        for neighbor, _ in neighbors:
            if neighbor.state not in visited and neighbor.is_walkable:
                neighbor.parent = current_node
                visited.add(neighbor.state)
                queue.put(neighbor)

    execution_time = time.time() - start_time
    return [], nodes_expanded, execution_time


def bfs_tree(start, goal, grid):

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

        for neighbor, _ in get_neighbors(grid, current_node):
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

def main():
    cost_file_path = "common/node_costs_50x50.xlsx"
    maze_file_path = "common/online_maze.xlsx"
    start_node, goal_node, grid, _ = read_grid(maze_file_path, cost_file_path)

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

    # Performance metrics
    print(f"Path Length: {len(path)}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Execution Time: {execution_time * 1000:.3f} milliseconds")

    visualize_grid(start_node, goal_node, grid, path, algorithm=algo_name)


if __name__ == "__main__":
    main()
