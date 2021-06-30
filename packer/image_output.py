import os
from db.alchemy import DatabaseHandler
from PIL import Image


class ImageOutput:
    def __init__(self, settings):
        self.settings = settings
        self.output_path = self.settings["output_path"]
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def output_maps(self):
        dbh = DatabaseHandler()
        all_packing_groups = dbh.get_all_packing_groups()

        for packing_group in all_packing_groups:
            try:
                file_path = self._make_file_path(packing_group)
                print(file_path)
                # self._pack_maps(file_path, packing_group)
            except Exception as e:
                print(e)

    def _make_file_path(self, packing_group):
        asset_name = packing_group["asset_name"]
        if self.settings["source_path_as_output"]:
            file_path = self._make_source_file_path(packing_group, asset_name)
        else:
            file_path = self._make_new_output_file_path(asset_name, packing_group)

        return file_path

    def _make_new_output_file_path(self, asset_name, packing_group):
        if not os.path.exists(f"{self.output_path}/{asset_name}"):
            os.mkdir(f"{self.output_path}/{asset_name}")

        file_path = f"{self.output_path}/{asset_name}/{packing_group['identifier']}_{asset_name}.{packing_group['extension']}"
        return file_path

    def _make_source_file_path(self, packing_group, asset_name):
        source_directory = packing_group["directory"]
        file_path = f"{source_directory}/{packing_group['identifier']}_{asset_name}.{packing_group['extension']}"
        return file_path

    def _pack_maps(self, file_path, packing_group):
        in_channels = []
        split_counter = 0
        prev_tex = ""
        for texture_type in packing_group["group"]["group"]:
            if texture_type != prev_tex:
                prev_tex = texture_type
                split_counter = 0
            for texture in packing_group["textures"]:
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
                output_texture.save(file_path)
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
                output_texture.save(file_path)
                return
        except Exception as e:
            print(packing_group["textures"][0]["asset_name"], e)
