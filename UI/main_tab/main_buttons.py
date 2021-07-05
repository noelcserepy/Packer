from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from packer.packer import Packer


class MainButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        # Button widget to hold "SCAN" and "PACK" buttons
        self.refresh_button = QPushButton("SCAN")
        self.refresh_button.clicked.connect(self.on_scan_clicked)
        self.pack_button = QPushButton("PACK")
        self.pack_button.clicked.connect(self.on_pack_clicked)
        self.live_pack_text = QLabel("Live Pack Assets")
        self.live_pack_checkbox = QCheckBox()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.pack_button)
        self.layout.addWidget(self.live_pack_text)
        self.layout.addWidget(self.live_pack_checkbox)

    def on_pack_clicked(self):
        Packer().pack()

    def on_scan_clicked(self):
        Packer().scan_new()