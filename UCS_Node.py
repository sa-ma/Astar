class UCS_Node:
    def __init__(self, x, y, isWalkable, cost = 1):
        self.x = x
        self.y = y
        self.isWalkable = isWalkable
        self.cost = cost
        self.parent = None
        
    def __repr__(self):
        return f"Node({self.x}, {self.y}, isWalkable = {self.isWalkable}, cost = {self.cost})"
    