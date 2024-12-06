import random
from common.node import Node

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