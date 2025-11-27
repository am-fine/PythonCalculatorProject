import sys
import pynput
from pynput import keyboard
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor
from PySide6.QtCore import Slot

app = QApplication([])

script_path = Path(sys.argv[0]).resolve()
script_dir = script_path.parent
qss_file_name = "CalculatorStyleSheet.qss"
qss_file_path = script_dir / qss_file_name

try:
    with open(qss_file_path, "r") as file:
        app.setStyleSheet(file.read())
        print(f"Successfully loaded stylesheet from: {qss_file_path}")
except FileNotFoundError:
    print(f"Error: Stylesheet file not found at {qss_file_path}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

class Calculator:

    def __init__(self):
        self.window = QMainWindow()
        
        self.window.resize(320,380)
        self.window.setObjectName("mainWindow")
        self.window.show()
        
        self.central = QWidget()
        self.window.setCentralWidget(self.central)

        self.layout = QGridLayout(self.central)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.current_input = ""
        
        self.input_window = QLabel()
        self.input_window.setObjectName("inputWindow")
        self.input_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input_window.setContentsMargins(0, 10, 0, 10)
        self.layout.addWidget(self.input_window, 1, 0, 1, 5)
        
        self.button_effects = []
        
        self.buttons = [
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
        
        listener = keyboard.Listener(on_press=self.key_press, on_release=None)
        listener.start()
        
        self.create_buttons()
        
    def create_shadow(self):
        self.button_shadow = QGraphicsDropShadowEffect()
        self.button_effects.append(self.button_shadow)
        self.button_shadow.setXOffset(0)
        self.button_shadow.setYOffset(3)
        self.button_shadow.setBlurRadius(4)
        self.button_shadow.setColor(QColor(0, 0, 0, 15))
        return self.button_shadow        
    
    @Slot()  
    def button_event(self, value):
        if value == "=":
            try:
                answer = str(eval(self.current_input))
                self.input_window.setText(answer)
                self.current_input = ""
            except SyntaxError:
                self.input_window.setText("Syntax Error")
                self.current_input = ""

        elif value == "CE":
            self.current_input = self.current_input[:-1]
            
        elif value == "C":
            self.current_input = ""
            
        elif len(self.current_input) == 12:
            self.current_input = self.current_input
        else:
            self.current_input += value
            
        if value != "=":
            self.input_window.setText(self.current_input)
            
    @Slot()
    def key_press(self, key):
        for text, value, key_value, *position in self.buttons:
            try:
                if key.char == key_value:
                    self.button_event(value)
            except AttributeError:
                if key == key_value:
                    self.button_event(value)
                    
        
    def create_buttons(self):
        
        for text, value, key_value, row, column, rspan, cspan in self.buttons:
            
            button = QPushButton(text)
            
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            def send_value(check, v=value):
                self.button_event(v)
            
            button.clicked.connect(send_value)
            if value.isdigit() or value == ".":
                button.setObjectName("numberButton")
            elif value != "=":
                button.setObjectName("operatorButton")
            else:
                button.setObjectName("equalButton")
            self.layout.addWidget(button, row, column, rspan, cspan)
            button_shadow = self.create_shadow()
            button.setGraphicsEffect(button_shadow)
            
calc = Calculator()
app.exec()