from drop import check_can_piece_split, split, check_can_move, move
import drop
from collections import deque, defaultdict
import queue

def bidirectional_search(initial_state, goal_state):
    queue_source = deque([(initial_state, [], defaultdict(list))])
    queue_target = deque([(goal_state, [], defaultdict(list))])
    visited_source = set()
    visited_target = set()

    while queue_source and queue_target:

        for _ in range(len(queue_source)):
            state, path, photon_paths = queue_source.popleft()
            print(visited_target)
            if state in visited_target:
                target_photon_paths = visited_target[state][2]
                merged_photon_paths = merge_photon_paths(photon_paths, target_photon_paths)
                return path + list(reversed(visited_target[state][1])), merged_photon_paths
            visited_source.add(state)
            for next_state, move, new_photon_paths in get_successors(state, photon_paths):
                if next_state not in visited_source:
                    queue_source.append((next_state, path + [move], new_photon_paths))

        for _ in range(len(queue_target)):
            state, path, photon_paths = queue_target.popleft()
            if state in visited_source:
                source_photon_paths = visited_source[state][2]
                merged_photon_paths = merge_photon_paths(photon_paths, source_photon_paths)
                return path + list(reversed(visited_source[state][1])), merged_photon_paths
            visited_target.add(state)
            for next_state, move, new_photon_paths in get_successors(state, photon_paths, reverse=True):
                if next_state not in visited_target:
                    queue_target.append((next_state, path + [move], new_photon_paths))

    return [], {}

def get_successors(state, photon_paths, reverse=False):
    board, selected, moves_left, _ = state
    successors = []

    # Split pieces
    for pos, piece in enumerate(board):
        if piece and piece[0:3] == 'ph_' and not check_can_piece_split(state, pos):
            new_state = split(list(state), pos)
            if new_state != state:
                new_photon_paths = update_photon_paths(photon_paths, piece, pos, new_state[0][pos])
                successors.append((tuple(new_state), f"Split {piece} at {pos}", new_photon_paths))

    # Move pieces
    if selected[0] != -1:
        for pos, piece in enumerate(board):
            if check_can_move(state, pos):
                new_state = move(list(state), pos)
                if new_state != state:
                    new_photon_paths = update_photon_paths(photon_paths, board[selected[1]], selected[1], pos)
                    successors.append((tuple(new_state), f"Move {board[selected[1]]} to {pos}", new_photon_paths))

    if reverse:
        successors = [(s, m, p) for s, m, p in successors][::-1]

    return successors

def update_photon_paths(photon_paths, photon, old_pos, new_pos):
    new_photon_paths = photon_paths.copy()
    new_photon_paths[photon].append(new_pos)
    if old_pos != -1:
        new_photon_paths[photon].append(old_pos)
    return new_photon_paths

def merge_photon_paths(source_paths, target_paths):
    merged_paths = defaultdict(list)
    for photon, path in source_paths.items():
        merged_paths[photon] = path
    for photon, path in target_paths.items():
        merged_paths[photon] = path + merged_paths[photon]
    return merged_paths

def init_informed(initial_state, goal_state, algo):
    if initial_state == []:
        return {} 
    
    to_move_pos = []
    goal_pos_dist = {}
    moves = {}
        
    for i in range(len(initial_state)):
        if initial_state[i][0] in drop.piece and initial_state[i][0] != 0:
            to_move_pos.append(i)
        if goal_state[i][0] in drop.piece and goal_state[i][0] != 0:
            goal_pos_dist[i] = drop.dist_to_goal(i)
            
    for pos in to_move_pos:
        selected = (99,99) 
        
        for goal in goal_pos_dist:
            check = not goal in drop.nodes[pos][0]
            if goal_pos_dist[goal][pos] + check <= selected[0]:
                selected = (goal_pos_dist[goal][pos] + check, goal)
            
        if algo:
            moves[pos] = greedy([], pos, selected[1], initial_state, goal_state, goal_pos_dist[selected[1]])
            goal_pos_dist.pop(selected[1])
        else:
            moves[pos] = a_star(pos, selected[1], initial_state, goal_pos_dist[selected[1]])
            goal_pos_dist.pop(selected[1])
        
    return moves

def greedy(prev, fr, to, initial_state, goal_state, distances):
    if fr == to:
        return [to]
    
    if fr == 99:
        return []
    
    ret = []
    
    mini = (99,99)
    
    for place in drop.nodes[fr][0]:
        to_check = initial_state[place][0]
        if to_check != 'blocked' and to_check != goal_state[to][0] and not place in prev and distances[place] < mini[0]:
            mini = (distances[place], place)
    
    prev.append(fr)
    ret.append(fr)
    
    return ret + greedy(prev, mini[1], to, initial_state, goal_state, distances)

def a_star(fr, to, initial_state, distances):
    frontier = queue.PriorityQueue()
    reached = [fr]
    dist_walked = 0
    print(f'from {fr} -> {to}')
   
    frontier.put((distances[fr], fr, fr, [])) #(dist, selected, father_node) 
   
    while frontier:
        selected = frontier.get()
        dist_walked = drop.dist(selected[1], selected[2])
       
        if selected[1] == to:
            return selected[3] + [to]
       
        for node in drop.nodes[selected[1]][0]:
            if initial_state[node][0] != 'blocked' and initial_state[node][0] != initial_state[fr][0] and not node in reached: #and distances[node] < distances[selected[1]]:
                frontier.put((distances[node] + dist_walked, node, selected[1], selected[3] + [selected[1]]))
                reached.append(node)

    return -1

if __name__ == "__main__":
    print(init_informed(
        drop.filter_photon(drop.LEVELS[1][0], 'ph_blue'),
        drop.filter_photon(drop.LEVELS[1][3], 'ph_blue'),
        False
    ))
