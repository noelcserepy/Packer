import os
import concurrent.futures
from db.alchemy import DatabaseHandler
from PIL import Image
from sqlalchemy.sql.expression import except_


class PackException(Exception):
    def __init__(self, packing_group_id, message):
        self.packing_group_id = packing_group_id
        self.message = message


class ImageOutput:
    def __init__(self, settings):
        self.settings = settings
        self.output_path = self.settings["output_path"]
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def output_maps(self):
        dbh = DatabaseHandler()
        all_packing_groups = dbh.get_all_packing_groups()
        for pg in all_packing_groups:
            try:
                result = self._multiprocess_pack(pg)
                dbh.set_packing_group_status(result, "Packed")
                print(result)
            except Exception as e:
                dbh.set_packing_group_status(e.packing_group_id, "Failed")
                print(e.message)


        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     results = executor.map(self._multiprocess_pack, all_packing_groups)
        #     for result in results:
        #         try:
        #             dbh.set_packing_group_status(result, "Packed")
        #         except Exception as e:
        #             print(e)
        #             dbh.set_packing_group_status(result, "Failed")


        all_pgs_after = dbh.get_all_packing_groups()
        for pg in all_pgs_after:
            print(pg["status"])

    def _multiprocess_pack(self, packing_group):
        file_path = self._make_file_path(packing_group)
        packing_group_id = self._pack_maps(file_path, packing_group)
        return packing_group_id

    def _make_file_path(self, packing_group):
        if self.settings["source_path_as_output"]:
            output_file_path = self._make_source_output_file_path(packing_group)
        else:
            output_file_path = self._make_custom_output_file_path(packing_group)
        return output_file_path

    def _make_custom_output_file_path(self, packing_group):
        custom_output_folder = f"{self.output_path}/{packing_group['asset_name']}"
        if not os.path.exists(custom_output_folder):
            os.mkdir(custom_output_folder)

        output_file_path = f"{custom_output_folder}/{packing_group['identifier']}_{packing_group['asset_name']}.{packing_group['extension']}"
        return output_file_path

    def _make_source_output_file_path(self, packing_group):
        source_directory = packing_group["directory"]
        output_file_path = f"{source_directory}/{packing_group['identifier']}_{packing_group['asset_name']}.{packing_group['extension']}"
        return output_file_path

    def _pack_maps(self, output_file_path, packing_group):
        in_channels = self._define_input_texture_channels(packing_group)
        out_channels = self._split_input_textures(in_channels)

        try:
            if len(out_channels) == 3:
                output_texture = self._merge_three(out_channels)
            if len(out_channels) == 4:
                output_texture = self._merge_four(out_channels)

            output_texture.save(output_file_path)
            return packing_group["id"]
        except Exception as e:
            raise PackException(packing_group["id"], e)

    def _merge_four(self, out_channels):
        output_texture = Image.merge(
            "RGBA",
            (
                out_channels[0],
                out_channels[1],
                out_channels[2],
                out_channels[3],
            ),
        )
        return output_texture

    def _merge_three(self, out_channels):
        output_texture = Image.merge(
            "RGB", (out_channels[0], out_channels[1], out_channels[2])
        )
        return output_texture

    def _split_input_textures(self, in_channels):
        out_channels = []
        for in_channel in in_channels:
            in_image = Image.open(in_channel[0])
            split = in_image.split()
            out_channels.append(split[in_channel[1]])
        return out_channels

    def _define_input_texture_channels(self, packing_group):
        in_channels = []
        counter = 0
        previous_texture_type = ""
        for channel in packing_group["channels"]:
            if channel.texture.texture_type == previous_texture_type:
                counter += 1
            else:
                counter = 0

            previous_texture_type = channel.texture.texture_type
            path_and_counter = (channel.texture.path, counter)
            in_channels.append(path_and_counter)
        return in_channels


