# File for building classes for all our GUI tools
import pygame, sys
from abc import ABC, abstractmethod  # Abstract base classes, help to make different shapes
from pygame.color import THECOLORS

class Window:
    def __init__(self, screen):
        """Initialize the Window with a screen and an empty widget dictionary."""
        self.screen = screen
        self.widgets = {}

    def add_widget(self, widget_id, widget):
        """Add a widget to the window using a unique widget_id."""
        self.widgets[widget_id] = widget

    def get_widget_value(self, widget_id):
        """Retrieve the value of a specified widget."""
        return self.widgets[widget_id].get_value()

    def set_widget_value(self, widget_id, value):
        """Set the value of a specified widget."""
        return self.widgets[widget_id].set_value(value)

    def remove_widget(self, widget_id):
        """Remove a widget from the window using its widget_id."""
        del self.widgets[widget_id]

    def set_widget_visibility(self, widget_id, visible):
        """Set the visibility of a widget."""
        if widget_id in self.widgets:
            self.widgets[widget_id].visible = visible

    def render(self):
        """Render all widgets in the window."""
        for widget in self.widgets.values():
            widget.render(self.screen)

    def update(self, event):
        """Update all widgets based on the received event."""
        for widget in self.widgets.values():
            widget.update(event)


class Box:
    def __init__(self, rect):
        """Initialize a Box with a given rectangle."""
        self.isActive = False
        self.rect = pygame.Rect(rect)

    def update(self, event):
        """Update the box's state based on mouse position and events."""
        self.mousePos = pygame.mouse.get_pos()
        self.clicked = event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(self.mousePos)
        self.hovered = self.rect.collidepoint(self.mousePos)


class Button(Box):
    def __init__(self, rect, text_or_image, color_or_hover_image, hover_color=None):
        """Initialize a Button with a rectangle, text or image, and colors."""
        super().__init__(rect)
        self.is_image_button = isinstance(text_or_image, str) and text_or_image.endswith(('.png', '.jpg', '.bmp'))
        
        if self.is_image_button:
            # Load images for the button
            self.image = pygame.image.load(text_or_image)
            self.hover_image = pygame.image.load(color_or_hover_image)
        else:
            # Set text and colors for the button
            self.text = text_or_image
            self.color = color_or_hover_image
            self.hover_color = hover_color
        
        self.active = False
        self.font = pygame.font.SysFont('Arial', 20)

    def render(self, screen):
        """Render the button on the screen."""
        if self.is_image_button:
            # Use hover image if hovered, otherwise use normal image
            image = self.hover_image if self.hovered else self.image
            screen.blit(image, self.rect)
        else:
            # Draw the button rectangle and text
            color = self.hover_color if self.hovered else self.color
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Draw border
            text_surf = self.font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def update(self, event):
        """Update the button's state based on events."""
        super().update(event)
        if self.clicked:
            # Toggle the button's active state when clicked
            self.active = not self.active

    def get_value(self):
        """Return the active state of the button."""
        return self.active

    def set_value(self, value):
        """Set the active state of the button."""
        self.active = value


class OutputBox(Box):
    def __init__(self, rect, label, color, font, initial_text=''):
        """Initialize an OutputBox with a rectangle, label, color, font, and initial text."""
        super().__init__(rect)
        self.label = label
        self.color = color
        self.font = font
        self.text = initial_text  # The initial text or output

    def render(self, screen):
        """Render the output box on the screen."""
        # Draw the label
        label_surface = self.font.render(self.label, True, self.color)
        screen.blit(label_surface, (self.rect.x + (self.rect.w - label_surface.get_width()) / 2, self.rect.y - 32))

        # Draw the text inside the box
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

        # Draw the box outline
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self, event):
        """OutputBox doesn't interact with input, so no need to handle input events."""
        pass

    def set_value(self, value):
        """Set the text to display in the output box."""
        self.text = value

    def get_value(self):
        """Get the current text in the output box."""
        return self.text


class InputBox(ABC, Box):
    def __init__(self, rect, label, color, font):
        """Initialize an InputBox with a rectangle, label, color, and font."""
        super().__init__(rect)
        self.label = label
        self.color = color
        self.font = font

    def render(self, screen):
        """Render the input box and its label on the screen."""
        label = self.font.render(self.label, True, self.color)
        screen.blit(label, (self.rect.x + (self.rect.w - label.get_width()) / 2, self.rect.y - 32))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    @abstractmethod
    def get_value(self):
        """Abstract method to get the value from the input box."""
        pass

    @abstractmethod
    def set_value(self, value):
        """Abstract method to set the value in the input box."""
        pass

class TextBox(InputBox):
    def __init__(self, rect, label, color, font, text):
        """Initialize a TextBox with a rectangle, label, color, font, and initial text."""
        super().__init__(rect, label, color, font)
        self.text = text
        self.active = False
        self.background_color = (250, 250, 250)  # White
        self.active_color = (255, 0, 0)  # Red
        self.selected = False

    def render(self, screen):
        """Render the text box on the screen."""
        super().render(screen)
        # Draw the background
        pygame.draw.rect(screen, self.background_color, self.rect)
        # Draw the border
        border_color = self.active_color if self.active else self.color
        pygame.draw.rect(screen, border_color, self.rect, 2)
        # Render the text
        text_to_render = self.text if self.text else "0"
        text_surface = self.font.render(text_to_render, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw selection highlight
        if self.selected:
            text_width, _ = self.font.size(text_to_render)
            highlight_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, text_width, self.rect.height - 10)
            pygame.draw.rect(screen, (0, 120, 215), highlight_rect)  # Light blue highlight
            text_surface = self.font.render(text_to_render, True, self.background_color)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        """Handle events for the text box, including mouse and keyboard input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.selected = True
            else:
                self.active = False
                self.selected = False
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.selected = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.selected:
                        self.text = ""
                        self.selected = False
                    else:
                        self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    if self.selected:
                        self.text = event.unicode
                        self.selected = False
                    else:
                        self.text += event.unicode
        return self.active

    def get_value(self):
        """Return the current text in the text box."""
        return self.text if self.text else "0"

    def set_value(self, value):
        """Set the text in the text box."""
        self.text = str(value)


class SlideBox(InputBox):
    def __init__(self, rect, label, color, font):
        """Initialize a SlideBox with a rectangle, label, color, and font."""
        super().__init__(rect, label, color, font)
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value = self.start

    def render(self, screen):
        """Render the slide box on the screen."""
        super().render(screen)
        pygame.draw.line(screen, self.color, (self.start, self.rect.y + 25), (self.end, self.rect.y + 25), 2)
        pygame.draw.line(screen, self.color, (self.value, self.rect.y + 5), (self.value, self.rect.y + 45), 12)

    def update(self, event):
        """Update the slide box's state based on events."""
        super().update(event)
        previousStart = self.start
        self.start = self.rect.x + 6
        self.end = self.rect.x + self.rect.w - 6
        self.value += self.start - previousStart

        if self.clicked:
            if self.start <= self.mousePos[0] <= self.end:
                self.value = self.mousePos[0]

    def get_value(self):
        """Return the current value of the slide box."""
        return self.value

    def set_value(self, value):
        """Set the value of the slide box."""
        self.value = value

class DropdownBox(InputBox):
    """DropdownBox allows for multiple selections from a list of options."""
    VISIBLE_OPTIONS = 5  # Number of options visible at once

    def __init__(self, rect, label, color, font, options, options_background_color):
        """Initialize a DropdownBox with a rectangle, label, color, font, options, and background color."""
        super().__init__(rect, label, color, font)
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
        super().render(screen)

        # Render the selected options in the input box
        selected_text = ", ".join(self.get_value()) if self.selected_options else "Select algorithms"
        # Truncate the text if it's too long
        max_width = self.rect.width - 20  # Leave some padding
        while self.font.size(selected_text)[0] > max_width and len(selected_text) > 3:
            selected_text = selected_text[:-4] + "..."
        option_text = self.font.render(selected_text, True, self.color)
        screen.blit(option_text, option_text.get_rect(center=self.rect.center))

        if self.openDropdown:
            # Render the dropdown background
            pygame.draw.rect(screen, self.options_background_color, self.dropdown_rect)
            pygame.draw.rect(screen, self.color, self.dropdown_rect, 2)

            # Render visible options with scrolling
            start_index = self.scroll_offset
            end_index = min(start_index + self.VISIBLE_OPTIONS, len(self.options))

            for index in range(start_index, end_index):
                rect = self.rect.copy()
                rect.y = self.rect.y - (index - start_index + 1) * self.rect.height

                pygame.draw.rect(screen, self.options_background_color, rect)
                pygame.draw.rect(screen, self.color, rect, 1)
                option_text = self.font.render(self.options[index], 1, self.color)
                screen.blit(option_text, option_text.get_rect(center=rect.center))

            # Render the scrollbar
            self.render_scrollbar(screen)

    def render_scrollbar(self, screen):
        """Render the scrollbar for the dropdown options."""
        total_options = len(self.options)
        if total_options > self.VISIBLE_OPTIONS:
            proportion_visible = self.VISIBLE_OPTIONS / total_options
            scrollbar_height = int(self.dropdown_rect.height * proportion_visible)

            max_scroll = total_options - self.VISIBLE_OPTIONS
            proportion_scrolled = self.scroll_offset / max_scroll if max_scroll > 0 else 0
            scrollbar_rect = pygame.Rect(self.dropdown_rect.right - self.scrollbar_width,
                                         self.dropdown_rect.y + proportion_scrolled * (self.dropdown_rect.height - scrollbar_height),
                                         self.scrollbar_width, scrollbar_height)

            # Draw the scrollbar (visual only)
            pygame.draw.rect(screen, self.color, scrollbar_rect)

    def update(self, event):
        """Update the dropdown box's state based on events."""
        super().update(event)

        # Toggle the dropdown when the input box is clicked
        if self.clicked:
            self.openDropdown = not self.openDropdown

        if self.openDropdown:
            # Handle mouse wheel scrolling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.scroll_offset = max(self.scroll_offset - 1, 0)
                elif event.button == 5:  # Scroll down
                    self.scroll_offset = min(self.scroll_offset + 1, len(self.options) - self.VISIBLE_OPTIONS)

            # Handle option selection
            self.handle_option_selection(event)

    def handle_option_selection(self, event):
        """Handle the selection of options in the dropdown."""
        start_index = self.scroll_offset
        for index in range(start_index, min(start_index + self.VISIBLE_OPTIONS, len(self.options))):
            rect = self.rect.copy()
            rect.y = self.rect.y - (index - start_index + 1) * self.rect.height

            if rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if index in self.selected_options:
                    self.selected_options.remove(index)  # Deselect if already selected
                else:
                    self.selected_options.add(index)  # Select the option
                # Close the dropdown after selection
                self.openDropdown = False

    def get_value(self):
        """Return the selected options from the dropdown."""
        return [self.options[i] for i in self.selected_options]

    def set_value(self, value):
        """Set the selected options in the dropdown."""
        self.selected_options = set(value)

class AlgorithmSelectionPopup:
    def __init__(self, screen, algorithms):
        """Initialize the AlgorithmSelectionPopup with a screen and a list of algorithms."""
        self.screen = screen
        self.algorithms = algorithms
        self.selected = set()  # Store selected algorithms
        self.font = pygame.font.SysFont('Arial', 20)  # Font for rendering text
        self.is_open = False  # State of the popup (open or closed)
        self.rect = pygame.Rect(200, 100, 400, 300)  # Rectangle for the popup
        self.checkboxes = [pygame.Rect(210, 110 + i*30, 20, 20) for i in range(len(algorithms))]  # Checkboxes for algorithms

    def toggle(self):
        """Toggle the visibility of the popup."""
        self.is_open = not self.is_open

    def handle_event(self, event):
        """Handle events for the popup, including checkbox selection."""
        if not self.is_open or event.type != pygame.MOUSEBUTTONDOWN:
            return
        pos = pygame.mouse.get_pos()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.collidepoint(pos):
                if i in self.selected:
                    self.selected.remove(i)  # Deselect if already selected
                else:
                    self.selected.add(i)  # Select the checkbox
                break

    def render(self):
        """Render the popup and its checkboxes on the screen."""
        if not self.is_open:
            return
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
        return [self.algorithms[i] for i in self.selected]

class RadioButton(InputBox):
    def __init__(self, rect, label, color, font, options):
        """Initialize a RadioButton with a rectangle, label, color, font, and options."""
        # Convert tuple to Rect if necessary
        if isinstance(rect, tuple):
            rect = pygame.Rect(*rect)
        super().__init__(rect, label, color, font)
        self.options = options  # List of options for the radio button
        self.selected = None  # Currently selected option
        self.buttons = [pygame.Rect(rect.x, rect.y + i*30, 20, 20) for i in range(len(options))]  # Rectangles for buttons

    def render(self, screen):
        """Render the radio buttons and their labels on the screen."""
        super().render(screen)
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
                    break

    def get_value(self):
        """Return the currently selected option."""
        return self.options[self.selected] if self.selected is not None else None

    def set_value(self, value):
        """Set the selected option based on the provided value."""
        if value in self.options:
            self.selected = self.options.index(value)