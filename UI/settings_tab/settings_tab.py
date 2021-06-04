import json
from PySide6 import QtCore
from PySide6.QtWidgets import *
from UI.settings_tab.texture_select import TextureSelect
from UI.settings_tab.dir_select import DirSelect
from UI.settings_tab.packinggroup_select import PackingGroupSelect


with open("settings.json", "r") as f:
    settings = json.load(f)


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()


    def setup(self):
        self.dirselect  = DirSelect(settings)
        self.dirselect.setMinimumHeight(150)
        self.dirselect.setMaximumHeight(150)
        self.dirselect.setMinimumWidth(800)
        self.texture_select = TextureSelect(settings)
        self.texture_select.setMinimumHeight(400)
        self.texture_select.setMinimumWidth(1000)
        self.packinggroupselect  = PackingGroupSelect(settings)
        self.packinggroupselect.setMinimumHeight(400)
        self.packinggroupselect.setMinimumWidth(1000)
        self.save = QWidget(self)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.on_save_clicked)
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.on_reset_clicked)

        self.save.layout = QHBoxLayout(self.save)
        self.save.layout.addWidget(self.reset_button)
        self.save.layout.addWidget(self.save_button)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.dirselect, 0, 0, 1, 2)
        self.layout.addWidget(self.texture_select, 1, 0, 1, 2)
        self.layout.addWidget(self.packinggroupselect, 2, 0, 1, 2)
        self.layout.addWidget(self.save, 3, 1, 1, 1)
        

    def print_data(self):
        collected_settings = {
            "sync_asset_dir": self.dirselect.get_data(),
            "textures": self.texture_select.get_data(),
            "packing_groups": self.packinggroupselect.get_data()
        }
        print(collected_settings)
        

    def on_save_clicked(self):
        collected_settings = {
            "sync_asset_dir": self.dirselect.get_data(),
            "textures": self.texture_select.get_data(),
            "packing_groups": self.packinggroupselect.get_data()
        }

        with open("settings.json", "w+") as f:
            json.dump(collected_settings, f)


    def on_reset_clicked(self):
        try:
            default_settings = json.load(open("settings_default.json", "r"))
        except:
            print("No default settings here.")
            return

        with open("settings.json", "w") as f:
            json.dump(default_settings, f)
        





