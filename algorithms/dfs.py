from queue import LifoQueue
import time
from common.grid import create_grid, generate_obstacles
from common.visualization import visualize_grid
from common.node import Node

def dfs(start: Node, goal: Node, grid: list[list[Node]]) -> tuple[list[Node], int, float]:
    """
    Depth-First Search implementation with performance metrics.
    """
    # Initialize performance metrics
    start_time = time.time()
    nodes_expanded = 0

    # DFS initialization
    stack = LifoQueue()
    stack.put(start)
    visited: set[tuple[int, int]] = set()
    visited.add(start.state)

    while not stack.empty():
        current_node = stack.get()
        nodes_expanded += 1  # Increment nodes expanded

        # Goal check
        if current_node.state == goal.state:
            execution_time = time.time() - start_time
            path = reconstruct_path(current_node)
            return path, nodes_expanded, execution_time

        # Explore neighbors
        for neighbor in get_neighbors(current_node, grid):
            if neighbor.state not in visited:
                visited.add(neighbor.state)
                neighbor.parent = current_node
                stack.put(neighbor)

    # No path found
    execution_time = time.time() - start_time
    return [], nodes_expanded, execution_time

def reconstruct_path(goal_node):
    """
    Reconstructs the path from the goal node back to the start node.
    """
    path = []
    current = goal_node
    while current:
        path.append(current)
        current = current.parent
    path.reverse()
    return path

def get_neighbors(node: Node, grid: list[list[Node]]) -> list[Node]:
    """
    Retrieves valid neighboring nodes.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dx, dy in directions:
        new_x, new_y = node.x + dx, node.y + dy
        if 0 <= new_x < rows and 0 <= new_y < cols:  # Boundary check
            neighbor = grid[new_x][new_y]
            if neighbor.is_walkable:
                neighbors.append(neighbor)

    return neighbors

def main():
    rows, columns = 100, 100
    grid = create_grid(rows, columns)
    generate_obstacles(grid, obstacle_count=20)

    start_node = grid[0][0]
    goal_node = grid[rows - 1][columns - 1]

    # Ensure start and goal are walkable
    start_node.is_walkable = True
    goal_node.is_walkable = True    

    # Run DFS
    path, nodes_expanded, execution_time = dfs(start_node, goal_node, grid)

    # Display performance metrics
    print(f"DFS Path Length: {len(path)}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Execution Time: {execution_time:.4f} seconds")

    # Visualize the result
    visualize_grid(start_node, goal_node, grid, path, algorithm="DFS")

if __name__ == "__main__":
    main()
