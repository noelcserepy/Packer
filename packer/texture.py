import re 
from datetime import datetime
from pprint import pprint

class Texture():
    def __init__(self, settings, path):
        self.all_texture_types = settings["textures"]
        self.path = path

        self.filename_full = self.path.split("/")[-1]
        self.filename, self.extension = self.filename_full.split(".")
        self.directory = self.path[:-len(self.filename_full)]
        
        self.scan_timestamp = datetime.now().timestamp()
        self.asset_name = str()
        self.preferred_filename = str()
        self.texture_type = str()
        self.preferred_identifier = str()

        self._identify_texture_from_path()

        
    def _identify_texture_from_path(self):
        for tex in self.all_texture_types:
            if self.extension.upper() not in tex["extensions"]:
                continue

            self._determine_asset_name(tex["identifiers"])

            if not self.asset_name:
                continue

            self.texture_type = tex["name"]
            self.preferred_identifier = tex["preferred_identifier"]
            self._create_preferred_filename()
            return

    
    def _determine_asset_name(self, identifiers):
        for id in identifiers:
            if id[1] == "end":
                pattern = rf".*{id[0]}$"
                match = re.search(pattern, self.filename)
                if match:
                    self.asset_name = self.filename[:-len(id[0])]
                    return
            if id[1] == "start":
                pattern = rf"^{id[0]}.*"
                match = re.match(pattern, self.filename)
                if match:
                    self.asset_name = self.filename[len(id[0]):]
                    return


    def _create_preferred_filename(self):
        if self.preferred_identifier[1] == "start":
            self.preferred_filename = f"{self.preferred_identifier[0]}{self.asset_name}.{self.extension}"
            return
        if self.preferred_identifier[1] == "end":
            self.preferred_filename = f"{self.asset_name}{self.preferred_identifier[0]}.{self.extension}"
            return


    def get_texture_data(self):
        texture_data = {
            "asset_name": self.asset_name,
            "path": self.path,
            "dir": self.directory,
            "current_filename": self.filename_full,
            "preferred_filename": self.preferred_filename,
            "texture_type": self.texture_type,
            "scan_timestamp": self.scan_timestamp
        }
        return texture_data