from graph.util import Stack

def child_graph(ancestors):

    parents = dict()
    
    for parent, child in ancestors:
        if child not in parents:
            parents[child] = [parent]
        else:
            parents[child].append(parent)
    return parents


def depth_first_search(child, parents):
    
    stack = Stack()
    seen = set()

    max_path = []
    
    stack.push([child])

    while stack.size() > 0:
        cur_path = stack.pop()
        print(cur_path)
        child = cur_path[-1]

        if child not in seen:
            seen.add(child)
            if child not in parents:
                if len(cur_path) > len(max_path):
                    max_path = cur_path
            else:
                for parent in parents[child]:
                    new_path = cur_path.copy()
                    new_path = new_path.append(parent)
                    stack.push(new_path)

    if max_path == []:
        return -1
    return max_path

def earliest_ancestor(ancestors, starting_node):
    
    parents = child_graph(ancestors)
    max_path = depth_first_search(starting_node, parents)

    
