import heapq
from common.visualization import visualize_grid
from common.grid import read_grid
from common.performance import track_performance
from common.get_neighbors import get_neighbors
import statistics
import pandas as pd

def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y) # Manhattan distance

def reconstruct_path(node):
    path = []
    current_node = node
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    path.reverse()
    return path


@track_performance
def astar_tree_pathfind(start_node, goal_node, grid):
    nodes_expanded = 0

    open_set = []  # Priority queue for the open set
    closed_set = set()  # Set to track expanded nodes

    # Initialize the starting node
    start_node.cost = 0
    heapq.heappush(open_set, (0, start_node))

    while open_set:
        nodes_expanded += 1
        _, parent_node = heapq.heappop(open_set)

        # Skip if the node has already been expanded
        if (parent_node.x, parent_node.y) in closed_set:
            continue

        # Mark the node as expanded
        closed_set.add((parent_node.x, parent_node.y))

        # Check if the goal is reached
        if parent_node.x == goal_node.x and parent_node.y == goal_node.y:
            return reconstruct_path(parent_node), nodes_expanded

        # Explore neighbors
        for neighbor, move_cost in get_neighbors(grid, parent_node):
            if not neighbor.is_walkable:
                continue

            new_cost = parent_node.cost + move_cost

            # Update neighbor cost and re-add to open set if cost is lower
            if (neighbor.x, neighbor.y) not in closed_set or new_cost < neighbor.cost:
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                priority = new_cost + heuristic(neighbor, goal_node)
                heapq.heappush(open_set, (priority, neighbor))

    # If no path is found
    return [], nodes_expanded



@track_performance
def astar_graph_pathfind(start_node, goal_node, grid):
    nodes_expanded = 0

    open_set = []  # Priority queue for the open set
    closed_set = set()  # Set to track expanded nodes
    best_cost = {}  # Dictionary to track the best cost for each state

    # Initialize the starting node
    start_node.cost = 0
    heapq.heappush(open_set, (0, start_node))
    best_cost[start_node.state] = 0

    while open_set:
        nodes_expanded += 1
        _, parent_node = heapq.heappop(open_set)

        # Skip if the node has already been expanded
        if parent_node.state in closed_set:
            continue

        # Mark the node as expanded
        closed_set.add(parent_node.state)

        # Check if the goal is reached
        if parent_node.state == goal_node.state:
            return reconstruct_path(parent_node), nodes_expanded

        # Explore neighbors
        for neighbor, move_cost in get_neighbors(grid, parent_node):
            tentative_cost = parent_node.cost + move_cost + neighbor.cost

            # Check if the neighbor is not in the closed set or has a better cost
            if neighbor.state not in closed_set and (
                neighbor.state not in best_cost or tentative_cost < best_cost[neighbor.state]
            ):
                neighbor.cost = tentative_cost
                neighbor.parent = parent_node
                best_cost[neighbor.state] = tentative_cost
                priority = tentative_cost + heuristic(neighbor, goal_node)
                heapq.heappush(open_set, (priority, neighbor))

    # If no path is found
    return [], nodes_expanded




def simulate_astar(name, astar_func, start_node, goal_node, grid, n_sim_iterations=100):
    results = []

    for _ in range(n_sim_iterations):
        # Call the A* function and collect performance metrics
        _, metrics = astar_func(start_node, goal_node, grid)
        results.append(metrics)

    # Compute averages
    averages = {
        "execution_time": statistics.mean(r["execution_time"] for r in results),
        "peak_memory": statistics.mean(r["peak_memory"] for r in results),
        "current_memory": statistics.mean(r["current_memory"] for r in results),
        "temporary_memory": statistics.mean(r["temporary_memory"] for r in results),
    }

    # Print results
    print(f"######### {name.upper()} AVERAGES AFTER {n_sim_iterations} ITERATIONS #########")
    print(f"Average Execution Time: {averages['execution_time']:.4f} seconds")
    print(f"Average Peak Memory: {averages['peak_memory']:.2f} KB")
    print(f"Average Current Memory: {averages['current_memory']:.2f} KB")
    print(f"Average Temporary Memory: {averages['temporary_memory']:.2f} KB")
    
    return averages, pd.DataFrame(results)

def simulate_astar_tree(start_node, goal_node, grid, n_sim_iterations=100):
    """
    Simulates the A* algorithm on a tree representation.
    """
    return simulate_astar("Tree", astar_tree_pathfind, start_node, goal_node, grid, n_sim_iterations)

def simulate_astar_graph(start_node, goal_node, grid, n_sim_iterations=100):
    """
    Simulates the A* algorithm on a graph representation.
    """
    return simulate_astar("Graph", astar_graph_pathfind, start_node, goal_node, grid, n_sim_iterations)


def main(): 
    #generate_obstacles(grid, obstacle_count = 5)
    maze_file_path = "common/mirror_maze_50x50.xlsx"
    cost_file_path = "common/node_costs_50x50.xlsx"
    start_node, goal_node, grid, grid_shape = read_grid(maze_file_path, cost_file_path)


    # Ask the user which UCS version to run
    algorithm = input("Select A* version (tree/graph): ").strip().lower()

    if algorithm == "tree":
        (path, total_cost), metric = astar_tree_pathfind(start_node, goal_node, grid)
        algorithm_name = "A* Tree Search"

        #print("\n\n######### TREE SIMULATION RESULTS #########")
        #simulate_astar_tree(start_node, goal_node, grid, n_sim_iterations=100)
        
    elif algorithm == "graph":
        (path, nodes_expanded), metric = astar_graph_pathfind(start_node, goal_node, grid)
        algorithm_name = "A* Graph Search"
        
        # print("\n\n######### TREE SIMULATION RESULTS #########")
        # _, df = simulate_astar_tree(start_node, goal_node, grid, n_sim_iterations=100)
        # print(df.describe())
    else:
        print("Invalid choice! Exiting.")
        return
    
    visualize_grid(start_node, goal_node, grid, path, algorithm = algorithm_name)
    
    

if __name__ == "__main__":
    main()