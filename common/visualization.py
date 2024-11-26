import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def visualize_grid(start_node, goal_node, grid, path):
    rows = len(grid)
    columns = len(grid[0])
    
    cmap = ListedColormap(["black", "white", "green", "blue", "red"])
    
    visual_grid = [[0 for _ in range(columns)] for _ in range(rows)]
    
    for x in range(rows):
        for y in range(columns):
            if not grid[x][y].is_walkable:
                visual_grid[x][y] = 0
            else:
                visual_grid[x][y] = 1
    
    for node in path:
        visual_grid[node.x][node.y] = 3

    visual_grid[start_node.x][start_node.y] = 2
    visual_grid[goal_node.x][goal_node.y] = 4

    plt.figure(figsize=(9, 9))
    plt.imshow(visual_grid, cmap=cmap, origin='lower')
    plt.xticks(range(columns))
    plt.yticks(range(rows))
    plt.grid(which="both", color="black", linestyle="-", linewidth=0.5)
    plt.xlim(-0.5, columns - 0.5)
    plt.ylim(-0.5, rows - 0.5)
    plt.title("Pathfinding Visualization")
    plt.show()