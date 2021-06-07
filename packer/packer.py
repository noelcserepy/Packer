import json
from packer.texture import Texture
from packer.packinggroup import GroupPacker
from packer.filesearch import FileSearch


class Packer():
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.load(f)
        
        self.all_directory_file_paths = FileSearch(self.settings).all_directory_file_paths
        self.all_textures = self._make_textures_from_file_paths()
        self.all_packing_groups = GroupPacker(self.settings).create_packing_groups(self.all_textures)


    def _make_textures_from_file_paths(self):
        asset_files = {}
        for file in self.all_directory_file_paths:
            try:
                texture = Texture(self.settings, file).get_texture_data()
                if not texture:
                    raise Exception("Texture could not be created.")
                
                asset_name = texture["asset_name"]
                if asset_name not in asset_files.keys():
                    asset_files[asset_name] = []

                asset_files[asset_name].append(texture)
            except:
                continue
        return asset_files




# def refresh():
#     pass


# def pack():
#     p_groups = json.load(open("pgroups.json"))
#     pg.output_maps(p_groups)


