import os
from db.alchemy import DatabaseHandler
from PIL import Image
from pprint import pprint


class ImageOutput:
    def __init__(self, settings):
        self.settings = settings
        self.output_folder = self.settings["output_path"]
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)

    def output_maps(self):
        dbh = DatabaseHandler()
        all_packing_groups = dbh.get_all_packing_groups()
        a = all_packing_groups[0].textures
        print(a)
    
        for p_group in matched_p_groups:
            asset_name = p_group["textures"][0]["asset_name"]
            if not os.path.exists(f"{self.output_folder}/{asset_name}"):
                os.mkdir(f"{self.output_folder}/{asset_name}")

            identifier = p_group["group"]["identifier"]
            extension = p_group["group"]["extension"]
            output_path = (
                f"{self.output_folder}/{asset_name}/{identifier}_{asset_name}.{extension}"
            )
            self.pack_maps(output_path, p_group)

    def pack_maps(self, output_path, p_group):
        in_channels = []
        split_counter = 0
        prev_tex = ""
        for texture_type in p_group["group"]["group"]:
            if texture_type != prev_tex:
                prev_tex = texture_type
                split_counter = 0
            for texture in p_group["textures"]:
                if texture["texture_type"] == texture_type:
                    tex_split_channel = (texture["path"], split_counter)
                    split_counter += 1
                    in_channels.append(tex_split_channel)
                    break

        out_channels = []
        for in_channel in in_channels:
            in_image = Image.open(in_channel[0])
            split = in_image.split()
            out_channels.append(split[in_channel[1]])

        try:
            if len(out_channels) == 3:
                output_texture = Image.merge(
                    "RGB", (out_channels[0], out_channels[1], out_channels[2])
                )
                output_texture.save(output_path)
                return

            if len(out_channels) == 4:
                output_texture = Image.merge(
                    "RGBA",
                    (
                        out_channels[0],
                        out_channels[1],
                        out_channels[2],
                        out_channels[3],
                    ),
                )
                output_texture.save(output_path)
                return

        except Exception as e:
            print(p_group["textures"][0]["asset_name"], e)
