from math import sqrt

#board, selected, nº remaining moves, goal
LEVELS = {
    1:[[
              0,0,
              'ph_red',
              'ph_red',0,
              'ph_red','ph_green',
              0,0,0,'ph_green',0,
              'ph_blue','ph_green',
              'ph_blue',0,
              'ph_blue',
              0,0
             ], [-1,'none'], 9,
             [
              0,0,
              0,
              0,'ph_yellow',
              0,0,
              0,'ph_magenta','ph_white',0,0,
              0,0,
              0,'ph_cyan',
              0,
              0,0
             ]],
    2:[
        [
              0,0,
              0,
              0,'ph_yellow',
              0,0,
              0,'ph_magenta','ph_white',0,0,
              0,0,
              0,'ph_cyan',
              0,
              0,0
             ], [-1,'none'], 15,
            [
              0,0,
              'ph_red',
              'ph_red',0,
              'ph_red','ph_green',
              0,0,0,'ph_green',0,
              'ph_blue','ph_green',
              'ph_blue',0,
              'ph_blue',
              0,0
             ]],
    3:[[
              0,0,
              'pi_magenta',
              0,0,
              0,0,
              'ph_white',0,'pi_cyan',0,0,
              0,0,
              0,0,
              'pi_yellow',
              0,0
             ], [-1,'none'], 19,
             [
              0,0,
              'pi_magenta',
              0,0,
              0,0,
              0,0,'pi_cyan',0,'ph_white',
              0,0,
              0,0,
              'pi_yellow',
              0,0
             ]],
    4:[
        [   
            0,0,
            0,
            0,0,
            0,0,
            0,0,'pi_white',0,0,
            0,0,
            'ph_green',0,
            'pi_white',
            'ph_blue',0
            ], [-1,'none'], 13,
            [
            0,0,
            0,
            0,0,
            0,0,
            0,0,'pi_white',0,0,
            0,0,
            0,'ph_green',
            'pi_white',
            0,'ph_blue'
            ]
    ],
    5:[
        [   
            0,0,
            0,
            0,0,
            0,0,
            'purple',0,0,0,'yellow',
            0,0,
            0,0,
            0,
            0,0
            ], 0, 6,
            [
            0,0,
            0,
            0,'red',
            0,0,
            0,0,'white',0,0,
            0,0,
            0,0,
            0,
            0,0
            ]
    ]
}

piece = {
            #photons
            'ph_red':[(127,0,0),True, {'ph_green':'ph_yellow', 'ph_blue':'ph_magenta', 'ph_cyan':'ph_white', 'pi_green':'pi_lime', 'pi_blue':'pi_purple', 'pi_cyan':'pi_blueS'}, 0],
            'ph_blue':[(0,0,127),True, {'ph_green':'ph_cyan', 'ph_red':'ph_magenta', 'ph_yellow':'ph_white', 'pi_red':'pi_violet', 'pi_green':'pi_mint', 'pi_yellow':'pi_beige'}, 0],
            'ph_green':[(0,127,0),True, {'ph_red':'ph_yellow', 'ph_blue':'ph_cyan', 'ph_magenta':'ph_white', 'pi_red':'pi_orange', 'pi_blue':'pi_mBlue', 'pi_magenta':'pi_pearl'}, 0],
            'ph_cyan':[(0,127,127),True, {'ph_red':'ph_white', 'pi_red':'pi_pink'},('ph_blue', 'ph_green',1)],
            'ph_yellow':[(127,127,0),True, {'ph_blue':'ph_white', 'pi_blue':'pi_lilac'},('ph_red', 'ph_green',1)],
            'ph_magenta':[(127,0,127),True, {'ph_green':'ph_white', 'pi_green':'pi_pistachio'},('ph_red', 'ph_blue',1)],
            'ph_white':[(240,240,240),True, {}, ('ph_red', 'ph_cyan',2)],
            
            #elemental pigments
            'pi_red':[(255,0,0),False,{},0],
            'pi_blue':[(0,0,255),False,{},0],
            'pi_green':[(0,255,0),False,{},0],
            'pi_cyan':[(0,255,255),False,{},0],
            'pi_yellow':[(255,255,0),False,{},0],
            'pi_magenta':[(255,0,255),False,{},0],
            'pi_white':[(255,255,255),False,{},0],
            
            #mix pigments
            'pi_orange':[(255,127,0),False,{},('ph_green', 'pi_red',0)],
            'pi_violet':[(255,0,127),False,{},('ph_blue', 'pi_red',0)],
            'pi_pink':[(255,127,127),False,{},('ph_cyan', 'pi_red',0)],
            'pi_lime':[(127,255,0),False,{},('ph_red', 'pi_green',0)],
            'pi_mint':[(0,255,127),False,{},('ph_blue', 'pi_green',0)],
            'pi_pistachio':[(127,255,127),False,{},('ph_violet', 'pi_green',0)],
            'pi_purple':[(127,0,255),False,{},('ph_red', 'pi_blue',0)],
            'pi_mBlue':[(0,127,255),False,{},('ph_green', 'pi_blue',0)],
            'pi_lilac':[(127,127,255),False,{},('ph_yellow', 'pi_blue',0)],
            'pi_blueS':[(127,255,255),False,{},('ph_red', 'pi_cyan',0)],
            'pi_pearl':[(255,127,255),False,{},('ph_green', 'pi_magenta',0)],
            'pi_beige':[(255,255,127),False,{},('ph_blue', 'pi_yellow',0)],
            
            #empty space
            0:[(105, 105, 105),False,{},0]
            
        } #{piece:[code, can be moved, {photon:mix}, [splits]]} to change splits -> (selects, leaves behind, cost)

nodes = {
        0:[[2,3,5],(2,1)], 1:[[2,4,6],(6,1)], 
        2:[[1,4,5],(4,2)], 
        3:[[0,2,5,9],(3,3)], 4:[[1,2,6,9],(5,3)], 
        5:[[0,3,7,8],(2,4)], 6:[[1,4,10,11],(6,4)], 
        7:[[5,8,12],(1,5)], 8:[[5,7,9,12],(2,5)], 9:[[3,4,8,10,14,15],(4,5)], 10:[[6,9,11,13],(6,5)], 11:[[6,10,13],(7,5)],
        12:[[7,8,14,17],(2,6)], 13:[[10,11,15,18],(6,6)],
        14:[[9,12,16,17],(3,7)], 15:[[9,13,16,18],(5,7)],
        16:[[14,15,17,18],(4,8)],
        17:[[12,14,16],(2,9)], 18:[[13,15,16],(6,9)]
        } #node1 -> node2, node2 -> node1

def check_can_piece_split(state, to_check):
    return piece[state[0][to_check]][3] == 0

def check_empty(state, to_check):
    return state[0][to_check] == 0

def check_can_merge(state, to): #can merge color
    return state[0][to] in piece[state[1][0]][2]

def check_can_move(state, to): #can move to space (empty and connected)
    return not(to in nodes[state[1][1]][1])

def check_win(state):
    return state[0] == state[3]

def split(state, pos):
    if check_can_piece_split(state, pos):
        return state
    
    state[1] = [piece[state[0][pos]][3][0], pos, state[2]]
    state[2] = state[2] - piece[state[0][pos]][3][2]
    state[0][pos] = piece[state[0][pos]][3][1]
    
    return state
        
def move(state, to):
    if check_can_move(state, to):
        return state
    elif check_empty(state, to):
        state[0][to] = state[1][0]
    elif check_can_merge(state, to):
        state[0][to] = piece[state[1][0]][2][state[0][to]]
    else:
        return state
    
    if state[1][1] != to:
        state[2] -= 1
    state[1] = [-1, 'none']
    
    return state  

def photon_in_place(photon, place):
    if place == photon:
        return True
    elif piece[place][3] == 0:
        return False
    elif piece[place][3][0] == photon:
        return True
    else:
        return photon_in_place(photon, piece[place][3][1])

def filter_photon(board, photon): #(status, extra_value -> +1 to merge, 0 to move, 99 can't move)
    result = []
    for place in board:
        if place == 0 or place == photon:
            result.append((place,0))
        elif res := photon_in_place(photon, place): 
            result.append((photon, 1))
        elif place in piece[photon][2]:
            result.append(('merge',1))
        else:
            result.append(('blocked', 99))
    return result

def dist(x,y):
    return sqrt((nodes[x][1][0]-nodes[y][1][0])**2 + (nodes[x][1][1]-nodes[y][1][1])**2)

def dist_to_goal(goal):
    dists = {}
    for i in range(0,18):
        dists[i] = dist(i, goal)
    return dists 

if __name__ == "__main__":
    print(filter_photon(LEVELS[3][0], 'ph_green'))
    print(filter_photon(LEVELS[3][3], 'ph_green'))
    print(dist_to_goal(9))