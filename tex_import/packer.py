import os
import json
from collections import Counter
from PIL import Image



class Packer():
    def __init__(self, settings):
        self.settings = settings


    def create_packing_groups(self, asset_files):
        matched_p_groups = []
        for asset in asset_files.values():
            for p_group in self.settings["packing_groups"]:
                matched = self.match_textures(p_group, asset)
                if matched:
                    matched_group = {
                        "group": p_group,
                        "textures": matched
                    }
                    matched_p_groups.append(matched_group)

        json.dump(matched_p_groups, open("pgroups.json", "w+"))

        #output_maps(matched_p_groups)


    def match_textures(self, p_group, asset):
        g = p_group["group"]
        matched = []
        for t_type in g:
            len_before = len(matched)
            for texture in asset:
                if texture["texture_type"] == t_type:
                    matched.append(texture)
                    break
            len_after = len(matched)
            if len_after <= len_before:
                return None
        return matched


    def output_maps(self, matched_p_groups):
        output_folder = self.settings["output_path"]
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        for p_group in matched_p_groups:
            asset_name = p_group["textures"][0]["asset_name"]
            identifier = p_group["group"]["identifier"]
            extension = p_group["group"]["extension"]
            output_path = f"{output_folder}/{identifier}_{asset_name}_{extension}"
            self.pack_maps(output_path, p_group)   


    def pack_maps(self, output_path, p_group):
        """ 
        Packs 3 or 4 files into a single texture and saves it with a given identifier and extension (set by match group settings).
        Sets channels with missing files to black (user setting?). 
        """
    
        type_count = dict(Counter(p_group["group"]["group"]))

        channels = []
        occurrence = 0
        for texture in p_group["textures"]:
            texture_img = Image.open(texture["path"])

            r, *_ = texture_img.split()
            print(r.format, r.size, r.mode)
        
        for file in p_group:
            texture_map = Image.open(file)
            r, *_ = texture_map.split()
            print(r.format, r.size, r.mode)
            r.append(r)

        if len(channels) == 3:
            output_texture = Image.merge("RGB", (channels[0], channels[1], channels[2]))
            with open(output_path, "wb") as f:
                f.write(output_texture)

        if len(channels) == 4:
            output_texture = Image.merge("RGBA", (channels[0], channels[1], channels[2], channels[3]))
            with open(output_path, "wb") as f:
                f.write(output_texture)

