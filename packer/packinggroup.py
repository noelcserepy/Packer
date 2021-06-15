import os
from PIL import Image
from db.alchemy import DatabaseHandler


class GroupPacker:
    def __init__(self, settings):
        self.settings = settings

    def match_textures_to_packing_group(self):
        dbh = DatabaseHandler()
        for packing_group in self.settings["packing_groups"]:
            dbh.add_textures_to_pg(packing_group)

    # def create_packing_groups(self, asset_files):
    #     matched_p_groups = []
    #     for asset in asset_files.values():
    #         for p_group in self.settings["packing_groups"]:
    #             matched = self._match_textures(p_group, asset)
    #             if matched:
    #                 matched_group = {"group": p_group, "textures": matched}
    #                 matched_p_groups.append(matched_group)

    #     for m in matched_p_groups:
    #         pg = PackingGroup(m)
    #         pg.save_packing_group_in_database()

    #     json.dump(matched_p_groups, open("pgroups.json", "w+"))

    # def _match_textures(self, p_group, asset):
    #     g = p_group["group"]
    #     matched = []
    #     for t_type in g:
    #         len_before = len(matched)
    #         for texture in asset:
    #             if texture["texture_type"] == t_type:
    #                 matched.append(texture)
    #                 break
    #         len_after = len(matched)
    #         if len_after <= len_before:
    #             return None
    #     return matched

    def output_maps(self, matched_p_groups):
        output_folder = self.settings["output_path"]
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        for p_group in matched_p_groups:
            asset_name = p_group["textures"][0]["asset_name"]
            if not os.path.exists(f"{output_folder}/{asset_name}"):
                os.mkdir(f"{output_folder}/{asset_name}")

            identifier = p_group["group"]["identifier"]
            extension = p_group["group"]["extension"]
            output_path = (
                f"{output_folder}/{asset_name}/{identifier}_{asset_name}.{extension}"
            )
            self.pack_maps(output_path, p_group)

    def pack_maps(self, output_path, p_group):
        """
        Packs 3 or 4 files into a single texture and saves it with a given identifier and extension (set by match group settings).
        Sets channels with missing files to black (user setting?).
        """

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
