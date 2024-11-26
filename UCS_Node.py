class UCS_Node:
    def __init__(self, x, y, isWalkable, cost = 1):
        self.x = x
        self.y = y
        self.state = (self.x, self.y)
        self.isWalkable = isWalkable
        self.cost = cost
        self.parent = None
        
    def __repr__(self):
        return f"Node({self.x}, {self.y}, cost = {self.cost})"
    
    # A less-than function made so that it will work with heapq.
    def __lt__(self, other):
        return self.cost < other.cost