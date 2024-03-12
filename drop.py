import pygame

photon = {
            'red':[(255,0,0),{'green':'moregreen', 'blue':'purple', 'cyan':'cyan'}, {'green':'yellow', 'blue':'purple'}, []],
            'blue':[(0,0,255),{'red':'violet', 'green':'aqua_green', 'yellow':'light_yellow'}, {'green':'cyan', 'red':'purple'}, []],
            'green':[(0,255,0),{'red':'orange', 'blue':'blue_sky', 'purple':'pink'}, {'red':'yellow', 'blue':'cyan'}, []],
            'cyan':[(0,255,255),{'red':'beige'},{'red':'white'},['blue', 'green']],
            'yellow':[(255,255,0),{'blue':'light_blue'},{'blue':'white'},['red', 'green']],
            'purple':[(255,0,255),{'green':'light_green'},{'green':'white'},['red', 'blue']],
            'white':[(255,255,255),0, 0, ['red', 'green', 'blue']]
        } #{photon:[code, {pigment:mix}, {photon:mix}, [splits]]}

nodes = {
        0:[2,3,5], 1:[2,4,6], 
        2:[1,2,4,5], 
        3:[0,2,5], 4:[1,2,6], 
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
    return state[0][to] in photon[state[fr]]

def check_can_move(state, fr, to): #can move to space (empty and connected)
    return to in nodes[fr]

def check_win(state):
    return state[0] == state[3]

def split(state, photon):
    if check_can_photon_split(state, photon):
        return 1
    return 0
        
def move(state, fr, to):
    if check_can_move(state, fr, to):
        return 1
    elif check_empty(to):
        state[0][to] = state[0][fr]
        state[0][fr] = 0
        return state
    elif check_can_merge(state, fr, to):
        state[0][to] = photon[state[0][to]][state[0][fr]]
        state[0][fr] = 0
        return state
    return 1

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
        
    #draw_photon(state[1], screen, (100, 700))

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
             ], 'red', 0,
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
             ]] #board, selected, nº remaining moves, goal

    pygame.init()

    screen_width = 800
    screen_height = 800
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    run = True
    selected = False
    
    state = move(state, 2, 1)
    
    while run:
        
        l = 40
        
        draw_board(state[0], screen)
        #draw_board(state[3], screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
           
        #if(pygame.mouse.get_pressed[0] and in_circle(pygame.mouse.get_pos())){
        #    
        #}
            
        pygame.display.update()
    
    return 0

if __name__ == "__main__":
    main()