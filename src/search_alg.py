from collections import deque

class Node:
    def __init__(self, val, neighbors=[]):
        self.val = val
        self.neighbors = neighbors
        self.visited_from_source = False
        self.visited_from_target = False
        self.parent_from_source = None
        self.parent_from_target = None

def bidirectional_search(source, target):
    if source == target:
        return [source.val]

    queue_source = deque([source])
    queue_target = deque([target])
    source.visited_from_source = True
    target.visited_from_target = True

    while queue_source and queue_target:
        
        for _ in range(len(queue_source)):
            node = queue_source.popleft()
            if node.visited_from_target:
                return extract_path(node)
            for neighbor in node.neighbors:
                if not neighbor.visited_from_source:
                    neighbor.parent_from_source = node
                    neighbor.visited_from_source = True
                    queue_source.append(neighbor)

        for _ in range(len(queue_target)):
            node = queue_target.popleft()
            if node.visited_from_source:
                return extract_path(node)
            for neighbor in node.neighbors:
                if not neighbor.visited_from_target:
                    neighbor.parent_from_target = node
                    neighbor.visited_from_target = True
                    queue_target.append(neighbor)

    return [] 

def extract_path(node):
    path = []
    while node:
        path.append(node.val)
        node = node.parent_from_source
    path.reverse()
    
    node = node.parent_from_target
    while node:
        path.append(node.val)
        node = node.parent_from_target
    
    return path
