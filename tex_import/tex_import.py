import json
from tex_import.packer import Packer
from tex_import.texture_search import TextureSearch


settings = json.load(open("settings.json"))
ft = TextureSearch(settings)
pk = Packer(settings)


def startup():
    asset_files = ft.get_asset_files()
    pk.create_packing_groups(asset_files)


def refresh():
    pass


def pack():
    p_groups = json.load(open("pgroups.json"))
    pk.output_maps(p_groups)


