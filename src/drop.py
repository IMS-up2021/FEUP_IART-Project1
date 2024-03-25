from math import sqrt
import pygame

piece = {
            #photons
            'ph_red':[(127,0,0),True,{'ph_green':'moreph_green', 'ph_blue':'ph_magenta', 'ph_cyan':'ph_cyan'}, {'ph_green':'ph_yellow', 'ph_blue':'ph_magenta', 'ph_cyan':'ph_white'}, []],
            'ph_blue':[(0,0,127),True,{'ph_red':'ph_magenta', 'ph_green':'aqua_ph_green', 'ph_yellow':'light_ph_yellow'}, {'ph_green':'ph_cyan', 'ph_red':'ph_magenta', 'ph_yellow':'ph_white'}, []],
            'ph_green':[(0,127,0),True,{'ph_red':'orange', 'ph_blue':'ph_blue_sky', 'ph_magenta':'pink'}, {'ph_red':'ph_yellow', 'ph_blue':'ph_cyan', 'ph_magenta':'ph_white'}, []],
            'ph_cyan':[(0,127,127),True,{'ph_red':'beige'},{'ph_red':'ph_white'},['ph_blue', 'ph_green']],
            'ph_yellow':[(127,127,0),True,{'ph_blue':'light_ph_blue'},{'ph_blue':'ph_white'},['ph_red', 'ph_green']],
            'ph_magenta':[(127,0,127),True,{'ph_green':'light_ph_green'},{'ph_green':'ph_white'},['ph_red', 'ph_blue']],
            'ph_white':[(127,127,127),True,{}, {}, ['ph_red', 'ph_green', 'ph_blue']],
            
            #elemental pigments
            'pi_red':[(255,0,0),False,{},{},[]],
            'pi_blue':[(0,0,255),False,{},{},[]],
            'pi_green':[(0,255,0),False,{},{},[]],
            'pi_cyan':[(0,255,255),False,{},{},[]],
            'pi_yellow':[(255,255,0),False,{},{},[]],
            'pi_magenta':[(255,0,255),False,{},{},[]],
            'pi_white':[(255,255,255),False,{},{},[]],
            
            #mix pigments
            'pi_orange':[(255,127,0),False,{},{},[]],
            'pi_violet':[(255,0,127),False,{},{},[]],
            'pi_pink':[(255,127,127),False,{},{},[]],
            'pi_lime':[(127,255,0),False,{},{},[]],
            'pi_mint':[(0,255,127),False,{},{},[]],
            'pi_pistachio':[(127,255,127),False,{},{},[]],
            'pi_purple':[(127,0,255),False,{},{},[]],
            'pi_mBlue':[(0,127,255),False,{},{},[]],
            'pi_lilac':[(127,127,255),False,{},{},[]],
            'pi_blueS':[(127,255,255),False,{},{},[]],
            'pi_pearl':[(255,127,255),False,{},{},[]],
            'pi_beige':[(255,255,127),False,{},{},[]],
            
            #empty space
            0:[(105, 105, 105),False,{},{},[]]
            
        } #{piece:[code, can be moved, {pigment:mix}, {photon:mix}, [splits]]}

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

def check_can_piece_split(state, to_check):
    if piece[state[0][to_check]] in piece:
        return piece[state[0][to_check]] == []
    return 1

def check_empty(state, to_check):
    return state[0][to_check] == 0

def check_can_merge(state, fr, to): #can merge color
    return state[0][to] in piece[state[0][fr]][3]

def check_can_move(state, fr, to): #can move to space (empty and connected)
    return not(to in nodes[fr])

def check_win(state):
    return state[0] == state[3]

def split(state, piece):
    if check_can_piece_split(state, piece):
        return 1
    return 0
        
def move(state, fr, to):
    if check_can_move(state, fr, to):
        return state
    elif check_empty(state, to):
        state[0][to] = state[0][fr]
        state[0][fr] = 0
    elif check_can_merge(state, fr, to):
        state[0][to] = piece[state[0][to]][3][state[0][fr]]
        state[0][fr] = 0
    state[2] -= 1
    return state

def draw_piece(p_draw, screen, coord):
    pygame.draw.circle(screen, piece[p_draw][0], coord, 20)

def draw_board(board, screen):
    i = 0
    
    while i < len(coords):
        draw_piece(board[i], screen, coords[i])
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
              'ph_red',
              'ph_red',0,
              'ph_red','ph_green',
              0,0,0,'ph_green',0,
              'ph_blue','ph_green',
              'ph_blue',0,
              'ph_blue',
              0,0
             ], [0,'none'], 9,
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
             ]] #board, selected (color,pos), nº remaining moves, goal

    pygame.init()

    #moves = []
    
    font = pygame.font.Font(None, 36)

    screen_width = 800
    screen_height = 800
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    run = True
    selected = False
    
    while run:
        
        screen.fill((0, 0, 0))
        
        l = 40
        
        if(check_win(state)):
            run = False
            print('you win!!')
            continue
        
        draw_board(state[0], screen)
        
        text_surface = font.render("Moves: " + str(state[2]), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(60, 20))
        screen.blit(text_surface, text_rect)

        draw_piece(state[1][0], screen, [100,700])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and len(moves) > 0:
                    state[0] = moves[0].copy()
                    moves.pop()
            '''
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(pygame.mouse.get_pressed()[0]):
                    chosen_space = in_circle(pygame.mouse.get_pos())
                    
                    if chosen_space != -1:
                        if state[1][0] != 0:
                            #moves.append(state[0])
                            state = move(state, state[1][1], chosen_space)
                            state[1] = [0, 'none'] 
                        elif piece[state[0][chosen_space]][1]:
                            state[1] = [state[0][chosen_space], chosen_space]
                            
                if(pygame.mouse.get_pressed()[2]):
                    state[1] = [0, 'none'] 
            
            
        pygame.display.update()
    
    return 0

if __name__ == "__main__":
    main()