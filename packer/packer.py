import json
from packer.file_search import FileSearch
from packer.texture_match import TextureMatch
from db.alchemy import DatabaseHandler
from packer.image_output import ImageOutput


class Packer:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

        self.file_paths = FileSearch(self.settings).file_paths

        self._make_textures_from_file_paths()
        self._match_textures_to_packing_group()
        imo = ImageOutput(self.settings)
        imo.output_maps()

    def _make_textures_from_file_paths(self):
        for file in self.file_paths:
            texture_match = TextureMatch(self.settings, file)
            if texture_match.match_completed:
                texture_match.save_in_db()

    def _match_textures_to_packing_group(self):
        dbh = DatabaseHandler()
        for packing_group in self.settings["packing_groups"]:
            dbh.populate_packing_groups(packing_group)

    def pack():
        pass

    def refresh():
        pass
