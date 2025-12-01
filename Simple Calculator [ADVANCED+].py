# =========================================== #
# John Daniel's Simple Calculator [ADVANCED+]
# 11/25-30/11/25 (forgot when i started)
# =========================================== #

# === MODULES === #
import sys
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor
from pynput import keyboard
import darkdetect
# =============== #

# === STYLE SHEET READING === #
def get_stylesheet(app):
    """Reads a stylesheet based off of the user's system theme."""
    script_path = Path(sys.argv[0]).resolve()
    # gets the path of the script as an absolute path.
    script_dir = script_path.parent
    # sets the location of the script to the parent of it, which would
    # be its location.
    light_qss = "light.qss"
    dark_qss = "dark.qss"
    
    theme = None

    if darkdetect.isLight():
        theme = script_dir / light_qss
        # if darkdetect detects the user's system theme as light, the
        # code will read the light style sheet, likewise for if the
        # system theme is dark.
    elif darkdetect.isDark():
        theme = script_dir / dark_qss
    else:
        print("no theme found!")
    
    if theme:
        # means if a theme is found (if theme = None this will not run.)
        try:
            with open(theme, "r") as file:
                app.setStyleSheet(file.read())
                # opens the style sheet and reads it, sets it as the
                # application's style sheet.
                print(f"loaded stylesheet from: {theme}")
            
        except FileNotFoundError:
            print(f"file not found at {theme}")
            # if no sheet is found, it will print a message, likewise
            # if another error occurs.
        except Exception as error:
            print(f"unexpected error occurred: {error}")
# =========================== #

# === GLOBAL VARIABLE === #
app = QApplication([])
# ======================= #

get_stylesheet(app)

# === CALCULATOR CLASS === #
class CalculatorApp:
    """
    A calculator application built using PySide6.
    """
    def __init__(self):
        """
        Makes the main window and defines the state variables of the
        application.
        """
        self._currently_typed = ""
        self._full_expression = ""
        self._can_input_operator = True
        self.button_effects = []
        # a container is needed to hold all of the drop shadows that the
        # buttons have.
        self.buttons = [
            # - order of info: - #
            # - text, value, key, row, column, row span, column span - #
            # - row 1 (bottom) - #
            ("0", "0", "0", 5, 0, 1, 2),
            (".", ".", ".", 5, 2, 1, 1),
            ("=", "=", keyboard.Key.enter, 5, 3, 1, 2),
            # - row 2 - #
            ("1", "1", "1", 4, 0, 1, 1),
            ("2", "2", "2", 4, 1, 1, 1),
            ("3", "3", "3", 4, 2, 1, 1),
            ("+", "+", "a", 4, 3, 1, 1),
            ("-", "-", "s", 4, 4, 1, 1),
            # - row 3 - #
            ("4", "4", "4", 3, 0, 1, 1),
            ("5", "5", "5", 3, 1, 1, 1),
            ("6", "6", "6", 3, 2, 1, 1),
            ("×", "*", "x", 3, 3, 1, 1),
            ("÷", "/", "d", 3, 4, 1, 1),
            # - row 4 (top) - #
            ("7", "7", "7", 2, 0, 1, 1),
            ("8", "8", "8", 2, 1, 1, 1),
            ("9", "9", "9", 2, 2, 1, 1),
            ("CE", "CE", keyboard.Key.backspace, 2, 3, 1, 1),
            ("C", "C", keyboard.Key.delete, 2, 4, 1, 1)
        ]
        
        self._setup_ui()
        self._start_keyboard_listener()
        self.create_buttons()
        # when the class is initialized (which will be at the end), 
        # these 3 things will happen.
    
    def _setup_ui(self):
        """
        Makes the layout and main UI of the application.
        """
        # - setting up the main window - #
        self.window = QMainWindow()
        self.window.resize(320,380)
        self.window.setObjectName("mainWindow")
        # this is so the window can be styled, this will occur with the
        # other elements as well like the buttons, text, etc.
        self.window.show()
        # - setting up the layout of buttons, text, etc. - #
        self.central = QWidget()
        self.window.setCentralWidget(self.central)
        # this sets self.central as the container for all the content of
        # the calculator.
        self.layout = QGridLayout(self.central)
        # we then make it so it arranges the content in a grid.
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        # - setting up the display window - #
        self.display_window = QLabel()
        # display_window is what will hold the user's inputs.
        self.display_window.setObjectName("displayWindow")
        # another instance of naming the object so it can be styled.
        self.display_window.setSizePolicy(QSizePolicy.Expanding,
                                          QSizePolicy.Expanding)
        # this is to allow the display window to resize automatically 
        # based on the size of the application, this is done with other
        # elements as well, just like setting their object name.
        self.display_window.setContentsMargins(0, 0, 0, 10)
        self.layout.addWidget(self.display_window, 1, 0, 1, 5)
        # - setting up the calculate window - #
        self.calculate_window = QLabel()
        # the calculate window is what will hold the equation the user
        # has made so far.
        self.calculate_window.setObjectName("calculateWindow")
        self.calculate_window.setSizePolicy(QSizePolicy.Expanding,
                                            QSizePolicy.Expanding)
        # another instance of allowing a widget to automatically resize.
        self.calculate_window.setContentsMargins(1, 0, 0, 80)
        self.layout.addWidget(self.calculate_window, 1, 0, 1, 5) 
        
    def _start_keyboard_listener(self):
        """
        Starts listening for keyboard inputs.
        """
        self.listener = keyboard.Listener(on_press=self.key_press,
                                          on_release=None)
        self.listener.start()
        # these 2 lines of code define a listener to listen for keyboard
        # inputs.
        
    def _create_shadow(self):
        """
        Creates a drop shadow effect for the buttons.
        
        Returns:
            self.button_shadow (var): the set shadow effect to be used
                                      by each button
        """
        self.button_shadow = QGraphicsDropShadowEffect()
        self.button_effects.append(self.button_shadow)
        # this puts the shadow in the container defined earlier.
        self.button_shadow.setXOffset(0)
        self.button_shadow.setYOffset(3)
        self.button_shadow.setBlurRadius(4)
        self.button_shadow.setColor(QColor(0, 0, 0, 15))
        return self.button_shadow
    
    def _is_operator(self, value):
        """
        Checks if the value given is an operator in the list.
        
        Args:
            value (str): the value of a button (e.g "5", "*", or "C")
        Returns:
            value (str): specifically returns if the value is an 
                         operator.
        """
        return value in ["+", "-", "*", "/"]
        # returns a value if it's in the list.
    
    def _clear_all(self):
        """
        Handles clearing/resetting (the "C" button) the calculator.
        """
        self._currently_typed = ""
        self._full_expression = ""
        self.calculate_window.setText("")
        self._can_input_operator = False
        # set to false to the first value cannot be an operator.
        self.display_window.setText("")
        
    def _clear_entry(self):
        """
        Handles backspacing (the "CE" button), when the user removes a 
        character.
        """
        self._currently_typed = self._currently_typed[:-1]
        # removes one character from the end of the string.
        self.display_window.setText(self._currently_typed)
            
        if len(self._currently_typed) == 0:
            # checks if there are 0 characters in the string.
            self._can_input_operator = False
            
    def _calculate(self):
        """
        Handles the calculation of the full expression inputted.
        (the "=" button).
        """
        final_expression = self._full_expression + self._currently_typed
            
        try:
            answer = str(eval(final_expression))
            # eval() is not a very safe method to use unless the input
            # is filtered like a calculator.
            # this runs the expression as python code, which calculates
            # the answer.
            self.calculate_window.setText(final_expression + " =")
            self.display_window.setText(answer)
                
            self._currently_typed = answer
            # sets currently_typed to the answer if they want to chain
            # equations off from it.
            self._full_expression = ""
            self._can_input_operator = True
            
        except Exception as error:
            # handles any error
            if "division by zero" in str(error):
                # checks if it is a ZeroDivisionError by checking for
                # a specific statement in the error message.
                self.display_window.setText("Undefined")
                    
            elif "invalid syntax" in str(error):
                # checks if it is a SyntaxError by checking the text
                # in the error message.
                self.display_window.setText("Syntax Error")
                
            self.calculate_window.setText("")
            self._currently_typed = ""
            self._full_expression = ""
                
            print(error)
            # prints the error message in case it's another error.
            
    def _handle_operator(self, operator):
        """Handles the input of an operator ("+", "-", etc.)"""
        if not self._currently_typed and not self._full_expression:
            # if there is no value in either of these it will ignore the
            # input of an operator.
            return
            
        if self._can_input_operator:

            self._full_expression += self._currently_typed + operator
            # gather what has currently been typed + the operator.
            self.calculate_window.setText(self._full_expression)
            
            self._currently_typed = ""
            self.display_window.setText("")
                
            self._can_input_operator = False
            
        else:
            # this allows the user to swap the operator.
            self._full_expression = self._full_expression[:-1] + operator
            self.calculate_window.setText(self._full_expression)
            
    def _handle_number(self, value):
        """
        Handles the input of a number or decimal ("7", "4", ".", etc.)
        """
        if value == "." and "." in self._currently_typed:
            # if there is already a decimal, it won't allow another.
            return

        if len(self._currently_typed) < 12:
            # limits the input amount to 12 characters, if the amount in
            # self._currently_typed is above 12, this won't run.
            self._currently_typed += value
            self.display_window.setText(self._currently_typed)
            self._can_input_operator = True
    
    # all of those functions culminate below in button_event where the
    # if elif chain is.
                
    def button_event(self, value):
        """
        Receives an input from a button/keypress and responds with the
        corresponding action.
        
        Args:
            value (str): the value of a button (e.g "5", "*", or "C")
        """
        if value == "=":
            self._calculate()
            
        elif value == "CE":
            self._clear_entry()
            
        elif value == "C":
            self._clear_all()
            
        elif self._is_operator(value):
            self._handle_operator(value)
            
        elif value.isdigit() or value == ".":
            self._handle_number(value)
            
    def key_press(self, key):
        """Handles keyboard inputs."""
        for text, value, key_value, *position in self.buttons:
            # unpacks the value and key_value to be used, ignoring
            # everything else.
            try:
                # this will only work if the key is not a key like
                # shift, alt, ctrl, etc.
                if key.char == key_value:
                    # if the character of the key equals the value
                    # required.
                    self.button_event(value)
            except AttributeError:
                # this will happen when the key is something like shift,
                # ctrl, alt, etc.
                if key == key_value:
                    # if the key itself equals the value required.
                    self.button_event(value)
        
    def create_buttons(self):
        """
        Takes the info of all buttons from a list and creates them based
        on that info.
        """
        for text, value, key_value, row, column, rspan, cspan in self.buttons:
            # loops through every button in the list and its info
            button = QPushButton(text)
            
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            def send_value(check, v=value):
                """
                Passes on the value of the button to the main handler to
                be processed.
                """
                self.button_event(v)
                # the reason this is a function is because we need to
                # catch a specific value "check", if not, pressing a
                # button will send an error.
            
            button.clicked.connect(send_value)
            # the if elif else chain below assigns the button a name
            # depending on what it is so different types of buttons
            # have different appearances.
            if value.isdigit() or value == ".":
                
                button.setObjectName("numberButton")
                
            elif value != "=":
                
                button.setObjectName("operatorButton")
                
            else:
                
                button.setObjectName("equalButton")

            self.layout.addWidget(button, row, column, rspan, cspan)
            button_shadow = self._create_shadow()
            button.setGraphicsEffect(button_shadow)
# ======================== #

# === PROGRAM EXECUTION === #
calc = CalculatorApp()
app.exec()
# ========================= #