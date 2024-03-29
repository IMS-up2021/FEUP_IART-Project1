from drop import check_can_piece_split, split, check_can_move, move
from collections import deque

def bidirectional_search(initial_state, goal_state):
    queue_source = deque([(initial_state, [])])
    queue_target = deque([(goal_state, [])])
    visited_source = set()
    visited_target = set()

    while queue_source and queue_target:

        for _ in range(len(queue_source)):
            state, path = queue_source.popleft()
            if state in visited_target:
                return path + list(reversed(visited_target[state]))
            visited_source.add(state)
            for next_state, move in get_successors(state):
                if next_state not in visited_source:
                    queue_source.append((next_state, path + [move]))

        for _ in range(len(queue_target)):
            state, path = queue_target.popleft()
            if state in visited_source:
                return path + list(reversed(visited_source[state]))
            visited_target.add(state)
            for next_state, move in get_successors(state, reverse=True):
                if next_state not in visited_target:
                    queue_target.append((next_state, path + [move]))

    return []

def get_successors(state, reverse=False):
    board, selected, moves_left, _ = state
    successors = []

    # Split pieces
    for pos, piece in enumerate(board):
        if piece and piece[0:3] == 'ph_' and not check_can_piece_split(state, pos):
            new_state = split(list(state), pos)
            if new_state != state:
                successors.append((tuple(new_state), f"Split {piece} at {pos}"))

    # Move pieces
    if selected[0] != -1:
        for pos, piece in enumerate(board):
            if check_can_move(state, pos):
                new_state = move(list(state), pos)
                if new_state != state:
                    successors.append((tuple(new_state), f"Move {board[selected[1]]} to {pos}"))

    if reverse:
        successors = [(s, m) for s, m in successors][::-1]

    return successors
