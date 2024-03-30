from drop import check_can_piece_split, split, check_can_move, move
from collections import deque, defaultdict

def bidirectional_search(initial_state, goal_state):
    queue_source = deque([(initial_state, [], defaultdict(list))])
    queue_target = deque([(goal_state, [], defaultdict(list))])
    visited_source = set()
    visited_target = set()

    while queue_source and queue_target:

        for _ in range(len(queue_source)):
            state, path, photon_paths = queue_source.popleft()
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
