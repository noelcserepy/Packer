import json
from packer.texture_match import TextureMatch
from packer.packinggroup import GroupPacker
from packer.filesearch import FileSearch


class Packer:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

        self.file_paths = FileSearch(self.settings).file_paths

        self._make_textures_from_file_paths()
        GroupPacker(self.settings).match_textures_to_packing_group()

    def _make_textures_from_file_paths(self):
        for file in self.file_paths:
            texture_match = TextureMatch(self.settings, file)
            if texture_match.match_completed:
                texture_match.save_in_db()

    def refresh():
        pass

    def pack():
        pass
