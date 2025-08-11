from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel

class FantasyView(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets
        # Create top label
        self.label = QLabel("Enter NBA team here: ")

        # 5 inputs for the 5 starters
        self.inputs = [QLineEdit() for _ in range(5)]
        # Submit button
        self.submit_btn = QPushButton("Submit")
        # Text area for the output from the algorithm
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setMinimumHeight(250)

        # Make a layout
        layout = QVBoxLayout()

        # Add all created widgets to that layout
        layout.addWidget(self.label)
        for inp in self.inputs:
            layout.addWidget(inp)
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.output_area)

        # Set the layout
        self.setLayout(layout)

        self.resize(500,500)
