from common.node import Node

# TODO:
# Create a grid that is made for tree traversal check. (No infinite loops)

def create_grid(rows, columns, default_cost=1):
    grid = []
    for x in range(rows):
        row = []
        for y in range(columns):
            row.append(Node(x, y, True, default_cost))
        grid.append(row)
    return grid

def generate_obstacles(grid, obstacles):
    for (x, y) in obstacles:
        grid[x][y].is_walkable = False