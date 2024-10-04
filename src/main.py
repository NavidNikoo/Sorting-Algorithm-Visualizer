import pygame  # Import the pygame library for creating games and multimedia applications
import random  # Import random for generating random numbers
import math  # Import math for mathematical functions
import time  # Import time for time-related functions
from visualization import Button, Window, TextBox, AlgorithmSelectionPopup, RadioButton  # Import GUI components
from algorithms.linear_search import linear_search  # Import the linear search algorithm
from AlgorithmDictionary import AlgDict  # Import the algorithm dictionary

# Initialize the pygame library
pygame.init()

# Define fonts for the GUI
font1 = pygame.font.SysFont('Times New Roman', 24)  # Set font style and size

# Define color constants for use in the GUI
BLACK = (0, 0, 0)  # Color for text and outlines
GRAY = (127, 127, 127)  # Color for inactive elements
WHITE = (250, 250, 250)  # Background color
RED = (255, 0, 0)  # Color for highlighting bars
GREEN = (0, 255, 0)  # Color for success indicators
BLUE = (0, 0, 255)  # Color for secondary highlights
LIGHT_GRAY = (200, 200, 200)  # Color for lighter elements
DARK_GRAY = (150, 150, 150)  # Color for darker elements

# Set screen size parameters
SCREEN_WIDTH = 900  # Width of the application window
SCREEN_HEIGHT = 500  # Height of the application window

# Set up the screen and window for the application
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create the display surface
pygame.display.set_caption("Sorting Algorithm Visualizer")  # Set the window title
window = Window(SCREEN)  # Create a window object

# Add GUI features to the window
window.add_widget(
    widget_id='size_input',
    widget=TextBox((30, 440, 100, 50), 'Size', GRAY, font1, '100')  # Input for size of the array
)
window.add_widget(
    widget_id='algorithm_select_button',
    widget=Button((140, 440, 200, 50), 'Select Algorithms', LIGHT_GRAY, DARK_GRAY)  # Button to select algorithms
)
window.add_widget(
    widget_id='play_pause_button',
    widget=Button((350, 440, 80, 40), 'Play', LIGHT_GRAY, DARK_GRAY)  # Button to start/pause the visualization
)
window.add_widget(
    widget_id='generate_array',
    widget=Button((440, 440, 80, 40), 'Reset', LIGHT_GRAY, DARK_GRAY)  # Button to reset the array
)
window.add_widget(
    widget_id='renew_button',
    widget=Button((530, 440, 80, 40), 'Renew', LIGHT_GRAY, DARK_GRAY)  # Button to generate a new random array
)

# Create the RadioButton for search options
search_option_radio = RadioButton((620, 440, 150, 50), 'Search for', GRAY, font1, ['Max', 'Min'])
search_option_radio.set_value('Max')  # Set default value to 'Max'
window.add_widget(widget_id='linear_search_option', widget=search_option_radio)

# Create the AlgorithmSelectionPopup with available algorithms
algorithm_popup = AlgorithmSelectionPopup(SCREEN, list(AlgDict.keys()))  # Initialize the algorithm selection popup

def calculate_layout(num_algorithms):
    """Calculate the layout for displaying algorithm bars based on the number of algorithms."""
    if num_algorithms == 1:
        return [(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 100)]  # Full width for one algorithm
    elif num_algorithms == 2:
        width = SCREEN_WIDTH // 2  # Divide screen width for two algorithms
        return [(0, 0, width, SCREEN_HEIGHT - 100),
                (width, 0, width, SCREEN_HEIGHT - 100)]
    elif num_algorithms == 3:
        width = SCREEN_WIDTH // 2  # Divide screen width for three algorithms
        height = (SCREEN_HEIGHT - 100) // 2  # Calculate height for three algorithms
        return [(0, 0, width, height),
                (width, 0, width, height),
                (0, height, SCREEN_WIDTH, height)]
    elif num_algorithms >= 4:
        width = SCREEN_WIDTH // 2  # Divide screen width for four or more algorithms
        height = (SCREEN_HEIGHT - 100) // 2
        return [(0, 0, width, height),
                (width, 0, width, height),
                (0, height, width, height),
                (width, height, width, height)]

def drawBars(screen, array, redBar1, redBar2, blueBar1, blueBar2, rect, algorithm_name):
    """Draw bars on the screen representing the current state of the sorting algorithm."""
    x, y, width, height = rect  # Unpack rectangle dimensions
    numBars = len(array)  # Get the number of bars
    if numBars != 0:
        bar_width = width / numBars  # Calculate width of each bar
        ceil_width = math.ceil(bar_width)  # Round up to ensure full coverage

    # Draw algorithm name
    name_font = pygame.font.SysFont('Arial', 20)  # Set font for algorithm name
    name_surface = name_font.render(algorithm_name, True, BLACK)  # Render the name
    name_rect = name_surface.get_rect(center=(x + width // 2, y + 20))  # Center the name
    screen.blit(name_surface, name_rect)  # Draw the name on the screen

    # Draw each bar in the array
    for num, bar_height in enumerate(array):
        # Determine color based on the state of the bar
        if num in (redBar1, redBar2):
            color = RED  # Highlighted bars
        elif num in (blueBar1, blueBar2):
            color = BLUE  # Secondary highlighted bars
        else:
            color = GRAY  # Default color for inactive bars
        scaled_height = (bar_height / 400) * (height - 40)  # Scale height for display
        pygame.draw.rect(screen, color, (x + num * bar_width, y + height - scaled_height, ceil_width, scaled_height))  # Draw the bar

def reset_array(window, original_numbers):
    """Reset the array to its original unsorted state."""
    numbers = original_numbers.copy()  # Copy the original numbers
    
    # Reset all related variables
    sortingIterators = {}  # Dictionary to hold sorting iterators
    algorithm_states = {}  # Dictionary to hold the state of each algorithm
    finished_algorithms = set()  # Set to track finished algorithms
    isSorting = False  # Flag to indicate if sorting is in progress
    isSearching = False  # Flag to indicate if searching is in progress
    start_times = {}  # Dictionary to hold start times for algorithms
    end_times = {}  # Dictionary to hold end times for algorithms
    pause_durations = {}  # Dictionary to hold pause durations for algorithms

    window.widgets['play_pause_button'].text = 'Play'  # Reset play/pause button text
    return numbers, sortingIterators, isSorting, isSearching, start_times, end_times, finished_algorithms, algorithm_states, pause_durations  # Return reset values

# Add these constants at the top of your file
VISUALIZATION_SPEED = 60  # Number of steps per second
STEP_DELAY = 1 / VISUALIZATION_SPEED  # Calculate delay between steps

def main():
    """Main function to run the sorting algorithm visualizer."""
    # Initialize numbers with a default size
    numBars = 100  # Default size for the array
    window.set_widget_value('size_input', str(numBars))  # Set the initial size in the input box
    original_numbers = [random.randint(10, 400) for _ in range(numBars)]  # Generate random numbers for the array
    numbers, sortingIterators, isSorting, isSearching, start_times, end_times, finished_algorithms, algorithm_states, pause_durations = reset_array(window, original_numbers)  # Reset the array and related variables
    
    running = True  # Flag to keep the main loop running
    isPaused = False  # Flag to indicate if the visualization is paused
    time_font = pygame.font.SysFont('Arial', 16)  # Font for displaying time
    pause_start_time = None  # Variable to track when the pause started
    pause_durations = {}  # Dictionary to store pause durations for each algorithm
    
    while running:  # Main loop
        SCREEN.fill(WHITE)  # Clear the screen with a white background
        for event in pygame.event.get():  # Process events
            if event.type == pygame.QUIT:  # Check for window close event
                running = False  # Exit the loop if the window is closed

            # Handle size input separately
            size_input = window.widgets['size_input']  # Get the size input widget
            if size_input.handle_event(event):  # Check if the size input has an event
                try:
                    new_size = max(1, int(size_input.get_value()))  # Ensure at least 1 bar
                    if new_size != len(numbers):  # Check if the size has changed
                        # Reset the array if the size has changed
                        numbers, sortingIterators, isSorting, isSearching, start_times, end_times, finished_algorithms, algorithm_states, pause_durations = reset_array(window, original_numbers)
                except ValueError:
                    pass  # Invalid input, do nothing

            # Handle events for other widgets
            for widget in window.widgets.values():  # Iterate through all widgets
                if widget != size_input:  # Skip the size input widget
                    widget.update(event)  # Update the widget with the event

            algorithm_popup.handle_event(event)  # Handle events for the algorithm selection popup

            # Handle play/pause button
            if window.get_widget_value('play_pause_button'):  # Check if the play/pause button is pressed
                window.set_widget_value('play_pause_button', False)  # Reset button state
                play_pause_button = window.widgets['play_pause_button']  # Get the play/pause button
                
                if not isSorting and not isSearching:  # Check if no sorting or searching is in progress
                    # Start sorting/searching
                    selectedAlgorithms = algorithm_popup.get_selected_algorithms()  # Get selected algorithms
                    for algorithm in selectedAlgorithms:  # Iterate through selected algorithms
                        if algorithm == 'linear_search':  # Check if linear search is selected
                            search_option = window.get_widget_value('linear_search_option')  # Get search option
                            if search_option == 'Max':
                                target = max(numbers)  # Set target to maximum value
                            elif search_option == 'Min':
                                target = min(numbers)  # Set target to minimum value
                            else:
                                continue  # Skip if no option is selected
                            sortingIterators[algorithm] = linear_search(numbers.copy(), target)  # Start linear search
                            start_times[algorithm] = time.time()  # Set start time for linear search
                            isSearching = True  # Set searching flag
                        else:
                            sortingIterators[algorithm] = AlgDict[algorithm](numbers.copy(), 0, len(numbers) - 1)  # Start sorting algorithm
                            start_times[algorithm] = time.time()  # Record start time
                    isSorting = True  # Set sorting flag
                    isPaused = False  # Ensure not paused
                    play_pause_button.text = 'Pause'  # Change button text to 'Pause'
                else:
                    # Toggle pause
                    isPaused = not isPaused  # Toggle the pause state
                    if isPaused:  # If now paused
                        pause_start_time = time.time()  # Record pause start time
                        play_pause_button.text = 'Play'  # Change button text to 'Play'
                    else:  # If resuming
                        if pause_start_time is not None:  # Check if there was a pause
                            pause_duration = time.time() - pause_start_time  # Calculate pause duration
                            for alg in start_times:  # Update pause durations for all algorithms
                                pause_durations[alg] = pause_durations.get(alg, 0) + pause_duration
                            pause_start_time = None  # Reset pause start time
                        play_pause_button.text = 'Pause'  # Change button text to 'Pause'

            # Handle reset button
            if window.get_widget_value('generate_array'):  # Check if reset button is pressed
                numbers, sortingIterators, isSorting, isSearching, start_times, end_times, finished_algorithms, algorithm_states, pause_durations = reset_array(window, original_numbers)  # Reset the array
                window.set_widget_value('generate_array', False)  # Reset button state
                isPaused = False  # Ensure not paused

        # Get the current state of buttons
        numberReset = window.get_widget_value('generate_array')  # Check reset button state
        numberRenew = window.get_widget_value('renew_button')  # Check renew button state
        openAlgorithmSelect = window.get_widget_value('algorithm_select_button')  # Check algorithm selection button state

        # Show/hide linear search option based on selection
        linear_search_selected = 'linear_search' in algorithm_popup.get_selected_algorithms()  # Check if linear search is selected
        window.set_widget_visibility('linear_search_option', linear_search_selected)  # Show/hide the option

        # Check if size has changed
        current_size = int(window.get_widget_value('size_input'))  # Get current size from input
        if current_size != len(numbers):  # If size has changed
            numbers, sortingIterators, isSorting, isSearching, start_times, end_times, finished_algorithms, algorithm_states, pause_durations = reset_array(window, original_numbers)  # Reset the array

        if openAlgorithmSelect:  # If algorithm selection button is pressed
            algorithm_popup.toggle()  # Toggle the visibility of the algorithm selection popup
            window.set_widget_value('algorithm_select_button', False)  # Reset the button state

        if numberReset:  # If reset button is pressed
            numbers, sortingIterators, isSorting, isSearching, start_times, end_times, finished_algorithms, algorithm_states, pause_durations = reset_array(window, original_numbers)  # Reset the array
            window.set_widget_value('generate_array', False)  # Reset button state
            isPaused = False  # Ensure not paused

        if numberRenew:  # If renew button is pressed
            # Generate a completely new random array
            original_numbers = [random.randint(10, 400) for _ in range(current_size)]  # Generate new random numbers
            numbers, sortingIterators, isSorting, isSearching, start_times, end_times, finished_algorithms, algorithm_states, pause_durations = reset_array(window, original_numbers)  # Reset the array
            window.set_widget_value('renew_button', False)  # Reset button state

        if isSorting and not isPaused:
            selectedAlgorithms = algorithm_popup.get_selected_algorithms()  # Get selected algorithms
            layout = calculate_layout(len(selectedAlgorithms))  # Calculate layout based on selected algorithms

            for i, algorithm in enumerate(selectedAlgorithms):  # Iterate through selected algorithms
                if i < len(layout) and algorithm in sortingIterators and algorithm not in finished_algorithms:
                    try:
                        if algorithm == 'linear_search':
                            # Handle linear search separately
                            result = next(sortingIterators[algorithm])  # Get the next result from the linear search iterator
                            if len(result) == 3:  # Linear search returns (array, current_index, found)
                                numbers, current_index, found = result
                                redBar1, redBar2 = current_index, -1  # Set highlighted bars for linear search
                                blueBar1, blueBar2 = (-1, -1) if not found else (current_index, -1)  # Set secondary highlighted bars
                            else:
                                numbers, redBar1, redBar2, blueBar1, blueBar2 = result  # Unpack result for other algorithms
                        else:
                            # Handle other algorithms
                            numbers, redBar1, redBar2, blueBar1, blueBar2 = next(sortingIterators[algorithm])  # Get the next result
                        
                        algorithm_states[algorithm] = (numbers, redBar1, redBar2, blueBar1, blueBar2)  # Update algorithm states
                    except StopIteration:
                        finished_algorithms.add(algorithm)  # Mark algorithm as finished
                        end_times[algorithm] = time.time()  # Record end time

                if algorithm in algorithm_states:  # If algorithm state exists
                    numbers, redBar1, redBar2, blueBar1, blueBar2 = algorithm_states[algorithm]  # Unpack algorithm state
                    drawBars(SCREEN, numbers, redBar1, redBar2, blueBar1, blueBar2, layout[i], algorithm)  # Draw bars for the algorithm
                    
                    # Update and display time for all algorithms, including linear search
                    if algorithm in start_times:  # If start time exists
                        if algorithm in end_times:  # If end time exists
                            elapsed_time = end_times[algorithm] - start_times[algorithm] - pause_durations.get(algorithm, 0)  # Calculate elapsed time
                        else:
                            elapsed_time = time.time() - start_times[algorithm] - pause_durations.get(algorithm, 0)  # Calculate elapsed time
                        time_surface = time_font.render(f'Time: {elapsed_time:.4f}s', True, BLACK)  # Render elapsed time
                        x, y, width, _ = layout[i]  # Unpack layout dimensions
                        SCREEN.blit(time_surface, (x + width - 100, y + 5))  # Draw elapsed time on the screen

        else:
            # Draw current state of algorithms (sorted, partially sorted, or unsorted)
            selectedAlgorithms = algorithm_popup.get_selected_algorithms()  # Get selected algorithms
            layout = calculate_layout(len(selectedAlgorithms))  # Calculate layout based on selected algorithms
            for i, algorithm in enumerate(selectedAlgorithms):  # Iterate through selected algorithms
                if i < len(layout):  # Check if within layout bounds
                    if algorithm in algorithm_states:  # If algorithm state exists
                        numbers, redBar1, redBar2, blueBar1, blueBar2 = algorithm_states[algorithm]  # Unpack algorithm state
                    else:
                        numbers, redBar1, redBar2, blueBar1, blueBar2 = numbers, -1, -1, -1, -1  # Default values if no state
                    drawBars(SCREEN, numbers, redBar1, redBar2, blueBar1, blueBar2, layout[i], algorithm)  # Draw bars for the algorithm
                    
                    # Display time if available
                    if algorithm in start_times:  # If start time exists
                        if algorithm in end_times:  # If end time exists
                            elapsed_time = end_times[algorithm] - start_times[algorithm] - pause_durations.get(algorithm, 0)  # Calculate elapsed time
                        else:
                            if isPaused:  # If paused
                                elapsed_time = pause_start_time - start_times[algorithm] - pause_durations.get(algorithm, 0)  # Calculate elapsed time during pause
                            else:
                                elapsed_time = time.time() - start_times[algorithm] - pause_durations.get(algorithm, 0)  # Calculate elapsed time
                        time_surface = time_font.render(f'Time: {elapsed_time:.4f}s', True, BLACK)  # Render elapsed time
                        x, y, width, _ = layout[i]  # Unpack layout dimensions
                        SCREEN.blit(time_surface, (x + width - 100, y + 5))  # Draw elapsed time on the screen

        window.render()  # Render the window
        algorithm_popup.render()  # Render the algorithm selection popup
        pygame.display.update()  # Update the display

if __name__ == '__main__':
    main()  # Run the main function