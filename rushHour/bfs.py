def run(root, display, object):
    open = []
    closed = []
    open.append([root])
    nodesExplored = 0
    while open:
        path = open.pop(0)
        node = path[-1]
        if display:
            object.display(node, 10)
        if object.isGoal(node):
            print ("FOUND GOAL STATE")
            return path, nodesExplored
        successors = object.get_successors(node)
        for successor in successors:
            if successor.state not in closed:
                nodesExplored += 1
                closed.append(successor.state)
                new_path = list(path)
                new_path.append(successor)
                open.append(new_path)
