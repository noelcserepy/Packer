import json
from packer.texture_match import TextureMatch
from packer.packinggroup import GroupPacker
from packer.filesearch import FileSearch
from db.alchemy import DatabaseHandler


class Packer:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)

        self.all_directory_file_paths = FileSearch(
            self.settings
        ).all_directory_file_paths
        self.all_textures = self._make_textures_from_file_paths()
        self.all_packing_groups = GroupPacker(
            self.settings
        ).match_textures_to_packing_group()

    def _make_textures_from_file_paths(self):
        for file in self.all_directory_file_paths:
            texture_match = TextureMatch(self.settings, file)
            if texture_match.match_completed:
                texture_match.save_in_db()

    # def _make_textures_from_file_paths(self):
    #     textures_by_asset = {}
    #     for file in self.all_directory_file_paths:
    #         try:
    #             texture = Texture(self.settings, file).get_texture_data()
    #             if not texture:
    #                 raise Exception("Texture could not be created.")

    #             asset_name = texture["asset_name"]
    #             if asset_name not in textures_by_asset.keys():
    #                 textures_by_asset[asset_name] = []

    #             textures_by_asset[asset_name].append(texture)
    #         except:
    #             continue
    #     return textures_by_asset


# def refresh():
#     pass


# def pack():
#     p_groups = json.load(open("pgroups.json"))
#     pg.output_maps(p_groups)
