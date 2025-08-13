from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from PySide6.QtCore import Qt

class FantasyView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Starting lineup analyzer')
        self.resize(1000, 600)
                
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setObjectName('mainLayout')

        self.setup_ui()

        self.apply_style()
        

    def setup_ui(self):

        # Create header area
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Basketball Team Manager")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.title_label)

        # Create player input area
        player_input_layout = QHBoxLayout()

        # Make the point gaurd input + label
        pg_input_layout = QVBoxLayout()
        self.pglabel = QLabel("PG")
        self.pglabel.setAlignment(Qt.AlignCenter)
        self.pginput = QLineEdit()
        pg_input_layout.addWidget(self.pglabel)
        pg_input_layout.addWidget(self.pginput)
        player_input_layout.addLayout(pg_input_layout)

        # Make the shooting gaurd input + label
        sg_input_layout = QVBoxLayout()
        self.sglabel = QLabel("SG")
        self.sglabel.setAlignment(Qt.AlignCenter)
        self.sginput = QLineEdit()
        sg_input_layout.addWidget(self.sglabel)
        sg_input_layout.addWidget(self.sginput)
        player_input_layout.addLayout(sg_input_layout)

        # Make the small forward input + label
        sf_input_layout = QVBoxLayout()
        self.sflabel = QLabel("SF")
        self.sflabel.setAlignment(Qt.AlignCenter)
        self.sfinput = QLineEdit()
        sf_input_layout.addWidget(self.sflabel)
        sf_input_layout.addWidget(self.sfinput)
        player_input_layout.addLayout(sf_input_layout)

        # Make the power forward input + label
        pf_input_layout = QVBoxLayout()
        self.pflabel = QLabel("PF")
        self.pflabel.setAlignment(Qt.AlignCenter)
        self.pfinput = QLineEdit()
        pf_input_layout.addWidget(self.pflabel)
        pf_input_layout.addWidget(self.pfinput)
        player_input_layout.addLayout(pf_input_layout)

        # Make the point gaurd input + label
        c_input_layout = QVBoxLayout()
        self.clabel = QLabel("C")
        self.clabel.setAlignment(Qt.AlignCenter)
        self.cinput = QLineEdit()
        c_input_layout.addWidget(self.clabel)
        c_input_layout.addWidget(self.cinput)
        player_input_layout.addLayout(c_input_layout)


        # Make the submit and output area
        submit_and_output_layout = QVBoxLayout()
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setObjectName('submitBtn')
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setMinimumHeight(250)
        self.output_area.setObjectName('outputarea')

        submit_and_output_layout.addWidget(self.submit_btn)
        submit_and_output_layout.addWidget(self.output_area)

        self.main_layout.addLayout(header_layout)
        self.main_layout.addLayout(player_input_layout)
        self.main_layout.addLayout(submit_and_output_layout)


    def apply_style(self):

        self.setStyleSheet("""
            #mainLayoutKs {
                color: blue;               
            }
                           
            #titleLabel {
                font-size: 24px;
                color: red;    
            }
                           
            #submitBtn {
                margin-top: 20px;
                margin-bottom: 20px;
                margin-left: 100px;
                margin-right: 100px;
                height: 30px;
            }
                           
            #outputarea {
                font-size: 18px; 
            }
            
        """)