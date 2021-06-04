from datetime import datetime

class Texture():
    def __init__(self, settings, path):
        self.path = path
        self.settings = settings
        self.filename_full = self.path.split("/")[-1]
        self.filename, self.extension = self.filename_full.split(".")
        self.directory = self.path[:-len(self.filename_full)]
        self.scan_timestamp = datetime.now().timestamp()
        self.asset_name = str()
        self.preferred_filename = str()
        self.texture_type = str()
        self.preferred_identifier = str()

        self._identify_texture()

        
    def _identify_texture(self):
        for tex in self.settings["textures"]:
            self.texture_type = tex["name"]
            if self.extension.upper() not in tex["extensions"]:
                continue
            self.preferred_identifier = tex["preferred_identifier"]
            for id in tex["identifiers"]:
                self._differentiate_start_and_end(id)


    def _differentiate_start_and_end(self, id):
        if id[1] == "end":
            if self.filename.endswith(id[0]):
                self.asset_name = self.filename[:-len(id[0])]
                self._create_preferred_filename(self.preferred_identifier, self.asset_name)
        if id[1] == "start":
            if self.filename.startswith(id[0]):
                self.asset_name = self.filename[len(id[0]):]
                self._create_preferred_filename(self.preferred_identifier, self.asset_name)


    def _create_preferred_filename(self, preferred_identifier, asset_name):
        if preferred_identifier[1] == "start":
            new_filename = f"{preferred_identifier[0]}{asset_name}"
        if preferred_identifier[1] == "end":
            new_filename = f"{asset_name}{preferred_identifier[0]}"
        self.preferred_filename = f"{new_filename}.{self.extension}"


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
        print(texture_data)
        return texture_data