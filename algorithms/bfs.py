from queue import Queue
from common.grid import read_grid
from common.visualization import visualize_grid
from common.get_neighbors import get_neighbors
from common.performance import track_performance

@track_performance
def bfs_graph(start, goal, grid):
    nodes_expanded = 0

    queue = Queue()
    queue.put(start)
    visited = set()
    visited.add(start.state)

    while not queue.empty():
        current_node = queue.get()
        nodes_expanded += 1

        if current_node.state == goal.state:
            path = reconstruct_path(current_node)
            total_cost = calculate_total_path_cost(path)
            return path, nodes_expanded, total_cost

        for neighbor, move_cost in get_neighbors(grid, current_node):
            if neighbor.state not in visited and neighbor.is_walkable:
                neighbor.parent = current_node
                neighbor.move_cost = move_cost
                visited.add(neighbor.state)
                queue.put(neighbor)

    return [], nodes_expanded, 0

@track_performance
def bfs_tree(start, goal, grid):
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
            path = reconstruct_path(current_node)
            total_cost = calculate_total_path_cost(path)
            return path, nodes_expanded, total_cost

        for neighbor, move_cost in get_neighbors(grid, current_node):
            if neighbor.is_walkable and neighbor.parent is None:
                if current_node.parent is not None and neighbor == current_node.parent:
                    continue
                neighbor.parent = current_node
                neighbor.move_cost = move_cost
                queue.put(neighbor)

    return [], nodes_expanded, 0

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
    cost_file_path = "common/grids/node_costs_50x50.xlsx"
    maze_file_path = "common/grids/mirror_maze_50x50.xlsx"
    start_node, goal_node, grid, _ = read_grid(maze_file_path, cost_file_path)

    algorithm = input("Select BFS version (tree/graph): ").strip().lower()

    if algorithm == "tree":
        results = bfs_tree(start_node, goal_node, grid)
        algorithm_name = "BFS Tree Search"
        
    elif algorithm == "graph":
        results = bfs_graph(start_node, goal_node, grid)
        algorithm_name = "BFS Graph Search"

    else:
        print("Invalid choice! Exiting.")
        return

    path = results[0][0]
    visualize_grid(start_node, goal_node, grid, path , algorithm=algorithm_name)

if __name__ == "__main__":
    main()