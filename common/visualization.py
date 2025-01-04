import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def visualize_grid(start_node, goal_node, grid, path, algorithm):
    """
    Visualizes the grid with obstacles, path, and start/goal nodes.
    Dynamically adjusts the legend based on the algorithm name.
    """
    rows = len(grid)
    columns = len(grid[0])

    # Colors:              obstacles, free,    path,   start, goal
    cmap = ListedColormap(["black", "white", "green", "blue", "red"])  
    visual_grid = [[0 for _ in range(columns)] for _ in range(rows)]

    # Fill the visual grid
    for x in range(rows):
        for y in range(columns):
            if not grid[x][y].is_walkable:
                visual_grid[x][y] = 0  # Obstacles
            else:
                visual_grid[x][y] = 1  # Free space

    for node in path:
        visual_grid[node.x][node.y] = 3  # Path

    visual_grid[start_node.x][start_node.y] = 2  # Start
    visual_grid[goal_node.x][goal_node.y] = 4  # Goal

    # Create the plot
    plt.figure(figsize=(10, 10))
    plt.imshow(visual_grid, cmap=cmap, origin='lower')

    # Move the grid lines by 0.5 to align exactly with pathing
    plt.xlim(-0.5, columns - 0.5)
    plt.ylim(-0.5, rows - 0.5)
    
    # Set up grid lines at each integer boundary
    plt.gca().set_xticks(np.arange(-0.5, columns, 1))
    plt.gca().set_yticks(np.arange(-0.5, rows, 1))
    
    # Turn on the grid, and remove axis labels
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])
    plt.grid(which="both", color="black", linestyle="-", linewidth=0.5)

    # Add legend
    colors = ['black', 'white', 'blue', 'green', 'red']
    labels = [
        'Obstacle',
        'Free Space',
        f'{algorithm} Path',
        'Start',
        'Goal'
    ]
    handles = [plt.Line2D([0], [0], color=color, marker='o', linestyle='', markersize=10) for color in colors]
    plt.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))

    plt.title(f"Grid Visualization with {algorithm}")
    plt.show()
