import pygame
import random
import math
import time
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
pygame.display.set_caption("Sorting Algorithm Visualizer")
window = Window(SCREEN)

#Features to GUI
window.add_widget(
    widget_id='size_input',
    widget=TextBox((30, 440, 100, 50), 'Size', GRAY, font1, '100')
)
window.add_widget(
    widget_id='algorithm_input',
    widget=DropdownBox((140, 440, 200, 50), 'Algorithm', GRAY, font1, list(AlgDict.keys()), WHITE)
)
window.add_widget(
    widget_id='play_button',
    widget=Button((350, 440, 40, 40), 'assets/playButton.png', 'assets/stopButton.png')
)
window.add_widget(
    widget_id= 'generate_array',
    widget=Button((400, 440, 125, 50), 'assets/resetButton.png', 'assets/resetButton.png')
)
window.add_widget(
    widget_id='Time',
    widget=TextBox((520, 440, 150, 50), 'Time', GRAY, font1, '0.0000s')
)


#drawing bars
def drawBars(screen, array, redBar1, redBar2, blueBar1, blueBar2, greenRows = {}):
    #Draw the bars and control their colors
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
    numbers = []
    numberReset = False
    running = True
    isPlaying = False
    isSorting = False
    isSearching = False
    sortingIterator = None

    # game loop
    while running:
        SCREEN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            window.update(event)

        isPlaying = window.get_widget_value('play_button')
        numberReset = window.get_widget_value('generate_array')

        #reset button
        if numberReset:
            numBars = int(window.get_widget_value('size_input'))
            numbers = [random.randint(10, 400) for i in range(numBars)]
            window.set_widget_value('generate_array', False)


        #play button pressed
        if isPlaying and not (isSorting or isSearching):

            # initialize sorting iterator
            sortingAlgorithm = window.get_widget_value('algorithm_input')
            start_time = time.time()
            if sortingAlgorithm == 'quick_sort':
                sortingIterator = quick_sort(numbers, 0, numBars - 1)
            if sortingAlgorithm == 'linear_search':
                if 'target_input' not in window.widgets:
                    window.add_widget(  # Button appears after linear search
                        widget_id='target_input',
                        widget=TextBox((750, 440, 100, 50), 'Target', GRAY, font1, '0')
                    )
                # Linear search case: use the target value from the input box
                try:
                    target_value = int(window.get_widget_value('target_input'))
                except ValueError:
                    target_value = 0  # Default to 0 if the input is invalid

                sortingIterator = linear_search(numbers, target_value)
                isSearching = True
            else:
                # Other sorting algorithms
                sortingIterator = AlgDict[sortingAlgorithm](numbers, 0, numBars - 1)
            isSorting = True

        #play button not pressed
        if not isPlaying:
            isSorting = False
            isSearching = False

        #searching algorithm
        if isSearching:
            try:
                # Fetch the next step of the linear search
                values = next(sortingIterator)

                if len(values) == 5:
                    # Linear search case: 5 values expected
                    numbers, redBar1, redBar2, blueBar1, blueBar2 = values
                    drawBars(SCREEN, numbers, redBar1, redBar2, blueBar1, blueBar2)

                    # Stop the search when the target is found
                    if blueBar1 != -1:
                        pygame.time.delay(1000)  # Pause for 2 seconds to show the found target
                        isSearching = False  # Stop searching
                        window.set_widget_value('play_button', False)

            except StopIteration:
                isSearching = False
                window.set_widget_value('play_button', False)

        #sorting algorithm
        if isSorting:
            try:
                numbers, redBar1, redBar2, blueBar1, blueBar2 = next(sortingIterator)
                drawBars(SCREEN, numbers, redBar1, redBar2, blueBar1, blueBar2)
            except StopIteration:
                end_time = time.time()
                elapsed_time = start_time - end_time

                window.set_widget_value('Time', f'{elapsed_time:.4f}s')

                isSorting = False
                window.set_widget_value('play_button', False)
        else:
            drawBars(SCREEN, numbers, -1, -1, -1, -1, greenRows=set(range(len(numbers))))

        window.render()
        pygame.display.update()


if __name__ == '__main__':
    main()
