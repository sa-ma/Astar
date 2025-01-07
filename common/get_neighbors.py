def get_neighbors(grid, node):
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