import random
import pandas as pd
from common.node import Node

def read_grid(file_path, cost_file_path):
    df = pd.read_excel(file_path, header = None)
    df_cost = pd.read_excel(cost_file_path, header = None)
    
    grid = []
    rows, columns = df.shape
    start_node = 0
    goal_node = 0
    
    for x in range(rows):
        row = []
        for y in range(columns):
            node_value = df.iloc[x, y]
            node_cost = df_cost.iloc[x, y]
            
            # Node is walkable if excel node value is 0, 2, or 3.
            is_walkable = node_value == 0 or node_value == 2 or node_value == 3
            node = Node(x, y, is_walkable, cost = node_cost if is_walkable else float('inf'))
            
            # Start Node
            if node_value == 2:
                node.cost = 0
                start_node = node
                print(f"Start Node is at: ({x}, {y})")
            # Goal Node
            elif node_value == 3:
                node.cost = node_cost
                goal_node = node
                print(f"Goal Node is at: ({x}, {y})")
                
            row.append(node)
        grid.append(row)
    
    return start_node, goal_node, grid, df.shape

def create_grid(rows, columns, default_cost=1):
    """
    Creates a grid of nodes with specified dimensions and default cost.
    """
    return [[Node(x, y, True, default_cost) for y in range(columns)] for x in range(rows)]

def generate_obstacles(grid, obstacle_count):
    """
    Places obstacles randomly in the grid.
    """
    rows = len(grid)
    cols = len(grid[0])
    all_positions = [(x, y) for x in range(rows) for y in range(cols)]
    obstacles = random.sample(all_positions, obstacle_count)

    for x, y in obstacles:
        grid[x][y].is_walkable = False
    
def generate_fixed_obstacles(grid, obstacles):
    for x, y in obstacles:
        grid[x][y].is_walkable = False
        
def get_neighbors(node, grid):
    movement_costs = {
        (0, 1): 1,  # Right
        (0, -1): 2, # Left
        (1, 0): 3,  # Down
        (-1, 0): 4  # Up
    }
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []

    for dx, dy in directions:
        new_x, new_y = node.x + dx, node.y + dy
        if 0 <= new_x < rows and 0 <= new_y < cols:
            move_cost = movement_costs[(dx, dy)]
            neighbors.append((grid[new_x][new_y], move_cost))
    return neighbors
