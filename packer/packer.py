import json
from packer.packinggroup import PackingGroup
from packer.filesearch import FileSearch


with open("settings.json", "r") as f:
    settings = json.load(f)
ft = FileSearch(settings)
pk = PackingGroup(settings)


def startup():
    asset_files = ft.get_asset_files()
    pk.create_packing_groups(asset_files)


def refresh():
    pass


def pack():
    p_groups = json.load(open("pgroups.json"))
    pk.output_maps(p_groups)


