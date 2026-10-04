# Import sqrt so the calculator can calculate square roots
from math import sqrt
# NiceGUI provides the web-based graphical user interface components.
from nicegui import ui
# simple_eval safely evaluates the mathematical expression entered by the user.
from simpleeval import simple_eval


class Calculator:
    # Initialize the calculator's display, memory, and default state.
    def __init__(self):
        self.data = '0'       # Current expression/result shown in the calculator.
        self.memory = ''      # Stores a value for the calculator memory functions.
        self.default = True   # True means the display is still showing the initial 0.
        self.setup_gui()      # Build the calculator interface.

    # Add a number or operator to the current expression.
    def add_data(self, data_to_add) -> None:
        # Prevent two operators such as "*" followed by "/" from being entered together.
        if all(x in ['*', '/', '%'] for x in [self.data[-1], data_to_add]):
            return

        # If this is the first value entered, replace the initial 0.
        elif self.default:
            self.data = self.data.replace('0', data_to_add)
            self.default = False

        # Otherwise append the new character to the existing expression.
        else:
            self.data += data_to_add
# Remove either the last character (C) or the entire expression (CE).
    def remove_data(self, remove_all) -> None:
        # If CE is selected, or only one character remains, reset to 0.
        if remove_all or len(self.data) <= 1:
            self.data = '0'
            self.default = True

        # Otherwise remove only the last character.
        else:
            self.data = self.data[:-1]

    # Evaluate the mathematical expression currently in the display.
    def calculate(self):
        try:
            # simple_eval evaluates the expression and round keeps the result
            # to a maximum of seven decimal places.
            self.data = str(round(simple_eval(self.data), 7))

        # Show a message when the expression has invalid syntax.
        except SyntaxError:
            ui.notify('The operation is not possible')

        # Catch other calculation errors and display the error message.
        except Exception as error:
            ui.notify(f'error {error}')

# Calculate the square root of the current value.
    def calculate_sqrt(self):
        # First evaluate the current expression.
        self.calculate()

        # Convert the result to a number, calculate its square root,
        # and convert the answer back to text for the display.
        self.data = str(round(sqrt(float(self.data)), 7))

    # Clear the calculator memory.
    def memory_clear(self):
        self.memory = ''

    # Recall the value stored in memory and add it to the display.
    def memory_recall(self):
        if self.memory:
            self.add_data(self.memory)

    # Add or subtract the current display value from calculator memory.
    def memory_modify(self, operation):
        # Print the current memory value for debugging.
        print(self.memory)

        if self.memory:
            # Apply the selected operation to the existing memory value.
            self.memory = str(simple_eval(
                f'{self.memory} {operation} {self.data}'))
        else:
            # If memory is empty, start from 0.
            self.memory = str(simple_eval(f'0 {operation} {self.data}'))

        # An empty memory is represented by an empty string rather than "0".
        if self.memory == '0':
            self.memory = ''
# Create the visual calculator interface.
    def setup_gui(self) -> None:
        # Put the calculator inside a card and center it on the page.
        with ui.card().classes('flex mx-auto mt-40'):

            # Show a memory icon only when a value is stored in memory.
            ui.icon('sim_card', color='primary').bind_visibility_from(
                self, 'memory')

            # Create the display/input field and bind it to self.data.
            # The Tailwind call from the original code was commented out
            # because it may cause an installation/configuration error.
            ui.input().bind_value(self, 'data').props(
                'outlined input-style="text-align:right"')
            # .tailwind('min-w-full')

            # Arrange calculator buttons in a five-column grid.
            with ui.grid(columns=5):
# Square-root and memory controls.
                ui.button('√', on_click=self.calculate_sqrt)
                ui.button('MC', on_click=self.memory_clear)
                ui.button('MR', on_click=self.memory_recall)
                ui.button('M-', on_click=lambda: self.memory_modify('-'))
                ui.button('M+', on_click=lambda: self.memory_modify('+'))

                # Percentage, number, and division buttons.
                ui.button('%', on_click=lambda: self.add_data('%'))
                ui.button('7', on_click=lambda: self.add_data('7'))
                ui.button('8', on_click=lambda: self.add_data('8'))
                ui.button('9', on_click=lambda: self.add_data('9'))
                ui.button('/', on_click=lambda: self.add_data('/'))

                # The ± button is implemented by adding a minus sign.
                ui.button('±', on_click=lambda: self.add_data('-'))
                ui.button('4', on_click=lambda: self.add_data('4'))
                ui.button('5', on_click=lambda: self.add_data('5'))
                ui.button('6', on_click=lambda: self.add_data('6'))
                ui.button('*', on_click=lambda: self.add_data('*'))

                # Clear, number, and subtraction buttons.
                ui.button('C', on_click=lambda: self.remove_data(False))
                ui.button('1', on_click=lambda: self.add_data('1'))
                ui.button('2', on_click=lambda: self.add_data('2'))
                ui.button('3', on_click=lambda: self.add_data('3'))
                ui.button('-', on_click=lambda: self.add_data('-'))
    # CE clears the complete expression; 0 and decimal are
                # used to enter decimal numbers; = performs the calculation.
                ui.button('CE', on_click=lambda: self.remove_data(True))
                ui.button('0', on_click=lambda: self.add_data('0'))
                ui.button('·', on_click=lambda: self.add_data('.'))
                ui.button('=', on_click=self.calculate)
                ui.button('+', on_click=lambda: self.add_data('+'))


# Create an instance of the Calculator class, which also builds the GUI.
calculator = Calculator()

# Start the NiceGUI web application with the calculator title and light theme.
ui.run(title='Calculator', dark=False)

                
