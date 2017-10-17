def run(root, display, object):
    open = []
    closed = []
    open.append([root])
    nodesExplored = 0
    nodesExpanded = 0
    while open:
        path = object.getLowest_fScore(open)
        node = path[-1]
        if display:
            object.display(node, 10)
        successors = object.get_successors(node)
        nodesExpanded += 1
        for successor in successors:
            if object.isGoal(successor):
                path.append(successor)
                print ("FOUND GOAL STATE")
                return path, nodesExplored, nodesExpanded
            successor.gScore = object.get_gScore(node)
            successor.hScore = object.get_hScore(successor)
            successor.fScore = successor.gScore + successor.hScore
            if successor.state not in open:
                skipSuccessor = False
                for alternative in closed:
                    if successor.state == alternative.state:
                        if successor.fScore < alternative.fScore:
                            nodesExplored += 1
                            closed.append(successor)
                            new_path = list(path)
                            new_path.append(successor)
                            open.append(new_path)
                            break
                        print ("skip successor")
                        skipSuccessor = True
                if not skipSuccessor:
                    nodesExplored += 1
                    closed.append(successor)
                    new_path = list(path)
                    new_path.append(successor)
                    open.append(new_path)
