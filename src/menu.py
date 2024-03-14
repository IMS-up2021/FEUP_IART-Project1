import pygame, sys

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Drop of Light")



def initialize_screen():
    pygame.init()
    return pygame.display.set_mode((1280, 720))

def get_font(size):
    return pygame.font.Font("assets_menu/font.ttf", size)

def display_text(screen, text, size, color, position):
    font = get_font(size)
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect(center=position)
    screen.blit(text_render, text_rect)

def create_button(pos, text, font_size, base_color, hovering_color):
    return Button(pos=pos, text_input=text, font=get_font(font_size), base_color=base_color, hovering_color=hovering_color)

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
                    play()
                elif options_button.checkForInput(mouse_pos):
                    options()
                elif quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play():
    screen = initialize_screen()

    while True:
        screen.fill((0 ,0 ,0))
        
        display_text(screen ,"THIS IS THE PLAY SCREEN" ,40 ,(255 ,255 ,255) ,(640 ,260))

        back_button = create_button((640 ,460) ,"BACK" ,50 ,(255 ,255 ,255) ,(100 ,100 ,100))
        
        back_button.rect = pygame.Rect(back_button.pos[0] - 75 ,back_button.pos[1] - 25 ,150 ,50)
        
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
