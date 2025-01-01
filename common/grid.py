import random
import pandas as pd
from common.node import Node

def read_grid(file_path):
    df = pd.read_excel(file_path, header = None)
    
    grid = []
    rows, columns = df.shape
    start_node = 0
    goal_node = 0
    
    for x in range(rows):
        row = []
        for y in range(columns):
            node_value = df.iloc[x, y]
            
            # Node is walkable if excel node value is 0, 2, or 3.
            is_walkable = node_value == 0 or node_value == 2 or node_value == 3
            node = Node(x, y, is_walkable, cost = 1)
            
            # Start Node
            if node_value == 2:
                node.cost = 0
                start_node = node
            # Goal Node
            elif node_value == 3:
                node.cost = 1
                goal_node = node
            # Obstacle Node
            elif node_value == 1:
                node.cost = float('inf')
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