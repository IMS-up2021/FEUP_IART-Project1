from math import sqrt
import pygame, sys, drop, copy

pygame.init()

screen_x = 1280
screen_y = 720

SCREEN = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Drop of Light")

coords = [(490, 100),(790, 100),
              (640, 187),
          (565, 230),(715, 230),
          (490, 273),(790, 273),
          (340, 360),(490, 360),(640, 360),(790, 360),(940, 360),
          (490, 447),(790, 447),
          (565, 490),(715, 490),
              (640, 533),
          (490, 620),(790, 620)] #to draw board

pieces = []

def initialize_screen():
    pygame.init()
    return pygame.display.set_mode((screen_x, screen_y))

def get_font(size):
    return pygame.font.Font("assets_menu/font.ttf", size)

def display_text(screen, text, size, color, position):
    font = get_font(size)
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect(center=position)
    screen.blit(text_render, text_rect)

def create_button(pos, text, font_size, base_color, hovering_color):
    return Button(pos=pos, text_input=text, font=get_font(font_size), base_color=base_color, hovering_color=hovering_color)

def create_piece(coord, color, pos):
    return Piece(coord=coord, color=color, pos=pos)

class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.pos = pos
        self.text = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.rect = None

    def update(self, screen):
        pygame.draw.rect(screen, self.base_color, self.rect)
        display_text(screen, self.text, 30, "black", (self.pos[0], self.pos[1]))

    def changeColor(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.base_color = self.hovering_color
        else:
            self.base_color = (139, 0, 39)

    def checkForInput(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Piece:
    def __init__(self, coord, color, pos):
        self.coord = coord
        self.color = color
        self.pos = pos
        self.rect = None

    def update(self, screen):
        if self.color in drop.piece:
            pygame.draw.circle(screen, drop.piece[self.color][0], self.coord, 20)
        else:
            pygame.draw.circle(screen, drop.piece[0][0], self.coord, 20)

    def checkForInput(self, mouse_pos):
        return dist_points(self.coord, mouse_pos) < 20
    
    def set_color(self, color):
        self.color = color
        
    def get_pos(self):
        return self.pos

def dist_points(pos_1, pos_2):
    return sqrt((pos_1[0] - pos_2[0])**2+(pos_1[1] - pos_2[1])**2)
   
def make_board(board):
    i = 0
    for i in range(len(coords)):
        pieces.append(create_piece(coords[i], board[i], i))
        i += 1
        
def draw_board(board, screen):
    pygame.draw.line(screen, (100, 100, 100), coords[0], coords[11], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[0], coords[18], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[0], coords[17], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[1], coords[7], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[1], coords[17], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[1], coords[18], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[7], coords[11], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[7], coords[18], 5)
    pygame.draw.line(screen, (100, 100, 100), coords[11], coords[17], 5)
    
    for piece in pieces:
        piece.set_color(board[piece.get_pos()]) 
        piece.update(screen)
        
def in_piece(mouse_pos):
    i = 0
    for i in range(len(pieces)):
        if pieces[i].checkForInput(mouse_pos):
            return i
    return -1

def main_menu():
    screen = initialize_screen()
    
    while True:
        screen.fill((0, 0, 0))

        display_text(screen, "MAIN MENU", 60, (139, 0, 39), (640, 100))

        play_button = create_button((640, 250), "PLAY", 40, (128, 0, 32), (100 ,100 ,100))
        options_button = create_button((640 ,400), "INSTRUCTIONS", 40,(200 ,200 ,200), (100 ,100 ,100))
        quit_button = create_button((640 ,550), "QUIT", 40,(200 ,200 ,200), (100 ,100 ,100))

        for button in [play_button ,options_button ,quit_button]:
            button.rect = pygame.Rect(button.pos[0] - 180 ,button.pos[1] - 40 ,360 ,80)
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.checkForInput(mouse_pos):
                    choose_level()
                elif options_button.checkForInput(mouse_pos):
                    options()
                elif quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
def choose_level():
    screen = initialize_screen()
    loop = True
    
    while loop:
        screen.fill((0, 0, 0))

        display_text(screen, "LEVEL SELECT", 60, (139, 0, 39), (640, 100))

        level_1 = create_button((427, 250), "1", 40, (128, 0, 32), (100 ,100 ,100))
        level_2 = create_button((854, 250), "2", 40,(200 ,200 ,200), (100 ,100 ,100))
        level_3 = create_button((427, 400), "3", 40,(200 ,200 ,200), (100 ,100 ,100))
        level_4 = create_button((854, 400), "4", 40,(200 ,200 ,200), (100 ,100 ,100))
        back_button = create_button((640, 550), "BACK", 40,(200 ,200 ,200), (100 ,100 ,100))

        for button in [level_1, level_2, level_3, level_4, back_button]:
            button.rect = pygame.Rect(button.pos[0] - 180 ,button.pos[1] - 40 ,360 ,80)
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if level_1.checkForInput(mouse_pos):
                    teste = copy.deepcopy(drop.LEVELS[1])
                    play(teste)
                if level_2.checkForInput(mouse_pos):
                    teste = copy.deepcopy(drop.LEVELS[2])
                    play(teste)
                if level_3.checkForInput(mouse_pos):
                    teste = copy.deepcopy(drop.LEVELS[3])
                    play(teste)
                if level_4.checkForInput(mouse_pos):
                    teste = copy.deepcopy(drop.LEVELS[4])
                    play(teste)
                elif back_button.checkForInput(mouse_pos):
                    loop = False

        pygame.display.update()
    

def play(state):
    screen = initialize_screen()

    run = True
    font = pygame.font.Font(None, 36)
    
    make_board(state[0])

    while run:
        screen.fill((0 ,0 ,0))
        
        if(drop.check_win(state)):
            run = False
            print('you win!!')
            continue
        
        if(state[2] <= 0):
            run = False
            print('out of moves')
            continue
        
        draw_board(state[0], screen)
        
        text_surface = font.render("Moves: " + str(state[2]), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(60, 20))
        screen.blit(text_surface, text_rect)

        if state[1][0] in drop.piece:
            pygame.draw.circle(screen, drop.piece[state[1][0]][0], (80,100), 20)
        else:
            pygame.draw.circle(screen, drop.piece[0][0], (80,100), 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                    
                if(pygame.mouse.get_pressed()[0]):
                    chosen_space = in_piece(mouse_pos)
                    
                    if chosen_space != -1:
                        if state[1][0] != 0 and state[1][0] in drop.piece:
                            state = drop.move(state, chosen_space)
                        elif drop.piece[state[0][chosen_space]][1]:
                            state[1] = [state[0][chosen_space], chosen_space, 0]
                            state[0][chosen_space] = 0
                            
                if(pygame.mouse.get_pressed()[2]):
                    chosen_space = in_piece(mouse_pos)
                    if state[1][0] == -1 and chosen_space != -1:
                        state = drop.split(state, chosen_space)
                    else:
                        state[0][state[1][1]] = state[1][0]
                        state[1] = [-1, 'none', 0]

        pygame.display.update()

def options():
    screen = initialize_screen()

    while True:
        screen.fill((0, 0, 0))
        display_text(screen, "INSTRUCTIONS", 60, (139, 0, 39), (640, 100))

        display_text(screen, "Drops of Light is a single player puzzle", 20, (255, 255, 255), (640, 260))
        display_text(screen, "game that's played on a star shaped web.", 20, (255, 255, 255), (640, 285))
        display_text(screen,"On the web are what look like coloured beads,", 20, (255, 255, 255), (640, 310))
        display_text(screen,"these are photons and the puzzle is to move,", 20, (255, 255, 255), (640, 335))
        display_text(screen,"arrange and combine the photons to produce a", 20, (255, 255, 255), (640, 360))
        display_text(screen,"specific pattern of colours.", 20, (255, 255, 255), (640, 385))

        back_button = create_button((640, 460), "BACK", 50, (0, 0, 0), (100, 100, 100))
        
        back_button.rect = pygame.Rect(back_button.pos[0] - 75, back_button.pos[1] - 25, 150, 50)
        
        back_button.changeColor(pygame.mouse.get_pos())
        
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.checkForInput(mouse_pos):
                    main_menu()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
