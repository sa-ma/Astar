from queue import Queue
from common.grid import read_grid
from common.visualization import visualize_grid
from common.get_neighbors import get_neighbors
from common.performance import track_performance
import statistics

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
            return path, nodes_expanded

        for neighbor, _ in get_neighbors(grid, current_node):
            if neighbor.state not in visited and neighbor.is_walkable:
                neighbor.parent = current_node
                visited.add(neighbor.state)
                queue.put(neighbor)

    return [], nodes_expanded

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
            return path, nodes_expanded

        for neighbor, _ in get_neighbors(grid, current_node):
            if neighbor.is_walkable and neighbor.parent is None:
                if current_node.parent is not None and neighbor == current_node.parent:
                    continue
                neighbor.parent = current_node
                queue.put(neighbor)

    return [], nodes_expanded

def reconstruct_path(goal_node):
    path = []
    current = goal_node
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]

def simulate_bfs(name, bfs_func, start_node, goal_node, grid, n_sim_iterations=100):
    results = []

    for _ in range(n_sim_iterations):
        _, metrics = bfs_func(start_node, goal_node, grid)
        results.append(metrics)

    averages = {
        "execution_time": statistics.mean(r["execution_time"] for r in results),
        "peak_memory": statistics.mean(r["peak_memory"] for r in results),
        "current_memory": statistics.mean(r["current_memory"] for r in results),
        "temporary_memory": statistics.mean(r["temporary_memory"] for r in results),
    }

    print(f"######### {name.upper()} AVERAGES AFTER {n_sim_iterations} ITERATIONS #########")
    print(f"Average Execution Time: {averages['execution_time']:.4f} seconds")
    print(f"Average Peak Memory: {averages['peak_memory']:.2f} KB")
    print(f"Average Current Memory: {averages['current_memory']:.2f} KB")
    print(f"Average Temporary Memory: {averages['temporary_memory']:.2f} KB")
    
    return averages

def simulate_bfs_tree(start_node, goal_node, grid, n_sim_iterations=100):
    return simulate_bfs("Tree", bfs_tree, start_node, goal_node, grid, n_sim_iterations)

def simulate_bfs_graph(start_node, goal_node, grid, n_sim_iterations=100):
    return simulate_bfs("Graph", bfs_graph, start_node, goal_node, grid, n_sim_iterations)

def main():
    cost_file_path = "common/node_costs_50x50.xlsx"
    maze_file_path = "common/online_maze.xlsx"
    start_node, goal_node, grid, _ = read_grid(maze_file_path, cost_file_path)

    algorithm = input("Select BFS version (tree/graph): ").strip().lower()

    if algorithm == "tree":
        (path, nodes_expanded), metric = bfs_tree(start_node, goal_node, grid)
        algorithm_name = "BFS Tree Search"
        
        print("\n\n######### TREE SIMULATION RESULTS #########")
        simulate_bfs_tree(start_node, goal_node, grid, n_sim_iterations=100)
        
    elif algorithm == "graph":
        (path, nodes_expanded), metric = bfs_graph(start_node, goal_node, grid)
        algorithm_name = "BFS Graph Search"
        
        print("\n\n######### GRAPH SIMULATION RESULTS #########")
        simulate_bfs_graph(start_node, goal_node, grid, n_sim_iterations=100)
        print(f"Nodes Expanded: {nodes_expanded}")
    else:
        print("Invalid choice! Exiting.")
        return

    visualize_grid(start_node, goal_node, grid, path, algorithm=algorithm_name)

if __name__ == "__main__":
    main()