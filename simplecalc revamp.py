import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor
from PySide6.QtCore import Slot

app = QApplication([])

with open(r"C:/Users/jdpat/Downloads/CalculatorPython/CalculatorStyleSheet.qss") as file:
    app.setStyleSheet(file.read())

class Calculator:

    def __init__(self):
        self.window = QMainWindow()
        
        self.window.resize(320,430)
        self.window.setObjectName("mainWindow")
        self.window.show()
        
        self.central = QWidget()
        self.window.setCentralWidget(self.central)

        self.layout = QGridLayout(self.central)
        self.layout.setRowStretch(0, 1) # Put all extra vertical space in row 5
        self.layout.setColumnStretch(1, 1) # Put all extra horizontal space in column 1
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.current_input = ""
        
        self.input_window = QLabel()
        self.input_window.setObjectName("inputWindow")
        self.layout.addWidget(self.input_window, 1, 0, 1, 4)
        
        self.button_effects = []
        
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
            print(eval(self.current_input))
            answer = str(eval(self.current_input))
            self.input_window.setText(answer)
            self.current_input = ""
        elif value == "CE":
            self.current_input = self.current_input[:-1]
            print(self.current_input)
        elif value == "C":
            self.current_input = ""
            print(self.current_input)
        else:
            self.current_input += value
            print(self.current_input)
        
        if value != "=":
            self.input_window.setText(self.current_input)
        
    def create_buttons(self):
        numbers = [
            # row 1 (bottom)
            ("0", "0", 5, 0, 1, 2),
            (".", ".", 5, 2, 1, 1),
            ("=", "=", 5, 3, 1, 2),
            # row 2
            ("1", "1", 4, 0, 1, 1),
            ("2", "2", 4, 1, 1, 1),
            ("3", "3", 4, 2, 1, 1),
            ("+", "+", 4, 3, 1, 1),
            ("-", "-", 4, 4, 1, 1),
            # row 3
            ("4", "4", 3, 0, 1, 1),
            ("5", "5", 3, 1, 1, 1),
            ("6", "6", 3, 2, 1, 1),
            ("×", "*", 3, 3, 1, 1),
            ("÷", "/", 3, 4, 1, 1),
            # row 4 (top)
            ("7", "7", 2, 0, 1, 1),
            ("8", "8", 2, 1, 1, 1),
            ("9", "9", 2, 2, 1, 1),
            ("CE", "CE", 2, 3, 1, 1),
            ("C", "C", 2, 4, 1, 1)
        ]
        
        for text, value, row, column, rspan, cspan in numbers:
            button = QPushButton(text)
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