import math

class Node():
    def __init__(self, type: str, depth: int = 0, price: float = 0.0, parent_action = None) -> None:
        self.type = type
        self.depth = depth
        self.price = price
        self.parent_action = parent_action
        self.children = dict()

    def __repr__(self):
        return f"{self.type}"

def next_price(current, quantity, alpha, beta):
    if quantity > 0:
        price_impact = math.sqrt(2 * quantity / alpha)
    elif quantity < 0:
        price_impact = -math.sqrt(-2 * quantity / beta)
    else:
        price_impact = 0
    return current + price_impact * 2 / 3

def populate_tree(node, deltas, quantities, time_horizon):
    if time_horizon <= 0:
        return
    
    if node.type == "taker":
        # Time for the taker to move
        for quantity in quantities:
            alpha, beta = node.parent_action
            price = next_price(node.price, quantity, alpha, beta)
            node.children[quantity] = Node("maker", node.depth + 1, price, quantity)

    elif node.type == "maker":
        # Time for the maker to move
        for (alpha, beta) in deltas:
            node.children[(alpha, beta)] = Node("taker", node.depth + 1, node.price, (alpha, beta))
        
        # The round ends when the taker moves
        time_horizon -= 1

    for child in node.children.values():
        populate_tree(child, deltas, quantities, time_horizon)

def print_tree(root):
    queue = [(None, root)]
    while len(queue) > 0:
        action, node = queue.pop()
        queue.extend(node.children.items())

        if action is None: print(node)
        else: print("---" * node.depth + f" action {action} => {node} [{node.price:.2f}$]")

def main():
    deltas = [(0.1, 0.1), (0.1, 0.2), (0.2, 0.2)]
    quantities = range(-1, 2)
    time_horizon = 2

    root = Node("maker", price=10)
    populate_tree(root, deltas, quantities, time_horizon)

    print_tree(root)


if __name__ == "__main__":
    main()