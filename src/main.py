import pygame
from visualization import Button

pygame.init()

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (250, 250, 250)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#Screen size paramters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

def main():
    #exit_img = pygame.image.load('exit_btn.png').convert_alpha()
    #start_img = pygame.image.load('start_btn.png').convert_alpha()

    #start_button = Button(100, 200, start_img, 0.8)
    #exit_button = Button(450, 200, exit_img, 0.8)

    # game loop
    run = True
    while run:

        SCREEN.fill(GRAY)

        #if start_button.draw(SCREEN):
        #    print('START')
        #if exit_button.draw(SCREEN):
        #    print('EXIT')
        #    run = False

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()