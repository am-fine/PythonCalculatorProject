# John Daniel's Simple Calculator [ADVANCED+] - 11/25-28/11/25 (forgot when i started)
# - PLEASE READ - #
# Some info you should know before hand!

# WHAT ARE STYLE SHEETS?
# You'll see me refer to style sheets, these are light.qss and dark.qss, this is basically
# what makes the calculator looks nice.

# PYSIDE6
# I used the module PySide6 which is managed by Qt, a pretty popular GUI application for many
# different languages, most of this code is just making and updating the GUI.

import sys # imports python's sys module, this is to access the style sheets
from pathlib import Path # imports Path, this is also used to access the style sheets
from PySide6.QtWidgets import * # imports every kind of widget, kind of innefficient but better than adding something everytime i need another thing
from PySide6.QtGui import QColor # this is only used to set the color of a shadow
from pynput import keyboard # this is to monitor the keyboard's input using the pynput module
import darkdetect # this is to set a theme based on the system theme of the user using darkdetect

app = QApplication([]) # this defines the application itself

sys.set_int_max_str_digits(100000)

# - retrieving the style sheets - #

script_path = Path(sys.argv[0]).resolve() # makes an absolute path to the style sheets
script_dir = script_path.parent # gets the directory of the sheets

light_qss = "light.qss" # defines the light mode style sheet
dark_qss = "dark.qss" # defines the dark mode style sheet

light_file_path = script_dir / light_qss # defines the path to the light mode style sheet
dark_file_path = script_dir / dark_qss # defines the path to the dark mode style sheet

# - detecting the system theme to set a corresponding theme - #

if darkdetect.isLight(): # checks if the user is using the light system mode
    
    try: # tries to open the light mode style sheet
        with open(light_file_path, "r") as file: # this is what opens the file so it can be read
            app.setStyleSheet(file.read()) # this is what reads the style sheet
            print(f"loaded stylesheet from: {light_file_path}") # will print if the style sheet has been read
            
    except FileNotFoundError: # if the file is not found
        print(f"file not found at {light_file_path}") # it will give the user an error message
        
    except Exception as error: # if something weird occurs, it will tell the user
        print(f"unexpected error occurred: {error}")
        
elif darkdetect.isDark(): # checks if the user is using the dark system mode
    
    try: # tries to open the dark mode style sheet
        with open(dark_file_path, "r") as file: # opens the file to be read
            app.setStyleSheet(file.read()) # reads the file
            print(f"loaded stylesheet from: {dark_file_path}") # tells the user it was read
            
    except FileNotFoundError: # if the file is not found
        print(f"file not found at {dark_file_path}") # it will tell the user that
        
    except Exception as error: # and if something unexpected happens
        print(f"unexpected error occurred: {error}") # it will tell the user
        
else: # if for some reason no theme is found
    print("inavlid theme") # the user will know because the code will tell them

# - the calculator's code - #

class Calculator: # defines the calculator class, this is so i could get around using global variables which would have been much messier
    """
    insert docstring
    """
    def __init__(self): # upon initialization of the class
        """
        insert docstring
        """
        self.window = QMainWindow() # define the main window of the application
        
        self.window.resize(320,380) # set its starting size
        self.window.setObjectName("mainWindow") # set its object name so it can be styled
        self.window.show() # show the window
        
        self.menu_bar = self.window.menuBar() # define a menu bar
        self.menu_bar.setObjectName("menuBar") # set the object name so it can be styled
        self.info_menu = self.menu_bar.addMenu("Info") # define a menu in the menu bar
        
        self.keybind_action = self.info_menu.addAction("Keybinds") # define an action from the menu
        self.keybind_action.setObjectName("keybindAction") # set its object name so it can be styled
        
        self.menu_bar.show() # show the menu bar
        
        self.central = QWidget() # define a central widget for organizing the buttons
        self.window.setCentralWidget(self.central) # set the central widget of the window to the central widget defined

        self.layout = QGridLayout(self.central) # add a layout to the central widget
        self.layout.setSpacing(10) # set the spacing of elements within the layot
        self.layout.setContentsMargins(10, 10, 10, 10) # set the margin of items in the layout
        
        self.currently_typed = "" # define what is currently typed by the user
        self.full_expression = "" # define what the full math expression is
        
        self.can_input_operator = True # define a flag to check whether the user can input an operator
        
        self.display_window = QLabel() # define the display window of the calculator
        self.display_window.setObjectName("displayWindow") # set the object name so it can be styled
        self.display_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # allow it to be resized automatically
        self.display_window.setContentsMargins(0, 0, 0, 10) # set the margins of the display window
        self.layout.addWidget(self.display_window, 1, 0, 1, 5) # set the position of the display window
        
        self.calculate_window = QLabel() # define the calculate window (what shows the calculation)
        self.calculate_window.setObjectName("calculateWindow") # set object name so it can be styled
        self.calculate_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # allow it to be automatically resized
        self.calculate_window.setContentsMargins(1, 0, 0, 80) # set its margins
        self.layout.addWidget(self.calculate_window, 1, 0, 1, 3) # set its position (it overlaps technically, but because of the margins it appears above the display window)
        
        self.button_effects = [] # this is to contain every single drop shadow for the buttons
        
        self.buttons = [ # list of every button with corresponding data to each
            # order of info: text, value, keyboard input, row position, column position, row spanning, column spanning
            
            # row 1 (bottom)
            ("0", "0", "0", 5, 0, 1, 2),
            (".", ".", ".", 5, 2, 1, 1),
            ("=", "=", keyboard.Key.enter, 5, 3, 1, 2),
            # row 2
            ("1", "1", "1", 4, 0, 1, 1),
            ("2", "2", "2", 4, 1, 1, 1),
            ("3", "3", "3", 4, 2, 1, 1),
            ("+", "+", "a", 4, 3, 1, 1),
            ("-", "-", "s", 4, 4, 1, 1),
            # row 3
            ("4", "4", "4", 3, 0, 1, 1),
            ("5", "5", "5", 3, 1, 1, 1),
            ("6", "6", "6", 3, 2, 1, 1),
            ("×", "*", "x", 3, 3, 1, 1),
            ("÷", "/", "d", 3, 4, 1, 1),
            # row 4 (top)
            ("7", "7", "7", 2, 0, 1, 1),
            ("8", "8", "8", 2, 1, 1, 1),
            ("9", "9", "9", 2, 2, 1, 1),
            ("CE", "CE", keyboard.Key.backspace, 2, 3, 1, 1),
            ("C", "C", keyboard.Key.delete, 2, 4, 1, 1)
        ]
        
        listener = keyboard.Listener(on_press=self.key_press, on_release=None) # defines the listener for the keyboard
        listener.start() # starts the listener to listen for keyboard inputs
        
        self.create_buttons() # calls the function that creates the buttons
    
    # OUTSIDE OF __init__ 
        
    def create_shadow(self): # define a function to create the drop shadows for each button
        """
        insert docstring
        """
        self.button_shadow = QGraphicsDropShadowEffect() # creates the drop shadow
        self.button_effects.append(self.button_shadow) # assigns it to container self.button_effects
        self.button_shadow.setXOffset(0) # sets the x offset of the shadow
        self.button_shadow.setYOffset(3) # sets the y offset of the shadow
        self.button_shadow.setBlurRadius(4) # sets the blur radius of the shadow
        self.button_shadow.setColor(QColor(0, 0, 0, 15)) # sets the colour of the shadow
        return self.button_shadow # returns the shadow
    
    def is_operator(self, value): # define a function to define what an operator is
        """
        insert docstring
        """
        return value in ["+", "-", "*", "/"] # returns value if it matches a character in the list
    
    def button_event(self, value): # defines the button event
        """
        insert docstring
        """
        is_operator = self.is_operator(value) # defines to the code what an operator is
        if value == "=": # if the user presses =
            
            final_expression = self.full_expression + self.currently_typed # makes the final expression to be calculated
            
            try: # checks if it can be evaluated
                answer = str(eval(final_expression)) # this is what defines the answer
                
                self.calculate_window.setText(final_expression + " =") # sets calculate window to display the equation
                self.display_window.setText(answer) # sets the display window to display the answer
                
                self.currently_typed = answer # sets what is currently typed as the answer (so the user can manipulate their answer further if wanted)
                self.full_expression = "" # sets the full expression to blank again
                self.can_input_operator = True # allows the user to input an operator (if they want to manipulate their answer)
            except Exception as error: # if an error occurs
                
                if Exception == SyntaxError: # if the error is a syntax error
                    self.display_window.setText("Syntax Error") # update the display to show that
                    
                elif Exception == ZeroDivisionError: # if it's a division involving 0
                    self.display_window.setText("Undefined") # update the display to show that
                
                self.calculate_window.setText("") # reset calculate window
                self.currently_typed = "" # reset what is currently typed
                self.full_expression = "" # reset the full expression
                
                print(error) # print the error in the console for debugging, in case its neither of the mentioned errors

        elif value == "CE": # if the user presses CE
            self.currently_typed = self.currently_typed[:-1] # removes one character from what is currently typed
            self.display_window.setText(self.currently_typed) # updates the display window
            
            if len(self.currently_typed) == 0: # if the user has removed all characters it will make sure they cannot enter an operator
                self.can_input_operator = False # won't allow an operator
            
        elif value == "C": # if the user presses C
            self.currently_typed = "" # clears what has currently been typed
            self.full_expression = "" # clears the entire expression
            self.calculate_window.setText("") # resets the calculate window
            self.display_window.setText("") # resets the display window
            self.can_input_operator = False # won't allow a user to input an operator as that would be the first value
            
        elif is_operator: # if the user presses an operator
            if not self.currently_typed and not self.full_expression: # if nothing has been typed, no operator will be inputted
                
                return # does nothing
            
            if self.can_input_operator: # if the user can input an operator
                
                self.full_expression += self.currently_typed + value # adds what has been typed and the operator to the full expression
                self.calculate_window.setText(self.full_expression) # updates the calculate window to the full expression
                
                self.currently_typed = "" # resets what the user has typed
                self.display_window.setText("") # resets the display window
                
                self.can_input_operator = False # won't allow the user to input an operator 
            
            else: # this allows the user to swap the operator
                
                self.full_expression = self.full_expression[:-1] + value # replaces whatever the last operator was
                self.calculate_window.setText(self.full_expression) # updates the calculate window
        
        elif value.isdigit() or value == ".": # if the user presses a digit or the decimal button
            
            if value == "." and "." in self.currently_typed: # if there is already a decimal it won't add another
                return # does nothing

            if len(self.currently_typed) < 12: # if the current input is below 12
                self.currently_typed += value # updates what has currently been typed
                self.display_window.setText(self.currently_typed) # updates the display
                self.can_input_operator = True # allows an operator to be typed
            
    def key_press(self, key): # defines a function to detect certain key inputs
        """
        insert docstring
        """
        for text, value, key_value, *position in self.buttons: # unpacks the buttons list, specifically to access what each button corresponds to on the keyboard
            try: # tries checking if a key is not a special key (like shift, ctrl, alt, etc.)
                if key.char == key_value: # if the character of the key equals the key value that was unpacked from buttons
                    self.button_event(value) # call on the button event function sending out the value
            except AttributeError: # if there's an attribute error (if IT IS a special key like shift or ctrl)
                if key == key_value: # if the key (not the character of it) equals the key value
                    self.button_event(value) # call on the button event sending the value
        
    def create_buttons(self): # defines a function to create the buttons
        """
        insert docstring
        """
        for text, value, key_value, row, column, rspan, cspan in self.buttons: # loops through every piece of data each button has
            
            button = QPushButton(text) # defines the button
            
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # allows it to be resized automatically
            
            def send_value(check, v=value): # defines a function to send out the value
                """
                insert docstring
                """
                self.button_event(v) # calls on the button event sending the value of the button
            
            button.clicked.connect(send_value) # if the button is clicked it will send the value
            if value.isdigit() or value == ".": # if the button is a digit button, or the decimal button
                button.setObjectName("numberButton") # set its object name to be styled
            elif value != "=": # if the button is an operator
                button.setObjectName("operatorButton") # set its object name to be styled differently from the numbers
            else: # if it is the equals button
                button.setObjectName("equalButton") # set its name to be styled as the equals button
            self.layout.addWidget(button, row, column, rspan, cspan) # places the button depending on its positon data
            button_shadow = self.create_shadow() # calls shadow creation function to create a shadow for the button
            button.setGraphicsEffect(button_shadow) # give the button its shadow
            
calc = Calculator() # initialize the class
app.exec() # execute the application