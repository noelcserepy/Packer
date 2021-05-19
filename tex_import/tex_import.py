import json
from tex_import.packer import Packer
from tex_import.texture_search import TextureSearch


def main():
    settings = json.load(open("settings.json"))

    ft = TextureSearch(settings)
    asset_files = ft.get_asset_files()

    pk = Packer(settings)
    pk.create_packing_groups(asset_files)
