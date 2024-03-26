from math import sqrt
import pygame

piece = {
            #photons
            'ph_red':[(127,0,0),True, {'ph_green':'ph_yellow', 'ph_blue':'ph_magenta', 'ph_cyan':'ph_white', 'pi_green':'pi_lime', 'pi_blue':'pi_purple', 'pi_cyan':'pi_blueS'}, 0],
            'ph_blue':[(0,0,127),True, {'ph_green':'ph_cyan', 'ph_red':'ph_magenta', 'ph_yellow':'ph_white', 'pi_red':'pi_violet', 'pi_green':'pi_mint', 'pi_yellow':'pi_beige'}, 0],
            'ph_green':[(0,127,0),True, {'ph_red':'ph_yellow', 'ph_blue':'ph_cyan', 'ph_magenta':'ph_white', 'pi_red':'pi_orange', 'pi_blue':'pi_mBlue', 'pi_magenta':'pi_pearl'}, 0],
            'ph_cyan':[(0,127,127),True, {'ph_red':'ph_white', 'pi_red':'pi_pink'},('ph_blue', 'ph_green')],
            'ph_yellow':[(127,127,0),True, {'ph_blue':'ph_white', 'pi_blue':'pi_lilac'},('ph_red', 'ph_green')],
            'ph_magenta':[(127,0,127),True, {'ph_green':'ph_white', 'pi_green':'pi_pistachio'},('ph_red', 'ph_blue')],
            'ph_white':[(240,240,240),True, {}, ('ph_red', 'ph_cyan')],
            
            #elemental pigments
            'pi_red':[(255,0,0),False,{},0],
            'pi_blue':[(0,0,255),False,{},0],
            'pi_green':[(0,255,0),False,{},0],
            'pi_cyan':[(0,255,255),False,{},0],
            'pi_yellow':[(255,255,0),False,{},0],
            'pi_magenta':[(255,0,255),False,{},0],
            'pi_white':[(255,255,255),False,{},0],
            
            #mix pigments
            'pi_orange':[(255,127,0),False,{},('ph_green', 'pi_red')],
            'pi_violet':[(255,0,127),False,{},('ph_blue', 'pi_red')],
            'pi_pink':[(255,127,127),False,{},('ph_cyan', 'pi_red')],
            'pi_lime':[(127,255,0),False,{},('ph_red', 'pi_green')],
            'pi_mint':[(0,255,127),False,{},('ph_blue', 'pi_green')],
            'pi_pistachio':[(127,255,127),False,{},('ph_violet', 'pi_green')],
            'pi_purple':[(127,0,255),False,{},('ph_red', 'pi_blue')],
            'pi_mBlue':[(0,127,255),False,{},('ph_green', 'pi_blue')],
            'pi_lilac':[(127,127,255),False,{},('ph_yellow', 'pi_blue')],
            'pi_blueS':[(127,255,255),False,{},('ph_red', 'pi_cyan')],
            'pi_pearl':[(255,127,255),False,{},('ph_green', 'pi_violet')],
            'pi_beige':[(255,255,127),False,{},('ph_blue', 'pi_yellow')],
            
            #empty space
            0:[(105, 105, 105),False,{},0]
            
        } #{piece:[code, can be moved, {photon:mix}, [splits]]} to change splits -> (selects, leaves behind)

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
    
    state[1] = [piece[state[0][pos]][3][0], pos]
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

def draw_piece(p_draw, screen, coord):
    if p_draw in piece:
        pygame.draw.circle(screen, piece[p_draw][0], coord, 20)
    else:
        pygame.draw.circle(screen, piece[0][0], coord, 20)

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
                        if state[1][0] != 0 and state[1][0] in piece:
                            #moves.append(state[0])
                            state = move(state, chosen_space)
                        elif piece[state[0][chosen_space]][1]:
                            state[1] = [state[0][chosen_space], chosen_space]
                            state[0][chosen_space] = 0
                            
                if(pygame.mouse.get_pressed()[2]):
                    chosen_space = in_circle(pygame.mouse.get_pos())
                    if state[1][0] == -1 and chosen_space != -1:
                        state = split(state, chosen_space)
                    else:
                        state[0][state[1][1]] = state[1][0]
                        state[1] = [-1, 'none'] 
            
        pygame.display.update()
    
    return 0

if __name__ == "__main__":
    main()