# File for building classes for all our GUI tools
import pygame
import sys
from abc import ABC, abstractmethod  # Abstract base classes, help to make different shapes
from pygame.color import THECOLORS

class Window:
    def __init__(self, screen):
        """Initialize the Window with a screen and an empty widget dictionary."""
        self.screen = screen
        self.widgets = {}  # Dictionary to hold widgets

    def add_widget(self, widget_id, widget):
        """Add a widget to the window using a unique widget_id."""
        self.widgets[widget_id] = widget  # Store widget with its ID

    def get_widget_value(self, widget_id):
        """Retrieve the value of a specified widget."""
        return self.widgets[widget_id].get_value()  # Get the value from the widget

    def set_widget_value(self, widget_id, value):
        """Set the value of a specified widget."""
        return self.widgets[widget_id].set_value(value)  # Set the value in the widget

    def remove_widget(self, widget_id):
        """Remove a widget from the window using its widget_id."""
        del self.widgets[widget_id]  # Delete the widget from the dictionary

    def set_widget_visibility(self, widget_id, visible):
        """Set the visibility of a widget."""
        if widget_id in self.widgets:
            self.widgets[widget_id].visible = visible  # Update visibility of the widget

    def render(self):
        """Render all widgets in the window."""
        for widget in self.widgets.values():
            widget.render(self.screen)  # Render each widget on the screen

    def update(self, event):
        """Update all widgets based on the received event."""
        for widget in self.widgets.values():
            widget.update(event)  # Update each widget with the event


class Box:
    def __init__(self, rect):
        """Initialize a Box with a given rectangle."""
        self.isActive = False  # State of the box
        self.rect = pygame.Rect(rect)  # Create a rectangle for the box

    def update(self, event):
        """Update the box's state based on mouse position and events."""
        self.mousePos = pygame.mouse.get_pos()  # Get current mouse position
        self.clicked = event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(self.mousePos)  # Check if clicked
        self.hovered = self.rect.collidepoint(self.mousePos)  # Check if hovered


class Button(Box):
    def __init__(self, rect, text_or_image, color_or_hover_image, hover_color=None):
        """Initialize a Button with a rectangle, text or image, and colors."""
        super().__init__(rect)  # Initialize the base class
        self.is_image_button = isinstance(text_or_image, str) and text_or_image.endswith(('.png', '.jpg', '.bmp'))  # Check if it's an image button
        
        if self.is_image_button:
            # Load images for the button
            self.image = pygame.image.load(text_or_image)  # Load normal image
            self.hover_image = pygame.image.load(color_or_hover_image)  # Load hover image
        else:
            # Set text and colors for the button
            self.text = text_or_image  # Set button text
            self.color = color_or_hover_image  # Set button color
            self.hover_color = hover_color  # Set hover color
        
        self.active = False  # Button state
        self.font = pygame.font.SysFont('Arial', 20)  # Font for rendering text

    def render(self, screen):
        """Render the button on the screen."""
        if self.is_image_button:
            # Use hover image if hovered, otherwise use normal image
            image = self.hover_image if self.hovered else self.image  # Select image based on hover state
            screen.blit(image, self.rect)  # Draw the image on the screen
        else:
            # Draw the button rectangle and text
            color = self.hover_color if self.hovered else self.color  # Select color based on hover state
            pygame.draw.rect(screen, color, self.rect)  # Draw button rectangle
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Draw border
            text_surf = self.font.render(self.text, True, (0, 0, 0))  # Render button text
            text_rect = text_surf.get_rect(center=self.rect.center)  # Center the text
            screen.blit(text_surf, text_rect)  # Draw the text on the screen

    def update(self, event):
        """Update the button's state based on events."""
        super().update(event)  # Update the base class
        if self.clicked:
            # Toggle the button's active state when clicked
            self.active = not self.active  # Change active state

    def get_value(self):
        """Return the active state of the button."""
        return self.active  # Return the active state

    def set_value(self, value):
        """Set the active state of the button."""
        self.active = value  # Update the active state


class OutputBox(Box):
    def __init__(self, rect, label, color, font, initial_text=''):
        """Initialize an OutputBox with a rectangle, label, color, font, and initial text."""
        super().__init__(rect)  # Initialize the base class
        self.label = label  # Set the label
        self.color = color  # Set the color
        self.font = font  # Set the font
        self.text = initial_text  # The initial text or output

    def render(self, screen):
        """Render the output box on the screen."""
        # Draw the label
        label_surface = self.font.render(self.label, True, self.color)  # Render the label
        screen.blit(label_surface, (self.rect.x + (self.rect.w - label_surface.get_width()) / 2, self.rect.y - 32))  # Center the label

        # Draw the text inside the box
        text_surface = self.font.render(self.text, True, self.color)  # Render the text
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))  # Center the text

        # Draw the box outline
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Draw the box outline

    def update(self, event):
        """OutputBox doesn't interact with input, so no need to handle input events."""
        pass  # No update needed for OutputBox

    def set_value(self, value):
        """Set the text to display in the output box."""
        self.text = value  # Update the displayed text

    def get_value(self):
        """Get the current text in the output box."""
        return self.text  # Return the current text


class InputBox(ABC, Box):
    def __init__(self, rect, label, color, font):
        """Initialize an InputBox with a rectangle, label, color, and font."""
        super().__init__(rect)  # Initialize the base class
        self.label = label  # Set the label
        self.color = color  # Set the color
        self.font = font  # Set the font

    def render(self, screen):
        """Render the input box and its label on the screen."""
        label = self.font.render(self.label, True, self.color)  # Render the label
        screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))  # Center the label
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Draw the input box

    @abstractmethod
    def get_value(self):
        """Abstract method to get the value from the input box."""
        pass  # To be implemented by subclasses

    @abstractmethod
    def set_value(self, value):
        """Abstract method to set the value in the input box."""
        pass  # To be implemented by subclasses

class TextBox(InputBox):
    def __init__(self, rect, label, color, font, text):
        """Initialize a TextBox with a rectangle, label, color, font, and initial text."""
        super().__init__(rect, label, color, font)  # Initialize the base class
        self.text = text  # Set the initial text
        self.active = False  # State of the text box
        self.background_color = (250, 250, 250)  # White background
        self.active_color = (255, 0, 0)  # Red border when active
        self.selected = False  # Selection state

    def render(self, screen):
        """Render the text box on the screen."""
        super().render(screen)  # Render the base class
        # Draw the background
        pygame.draw.rect(screen, self.background_color, self.rect)  # Draw the background
        # Draw the border
        border_color = self.active_color if self.active else self.color  # Select border color based on active state
        pygame.draw.rect(screen, border_color, self.rect, 2)  # Draw the border
        # Render the text
        text_to_render = self.text if self.text else "0"  # Default to "0" if no text
        text_surface = self.font.render(text_to_render, True, self.color)  # Render the text
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Draw the text
        # Draw selection highlight
        if self.selected:
            text_width, _ = self.font.size(text_to_render)  # Get text width
            highlight_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, text_width, self.rect.height - 10)  # Create highlight rectangle
            pygame.draw.rect(screen, (0, 120, 215), highlight_rect)  # Light blue highlight
            text_surface = self.font.render(text_to_render, True, self.background_color)  # Render text in background color
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Draw highlighted text

    def handle_event(self, event):
        """Handle events for the text box, including mouse and keyboard input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True  # Activate the text box
                self.selected = True  # Mark as selected
            else:
                self.active = False  # Deactivate if clicked outside
                self.selected = False  # Deselect
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False  # Deactivate on return
                    self.selected = False  # Deselect
                elif event.key == pygame.K_BACKSPACE:
                    if self.selected:
                        self.text = ""  # Clear text if selected
                        self.selected = False  # Deselect
                    else:
                        self.text = self.text[:-1]  # Remove last character
                elif event.unicode.isdigit():
                    if self.selected:
                        self.text = event.unicode  # Replace text if selected
                        self.selected = False  # Deselect
                    else:
                        self.text += event.unicode  # Append digit to text
        return self.active  # Return active state

    def get_value(self):
        """Return the current text in the text box."""
        return self.text if self.text else "0"  # Return text or "0"

    def set_value(self, value):
        """Set the text in the text box."""
        self.text = str(value)  # Update text


class SlideBox(InputBox):
    def __init__(self, rect, label, color, font):
        """Initialize a SlideBox with a rectangle, label, color, and font."""
        super().__init__(rect, label, color, font)  # Initialize the base class
        self.start = self.rect.x + 6  # Starting position for the slider
        self.end = self.rect.x + self.rect.w - 6  # Ending position for the slider
        self.value = self.start  # Initial value

    def render(self, screen):
        """Render the slide box on the screen."""
        super().render(screen)  # Render the base class
        pygame.draw.line(screen, self.color, (self.start, self.rect.y + 25), (self.end, self.rect.y + 25), 2)  # Draw slider line
        pygame.draw.line(screen, self.color, (self.value, self.rect.y + 5), (self.value, self.rect.y + 45), 12)  # Draw slider handle

    def update(self, event):
        """Update the slide box's state based on events."""
        super().update(event)  # Update the base class
        previousStart = self.start  # Store previous start position
        self.start = self.rect.x + 6  # Update start position
        self.end = self.rect.x + self.rect.w - 6  # Update end position
        self.value += self.start - previousStart  # Adjust value based on position change

        if self.clicked:
            if self.start <= self.mousePos[0] <= self.end:
                self.value = self.mousePos[0]  # Set value to mouse position

    def get_value(self):
        """Return the current value of the slide box."""
        return self.value  # Return the current value

    def set_value(self, value):
        """Set the value of the slide box."""
        self.value = value  # Update the value

class DropdownBox(InputBox):
    """DropdownBox allows for multiple selections from a list of options."""
    VISIBLE_OPTIONS = 5  # Number of options visible at once

    def __init__(self, rect, label, color, font, options, options_background_color):
        """Initialize a DropdownBox with a rectangle, label, color, font, options, and background color."""
        super().__init__(rect, label, color, font)  # Initialize the base class
        self.openDropdown = False  # State of the dropdown (open or closed)
        self.options = options  # List of options to select from
        self.options_background_color = options_background_color  # Background color of the dropdown
        self.selected_options = set()  # Use a set to store multiple selections

        # Define the rectangle for the dropdown options
        self.dropdown_rect = pygame.Rect(
            self.rect.x,
            self.rect.y - self.rect.height * self.VISIBLE_OPTIONS,
            self.rect.width,
            self.rect.height * self.VISIBLE_OPTIONS
        )
        self.scroll_offset = 0  # Current scroll position
        self.scrollbar_width = 5  # Width of the scrollbar

    def render(self, screen):
        """Render the dropdown box and its options on the screen."""
        super().render(screen)  # Render the base class

        # Render the selected options in the input box
        selected_text = ", ".join(self.get_value()) if self.selected_options else "Select algorithms"  # Get selected text
        # Truncate the text if it's too long
        max_width = self.rect.width - 20  # Leave some padding
        while self.font.size(selected_text)[0] > max_width and len(selected_text) > 3:
            selected_text = selected_text[:-4] + "..."  # Truncate text
        option_text = self.font.render(selected_text, True, self.color)  # Render selected text
        screen.blit(option_text, option_text.get_rect(center=self.rect.center))  # Draw selected text

        if self.openDropdown:
            # Render the dropdown background
            pygame.draw.rect(screen, self.options_background_color, self.dropdown_rect)  # Draw dropdown background
            pygame.draw.rect(screen, self.color, self.dropdown_rect, 2)  # Draw dropdown border

            # Render visible options with scrolling
            start_index = self.scroll_offset  # Start index for visible options
            end_index = min(start_index + self.VISIBLE_OPTIONS, len(self.options))  # End index for visible options

            for index in range(start_index, end_index):
                rect = self.rect.copy()  # Copy the input box rectangle
                rect.y = self.rect.y - (index - start_index + 1) * self.rect.height  # Position for each option

                pygame.draw.rect(screen, self.options_background_color, rect)  # Draw option background
                pygame.draw.rect(screen, self.color, rect, 1)  # Draw option border
                option_text = self.font.render(self.options[index], 1, self.color)  # Render option text
                screen.blit(option_text, option_text.get_rect(center=rect.center))  # Draw option text

            # Render the scrollbar
            self.render_scrollbar(screen)  # Draw scrollbar

    def render_scrollbar(self, screen):
        """Render the scrollbar for the dropdown options."""
        total_options = len(self.options)  # Total number of options
        if total_options > self.VISIBLE_OPTIONS:
            proportion_visible = self.VISIBLE_OPTIONS / total_options  # Calculate visible proportion
            scrollbar_height = int(self.dropdown_rect.height * proportion_visible)  # Calculate scrollbar height

            max_scroll = total_options - self.VISIBLE_OPTIONS  # Maximum scroll value
            proportion_scrolled = self.scroll_offset / max_scroll if max_scroll > 0 else 0  # Calculate scroll position
            scrollbar_rect = pygame.Rect(self.dropdown_rect.right - self.scrollbar_width,
                                         self.dropdown_rect.y + proportion_scrolled * (self.dropdown_rect.height - scrollbar_height),
                                         self.scrollbar_width, scrollbar_height)  # Create scrollbar rectangle

            # Draw the scrollbar (visual only)
            pygame.draw.rect(screen, self.color, scrollbar_rect)  # Draw scrollbar

    def update(self, event):
        """Update the dropdown box's state based on events."""
        super().update(event)  # Update the base class

        # Toggle the dropdown when the input box is clicked
        if self.clicked:
            self.openDropdown = not self.openDropdown  # Toggle dropdown state

        if self.openDropdown:
            # Handle mouse wheel scrolling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.scroll_offset = max(self.scroll_offset - 1, 0)  # Decrease scroll offset
                elif event.button == 5:  # Scroll down
                    self.scroll_offset = min(self.scroll_offset + 1, len(self.options) - self.VISIBLE_OPTIONS)  # Increase scroll offset

            # Handle option selection
            self.handle_option_selection(event)  # Process option selection

    def handle_option_selection(self, event):
        """Handle the selection of options in the dropdown."""
        start_index = self.scroll_offset  # Start index for visible options
        for index in range(start_index, min(start_index + self.VISIBLE_OPTIONS, len(self.options))):
            rect = self.rect.copy()  # Copy the input box rectangle
            rect.y = self.rect.y - (index - start_index + 1) * self.rect.height  # Position for each option

            if rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if index in self.selected_options:
                    self.selected_options.remove(index)  # Deselect if already selected
                else:
                    self.selected_options.add(index)  # Select the option
                # Close the dropdown after selection
                self.openDropdown = False  # Close dropdown

    def get_value(self):
        """Return the selected options from the dropdown."""
        return [self.options[i] for i in self.selected_options]  # Return selected options

    def set_value(self, value):
        """Set the selected options in the dropdown."""
        self.selected_options = set(value)  # Update selected options

class AlgorithmSelectionPopup:
    def __init__(self, screen, algorithms):
        """Initialize the AlgorithmSelectionPopup with a screen and a list of algorithms."""
        self.screen = screen  # Set the screen
        self.algorithms = algorithms  # List of algorithms
        self.selected = set()  # Store selected algorithms
        self.font = pygame.font.SysFont('Arial', 20)  # Font for rendering text
        self.is_open = False  # State of the popup (open or closed)
        self.rect = pygame.Rect(200, 100, 400, 300)  # Rectangle for the popup
        self.checkboxes = [pygame.Rect(210, 110 + i*30, 20, 20) for i in range(len(algorithms))]  # Checkboxes for algorithms
        self.linear_search_index = self.algorithms.index('linear_search') if 'linear_search' in self.algorithms else -1  # Index for linear search

    def toggle(self):
        """Toggle the visibility of the popup."""
        self.is_open = not self.is_open  # Change open state

    def handle_event(self, event):
        """Handle events for the popup, including checkbox selection."""
        if not self.is_open or event.type != pygame.MOUSEBUTTONDOWN:
            return  # Exit if popup is closed or not a mouse click
        pos = pygame.mouse.get_pos()  # Get mouse position
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.collidepoint(pos):
                if i == self.linear_search_index:
                    if i in self.selected:
                        self.selected.remove(i)  # Deselect linear search
                    else:
                        self.selected = {i}  # Select only linear search, deselect others
                else:
                    if i in self.selected:
                        self.selected.remove(i)  # Deselect the algorithm
                    else:
                        self.selected.add(i)  # Select the algorithm
                        if self.linear_search_index in self.selected:
                            self.selected.remove(self.linear_search_index)  # Deselect linear search
                break  # Exit loop after handling selection

    def render(self):
        """Render the popup and its checkboxes on the screen."""
        if not self.is_open:
            return  # Exit if popup is closed
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect)  # Draw popup background
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)  # Draw popup border
        for i, (checkbox, algorithm) in enumerate(zip(self.checkboxes, self.algorithms)):
            pygame.draw.rect(self.screen, (0, 0, 0), checkbox, 2)  # Draw checkbox border
            if i in self.selected:
                pygame.draw.rect(self.screen, (0, 0, 0), checkbox.inflate(-4, -4))  # Draw filled checkbox
            text = self.font.render(algorithm, True, (0, 0, 0))  # Render algorithm text
            self.screen.blit(text, (checkbox.right + 10, checkbox.top))  # Position text next to checkbox

    def get_selected_algorithms(self):
        """Return the list of selected algorithms."""
        return [self.algorithms[i] for i in self.selected]  # Return selected algorithms

    def is_linear_search_selected(self):
        """Check if linear search is selected."""
        return self.linear_search_index in self.selected  # Check if linear search is selected

class RadioButton(InputBox):
    def __init__(self, rect, label, color, font, options):
        """Initialize a RadioButton with a rectangle, label, color, font, and options."""
        # Convert tuple to Rect if necessary
        if isinstance(rect, tuple):
            rect = pygame.Rect(*rect)  # Create a Rect from tuple
        super().__init__(rect, label, color, font)  # Initialize the base class
        self.options = options  # List of options for the radio button
        self.selected = None  # Currently selected option
        self.buttons = [pygame.Rect(rect.x, rect.y + i*30, 20, 20) for i in range(len(options))]  # Rectangles for buttons

    def render(self, screen):
        """Render the radio buttons and their labels on the screen."""
        super().render(screen)  # Render the base class
        for i, (button, option) in enumerate(zip(self.buttons, self.options)):
            pygame.draw.rect(screen, self.color, button, 2)  # Draw button border
            if self.selected == i:
                pygame.draw.rect(screen, self.color, button.inflate(-4, -4))  # Draw filled button for selected option
            text = self.font.render(option, True, self.color)  # Render option text
            screen.blit(text, (button.right + 10, button.top))  # Position text next to button

    def update(self, event):
        """Update the radio button's state based on events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.collidepoint(event.pos):
                    self.selected = i  # Set selected option
                    break  # Exit loop after selection

    def get_value(self):
        """Return the currently selected option."""
        return self.options[self.selected] if self.selected is not None else None  # Return selected option or None

    def set_value(self, value):
        """Set the selected option based on the provided value."""
        if value in self.options:
            self.selected = self.options.index(value)  # Update selected option