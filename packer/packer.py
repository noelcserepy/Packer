import json
from packer.file_search import FileSearch
from packer.texture_match import TextureMatch
from db.alchemy import DatabaseHandler
from packer.image_output import ImageOutput


class Packer:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

    def scan(self, rescan=False):
        if rescan:
            fs = FileSearch(self.settings, rescan=True)
        else:
            fs = FileSearch(self.settings)
        self.file_paths = fs.get_file_paths()
        self._make_textures_from_file_paths()
        dbh = DatabaseHandler()
        dbh.populate_all_packing_groups(self.settings)

    def pack(self):
        imo = ImageOutput(self.settings)
        imo.time_the_functions()

    def _make_textures_from_file_paths(self):
        dbh = DatabaseHandler()
        for file in self.file_paths:
            texture_match = TextureMatch(self.settings, file)
            if texture_match.match_completed:
                dbh.add_texture(texture_match)
