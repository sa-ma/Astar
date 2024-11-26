class Node:
    def __init__(self, x, y, is_walkable, cost=1):
        self.x = x
        self.y = y
        self.state = (self.x, self.y)
        self.is_walkable = is_walkable
        self.cost = cost
        self.parent = None

    def __repr__(self):
        return f"Node({self.x}, {self.y}, cost={self.cost})"

    def __lt__(self, other):
        return self.cost < other.cost