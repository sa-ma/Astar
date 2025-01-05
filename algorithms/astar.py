import heapq
import time
from common.visualization import visualize_grid
from common.grid import read_grid
from common.performance import track_performance

def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y) # Manhattan distance


def get_neighbors(grid, node, grid_shape):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rows, columns = grid_shape
    neighbors = []
    
    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < columns:
            neighbor_node = grid[nx][ny]
            if neighbor_node.is_walkable:
                neighbors.append(neighbor_node)
    return neighbors

def reconstruct_path(node):
    path = []
    current_node = node
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    path.reverse()
    return path

@track_performance
def astar_tree_pathfind(start_node, goal_node, grid, grid_shape):
    nodes_expanded = 0

    # Priority queue for open set
    open_set = []
    # Set to track expanded nodes
    closed_set = set()

    # Initialize starting node
    start_node.cost = 0
    heapq.heappush(open_set, (0, start_node))

    while open_set:
        nodes_expanded += 1
        _, parent_node = heapq.heappop(open_set)

        # Skip if already expanded
        if parent_node.state in closed_set:
            continue

        # Mark the node as expanded
        closed_set.add(parent_node.state)

        # Check if the goal is reached
        if parent_node.state == goal_node.state:
            return reconstruct_path(parent_node), nodes_expanded

        # Explore neighbors
        for neighbor in get_neighbors(grid, parent_node, grid_shape):
            new_cost = parent_node.cost + neighbor.cost + heuristic(neighbor, goal_node)

            # Update neighbor only if it is not yet expanded
            if neighbor.state not in closed_set:
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                heapq.heappush(open_set, (new_cost, neighbor))

    # If no path found
    return [], nodes_expanded

@track_performance
def astar_graph_pathfind(start_node, goal_node, grid, grid_shape):
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
            return reconstruct_path(parent_node), nodes_expanded
        
        closed_set[parent_node.state] = parent_node
        
        for neighbor in get_neighbors(grid, parent_node, grid_shape):
            new_cost = parent_node.cost + neighbor.cost + heuristic(neighbor, goal_node)
            if neighbor.state not in closed_set and (neighbor.state not in best_cost or new_cost < best_cost[neighbor.state]):
                neighbor.cost = new_cost
                neighbor.parent = parent_node
                best_cost[neighbor.state] = new_cost
                heapq.heappush(open_set, (new_cost, neighbor))
                
    return [], nodes_expanded


def main():    
    #generate_obstacles(grid, obstacle_count = 5)
    maze_file_path = "common/online_maze.xlsx"
    cost_file_path = "common/node_costs_50x50.xlsx"
    start_node, goal_node, grid, grid_shape = read_grid(maze_file_path, cost_file_path)
    
    # Ask the user which UCS version to run
    algorithm = input("Select A* version (tree/graph): ").strip().lower()

    if algorithm == "tree":
        path, nodes_expanded = astar_tree_pathfind(start_node, goal_node, grid, grid_shape)
        algorithm_name = "A* Tree Search"
    elif algorithm == "graph":
        path, nodes_expanded = astar_graph_pathfind(start_node, goal_node, grid, grid_shape)
        algorithm_name = "A* Graph Search"
    else:
        print("Invalid choice! Exiting.")
        return
    
    visualize_grid(start_node, goal_node, grid, path, algorithm = algorithm_name)

if __name__ == "__main__":
    main()