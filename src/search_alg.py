from drop import check_can_piece_split, split, check_can_move, move
import drop
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

def init_informed(initial_state, goal_state, algo):
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
            if goal_pos_dist[goal][pos] <= selected[0]:
                selected = (goal_pos_dist[goal][pos], goal)
            
        if algo:
            print(f'pos: {pos}')
            moves[pos] = greedy([], pos, selected[1], initial_state, goal_state, goal_pos_dist[selected[1]])
            goal_pos_dist.pop(selected[1])
            
        '''
        else:
            A*
        ''' 
        print('done')
        
    return moves

def greedy(prev, fr, to, initial_state, goal_state, distances):
    if fr == to:
        return [to]
    
    ret = []
    
    mini = (99,99)
    
    for place in drop.nodes[fr][0]:
        to_check = initial_state[place][0]
        if to_check != 'blocked'and to_check != goal_state[to][0] and not place in prev and distances[place] < mini[0]:
            mini = (distances[place], place)
    
    prev.append(fr)
    ret.append(fr)
    
    print(f'{mini[1]} -> {initial_state[mini[1]][0]}')
    
    return ret + greedy(prev, mini[1], to, initial_state, goal_state, distances)

if __name__ == "__main__":
    print(init_informed(
        [(0, 0), (0, 0), ('merge', 1), (0, 0), (0, 0), (0, 0), (0, 0), ('ph_green', 1), (0, 0), ('blocked', 99), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), ('blocked', 99), (0, 0), (0, 0)],
        [(0, 0), (0, 0), ('merge', 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), ('blocked', 99), (0, 0), ('ph_green', 1), (0, 0), (0, 0), (0, 0), (0, 0), ('blocked', 99), (0, 0), (0, 0)],
        True
    ))