from math import sqrt
import pygame

photon = {
            'red':[(255,0,0),{'green':'moregreen', 'blue':'purple', 'cyan':'cyan'}, {'green':'yellow', 'blue':'purple', 'cyan':'white'}, []],
            'blue':[(0,0,255),{'red':'violet', 'green':'aqua_green', 'yellow':'light_yellow'}, {'green':'cyan', 'red':'purple', 'yellow':'white'}, []],
            'green':[(0,255,0),{'red':'orange', 'blue':'blue_sky', 'purple':'pink'}, {'red':'yellow', 'blue':'cyan', 'purple':'white'}, []],
            'cyan':[(0,255,255),{'red':'beige'},{'red':'white'},['blue', 'green']],
            'yellow':[(255,255,0),{'blue':'light_blue'},{'blue':'white'},['red', 'green']],
            'purple':[(255,0,255),{'green':'light_green'},{'green':'white'},['red', 'blue']],
            'white':[(255,255,255),{}, {}, ['red', 'green', 'blue']]
        } #{photon:[code, {pigment:mix}, {photon:mix}, [splits]]}

nodes = {
        0:[2,3,5], 1:[2,4,6], 
        2:[1,2,4,5], 
        3:[0,2,5,9], 4:[1,2,6,9], 
        5:[0,3,7,8], 6:[1,4,10,11], 
        7:[5,8,12], 8:[5,7,9,12], 9:[3,4,8,10,14,15], 10:[6,9,11,13], 11:[6,10,13],
        12:[7,8,9,14,17], 13:[10,11,15,18],
        14:[9,12,16,17], 15:[9,13,16,18],
        16:[14,15,17,18],
        17:[12,14,16], 18:[13,15,16]
        } #node1 -> node2, node2 -> node1

coords = [(250, 100),(550, 100),
              (400, 160),
              (325, 200),(475, 200),
              (250, 240),(550, 240),
              (100, 320),(250, 320),(400, 320),(550, 320),(700, 320),
              (250, 400),(550, 400),
              (325, 440),(475, 440),
              (400, 480),
              (250, 560),(550, 560)] #to draw board

def check_can_photon_split(state, to_check):
    if photon[state[0][to_check]] in photon:
        return photon[state[0][to_check]] == []
    return 1

def check_empty(state, to_check):
    return state[0][to_check] == 0

def check_can_merge(state, fr, to): #can merge color
    return state[0][to] in photon[state[0][fr]][2]

def check_can_move(state, fr, to): #can move to space (empty and connected)
    return not(to in nodes[fr])

def check_win(state):
    return state[0] == state[3]

def split(state, photon):
    if check_can_photon_split(state, photon):
        return 1
    return 0
        
def move(state, fr, to):
    if check_can_move(state, fr, to):
        return state
    elif check_empty(state, to):
        state[0][to] = state[0][fr]
        state[0][fr] = 0
    elif check_can_merge(state, fr, to):
        state[0][to] = photon[state[0][to]][2][state[0][fr]]
        state[0][fr] = 0
    state[2] -= 1
    return state

def draw_photon(p_draw, screen, coord):
    if p_draw in photon:
        pygame.draw.circle(screen, photon[p_draw][0], coord, 20)
    else:
        pygame.draw.circle(screen, (105, 105, 105), coord, 20)

def draw_board(board, screen):
    i = 0
    
    while i < len(coords):
        draw_photon(board[i], screen, coords[i])
        i += 1
        
def dist_points(pos_1, pos_2):
    return sqrt((pos_1[0] - pos_2[0])**2+(pos_1[1] - pos_2[1])**2)
         

def in_circle(to_check):
    i = 0
    
    while i < len(coords):
        if dist_points(coords[i], to_check) < 20:
            return i
        i += 1
    
    return -1
        

def main():
    state = [[
              0,0,
              'red',
              'red',0,
              'red','green',
              0,0,0,'green',0,
              'blue','green',
              'blue',0,
              'blue',
              0,0
             ], [0,'none'], 9,
             [
              0,0,
              0,
              0,'yellow',
              0,0,
              0,'purple','white',0,0,
              0,0,
              0,'cyan',
              0,
              0,0
             ]] #board, selected (color,pos), nº remaining moves, goal

    pygame.init()

    moves = []

    screen_width = 800
    screen_height = 800
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    run = True
    selected = False
    
    while run:
        
        l = 40
        
        if(check_win(state)):
            run = False
            print('you win!!')
            continue
        
        draw_board(state[0], screen)

        draw_photon(state[1][0], screen, [100,700])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_ESCAPE and len(moves) > 0:
                    state = moves[0]
                    moves.pop()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(pygame.mouse.get_pressed()[0]):
                    chosen_space = in_circle(pygame.mouse.get_pos())
                    
                    if chosen_space != -1:
                        moves.append(state)
                        if state[1][0] != 0:
                            state = move(state, state[1][1], chosen_space)
                            state[1][0] = 0
                            state[1][1] = 'none'
                            print(state[2])
                        else:
                            state[1][0] = state[0][chosen_space]
                            state[1][1] = chosen_space
            
            
        pygame.display.update()
    
    return 0

if __name__ == "__main__":
    main()