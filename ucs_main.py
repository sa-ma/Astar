from UCS_Node import UCS_Node

def CreateGrid(rows, columns):
    # Creates a 2D Array while assuming every cost to enter the node is 1.
    grid = []
    for x in range(rows):
        row = []
        for y in range(columns):
            # Every Node is Walkable during Grid Creation.
            row.append(UCS_Node(x, y, True))
        grid.append(row)
    return grid

def GenerateObstaclesTest1(grid):
    grid[0][7].isWalkable = False
    grid[1][7].isWalkable = False
    grid[3][2].isWalkable = False
    grid[2][2].isWalkable = False
    grid[4][3].isWalkable = False
    grid[6][6].isWalkable = False
    grid[6][5].isWalkable = False

def ShowGridText(grid):
    # The Reverse Function ensures that (0, 0) starts at the bottom left.
    # Row is the Y-Axis
    # Column is the X-Axis
    for row in (grid):
        print(" ".join("#" if not node.isWalkable else "." for node in row))
        
def GetNeighbors4n(grid, node):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rows = len(grid)
    columns = len(grid[0])
    neighbours = []
    
    for dx, dy in directions:
        nx = node.x + dx
        ny = node.y + dy
        # Bound Checking
        if(0 <= nx < rows and 0 <= ny < columns):
            neighbour_node = grid[nx][ny]
            if(neighbour_node.isWalkable):
                neighbours.append(neighbour_node)
                
    return neighbours

def main():
    grid = CreateGrid(8, 8)
    GenerateObstaclesTest1(grid)
    ShowGridText(grid)
    
    # Implement UCS Algorithm!!
    # Idea:
    # Randomly generate obstacles and node costs then save them into text or excel, so that results can be replicated.
    

if __name__ == "__main__":
    main()