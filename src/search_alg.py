from drop import check_win, move, nodes
import drop
from collections import deque, defaultdict
import queue

'''
def dfs(state, goal, depth_limit):
    if depth_limit == 0:
        return None  # Limite de profundidade atingido sem encontrar uma solução
    
    if check_win(state):  # Verifica se o estado atual é uma solução
        return []  # Retorna uma lista vazia para indicar que encontramos uma solução
    
    for i in range(19):  # Itera sobre todas as posições do tabuleiro
        new_state = move(state[:], i)  # Realiza um movimento em uma posição específica
        if new_state != state:  # Verifica se o movimento foi válido
            if state[1][1] != 'none':
                # Verifica se a posição para onde está se movendo é uma posição válida em nodes
                if state[1][1] in nodes and i in nodes[state[1][1]][0]:
                    result = dfs(new_state, goal, depth_limit - 1)  # Chama recursivamente a função dfs com o novo estado
                    if result is not None:  # Se encontrar uma solução, retorna a sequência de movimentos
                        return [i] + result
            else:
                result = dfs(new_state, goal, depth_limit - 1)  # Chama recursivamente a função dfs com o novo estado
                if result is not None:  # Se encontrar uma solução, retorna a sequência de movimentos
                    return [i] + result
    
    return None  # Se nenhum movimento válido for encontrado, retorna None
'''

'''
def solve_game(start_state, goal_state, max_depth):
    return dfs(start_state, goal_state, max_depth)
'''

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
        selected = (99, 99)

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
        False))