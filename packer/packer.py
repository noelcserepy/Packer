import json
from packer.file_search import FileSearch
from packer.texture_match import TextureMatch
from db.alchemy import DatabaseHandler
from packer.image_output import ImageOutput


class Packer:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

    def complete_search(self):
        self.file_paths = FileSearch(self.settings).file_paths
        self._make_textures_from_file_paths()
        dbh = DatabaseHandler()
        dbh.populate_packing_groups(self.settings)

    def pack(self):
        imo = ImageOutput(self.settings)
        imo.output_maps()

    def scan_new(self):
        pass

    def _make_textures_from_file_paths(self):
        for file in self.file_paths:
            texture_match = TextureMatch(self.settings, file)
            if texture_match.match_completed:
                texture_match.save_in_db()
