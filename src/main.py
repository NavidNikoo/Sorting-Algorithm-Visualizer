import pygame
import random
import math
from visualization import Button, Window, TextBox, DropdownBox
from src.algorithms.linear_search import linear_search
from src.algorithms.quick_sort import quick_sort
from AlgorithmDictionary import AlgDict

pygame.init()

#fonts
font1 = pygame.font.SysFont('Times New Roman', 24)

#colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (250, 250, 250)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#Screen size parameters
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500

#screen and window set up
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")
window = Window(SCREEN)

#Features to GUI
window.add_widget(
    widget_id='size_input',
    widget=TextBox((30, 440, 100, 50), 'Size', GRAY, font1, '100')
)
window.add_widget(
    widget_id='algorithmInput',
    widget=DropdownBox((140, 440, 200, 50), 'Algorithm', GRAY, font1, list(AlgDict.keys()), WHITE)
)
window.add_widget(
    widget_id='playButton',
    widget=Button((350, 440, 40, 40), 'assets/playButton.png', 'assets/stopButton.png')
)

#drawing bars
def drawBars(screen, array, redBar1, redBar2, blueBar1, blueBar2, greenRows = {}):
    '''Draw the bars and control their colors'''
    numBars = len(array)
    if numBars != 0:
        bar_width  = 900 / numBars
        ceil_width = math.ceil(bar_width)

    for num in range(numBars):
        if   num in (redBar1, redBar2)  : color = RED
        elif num in (blueBar1, blueBar2): color = BLUE
        elif num in greenRows           : color = GREEN
        else                            : color = GRAY
        pygame.draw.rect(screen, color, (num * bar_width, 400 - array[num], ceil_width, array[num]))


def main():
    numbers = []    #empty array for input
    running = True
    isPlaying = False
    isSorting = False
    isSearching = False
    sortingIterator = None

    while running: #game loop
        SCREEN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            window.update(event)

        isPlaying = window.get_widget_value('playButton')
        if isPlaying and not (isSorting or isSearching):
            # random list to be sorted
            numBars = int(window.get_widget_value('size_input'))
            numbers = [random.randint(10, 400) for i in range(numBars)]

            # initialize sorting iterator
            sortingAlgorithm = window.get_widget_value('algorithmInput')
            if sortingAlgorithm == 'linear_search':
                window.add_widget(    # Button appears after linear search
                    widget_id='target_input',
                    widget=TextBox((410, 440, 100, 50), 'Target', GRAY, font1, '0')
                )
                # Linear search case: use the target value from the input box
                target = int(window.get_widget_value('target_input'))
                sortingIterator = linear_search(numbers, target)
                isSearching = True
            else:
                if sortingAlgorithm == 'quick_sort':
                    sortingIterator = quick_sort(numbers, 0, numBars - 1)
                else:
                    # Other sorting algorithms
                    sortingIterator = AlgDict[sortingAlgorithm](numbers, 0, numBars - 1)
                isSorting = True

        if not isPlaying:
            isSorting = False

        # If linear search is running
        if isSearching:
            try:
                result = next(sortingIterator)
                numbers, currentIndex = result[:2]  # Only unpack the first two elements if there are extra values
                # Highlight the current index being compared in blue
                drawBars(SCREEN, numbers, -1, -1, currentIndex, -1)
            except StopIteration:
                isSearching = False
                window.set_widget_value('playButton', False)


        if isSorting:
            try:
                numbers, redBar1, redBar2, blueBar1, blueBar2 = next(sortingIterator)
                drawBars(SCREEN, numbers, redBar1, redBar2, blueBar1, blueBar2)
            except StopIteration:
                isSorting = False
                window.set_widget_value('playButton', False)
        else:
            drawBars(SCREEN, numbers, -1, -1, -1, -1, greenRows=set(range(len(numbers))))

        window.render()
        pygame.display.update()


if __name__ == '__main__':
    main()
