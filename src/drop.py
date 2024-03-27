from math import sqrt
import pygame

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
             ]
    ],
    3:[
        [   
            'yellow','white',
            'green',
            'green','white',
            'green','blue',
            'white','white',0,'blue','cyan',
            'red','blue',
            'red','white',
            'red',
            'purple','white'
            ], 0, 16,
            [
            'cyan','white',
            'green',
            'green','white',
            'green','blue',
            'white','white',0,'blue','purple',
            'red','blue',
            'red','white',
            'red',
            'yellow','white'
            ]
    ],
    4:[
        [   
            'white','white',
            0,
            0,0,
            0,0,
            0,0,'yellow',0,0,
            0,0,
            'yellow','yellow',
            0,
            'yellow','yellow'
            ], 0, 18,
            [
            'yellow','yellow',
            0,
            'yellow','yellow',
            0,0,
            0,0,'yellow',0,0,
            0,0,
            0,0,
            0,
            'white','white'
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
            'pi_orange':[(255,127,0),False,{},('ph_green', 'pi_red',1)],
            'pi_violet':[(255,0,127),False,{},('ph_blue', 'pi_red',1)],
            'pi_pink':[(255,127,127),False,{},('ph_cyan', 'pi_red',1)],
            'pi_lime':[(127,255,0),False,{},('ph_red', 'pi_green',1)],
            'pi_mint':[(0,255,127),False,{},('ph_blue', 'pi_green',1)],
            'pi_pistachio':[(127,255,127),False,{},('ph_violet', 'pi_green',1)],
            'pi_purple':[(127,0,255),False,{},('ph_red', 'pi_blue',1)],
            'pi_mBlue':[(0,127,255),False,{},('ph_green', 'pi_blue',1)],
            'pi_lilac':[(127,127,255),False,{},('ph_yellow', 'pi_blue',1)],
            'pi_blueS':[(127,255,255),False,{},('ph_red', 'pi_cyan',1)],
            'pi_pearl':[(255,127,255),False,{},('ph_green', 'pi_violet',1)],
            'pi_beige':[(255,255,127),False,{},('ph_blue', 'pi_yellow',1)],
            
            #empty space
            0:[(105, 105, 105),False,{},0]
            
        } #{piece:[code, can be moved, {photon:mix}, [splits]]} to change splits -> (selects, leaves behind, cost)

nodes = {
        0:[0,2,3,5], 1:[1,2,4,6], 
        2:[1,2,4,5], 
        3:[0,2,3,5,9], 4:[1,2,4,6,9], 
        5:[0,3,5,7,8], 6:[1,4,6,10,11], 
        7:[5,7,8,12], 8:[5,7,8,9,12], 9:[3,4,8,8,10,14,15], 10:[6,9,10,11,13], 11:[6,10,11,13],
        12:[7,8,12,14,17], 13:[10,11,13,15,18],
        14:[9,12,14,16,17], 15:[9,13,15,16,18],
        16:[14,15,16,17,18],
        17:[12,14,16,17], 18:[13,15,16,18]
        } #node1 -> node2, node2 -> node1

def check_can_piece_split(state, to_check):
    return piece[state[0][to_check]][3] == 0

def check_empty(state, to_check):
    return state[0][to_check] == 0

def check_can_merge(state, to): #can merge color
    return state[0][to] in piece[state[1][0]][2]

def check_can_move(state, to): #can move to space (empty and connected)
    return not(to in nodes[state[1][1]])

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