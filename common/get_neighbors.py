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
