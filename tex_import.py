import os
import re
import json
import pickle
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff, EmptyDirectorySnapshot
from pprint import pprint
from PIL import Image


 
"""
1. Search all dirs for changed/added files
    1.1 If data exists, load tree
    1.2 Make new tree of dirs
    1.3 Compare to make new tree of changed dirs
    
2. Create packing groups from changed files
3. Display to user and wait for input
4. Pack textures
5. Import to Unreal

pytest pyside
"""


settings = json.load(open("settings.json"))

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR


def detect_changes(dir):
    """ 
    Takes main directory to search.
    Returns a list of all subdirectories in which changes have been detected. 
    """

    if not os.path.exists("data.P"):
        empty_snap = EmptyDirectorySnapshot()
        snap = DirectorySnapshot(dir)
        diff = DirectorySnapshotDiff(empty_snap, snap)

        with open("data.P", "wb") as f:
            pickle.dump(snap, f)
        
        print_changes(diff)
        return diff

    with open("data.P", "rb") as f:
        o_snap = pickle.load(f)

    snap = DirectorySnapshot(dir)
    diff = DirectorySnapshotDiff(o_snap, snap)
    print_changes(diff)
    return diff


def change_slashes(to_change):
    return [s.replace("\\", "/") for s in to_change]


def print_changes(diff):
    print(bcolors.WARNING + "Directories Modified:")
    print(change_slashes(diff.dirs_modified))
    print("Files Modified:")
    print(change_slashes(diff.files_modified))

    print(bcolors.OK + "Directories Created:")
    print(change_slashes(diff.dirs_created))
    print("Files Created:")
    print(change_slashes(diff.files_created))

    print(bcolors.FAIL + "Directories Deleted:")
    print(change_slashes(diff.dirs_deleted))
    print("Files Deleted:")
    print(change_slashes(diff.files_deleted))

    print(bcolors.RESET)


def pack_maps(output_texture_path, file_list):
    """ 
    Packs 3 or 4 files into a single texture and saves it with a given identifier and extension (set by match group settings).
    Sets channels with missing files to black (user setting?). 
    """

    channels = []
    for file in file_list:
        texture_map = Image.open(file)
        r, *_ = texture_map.split()
        print(im.format, im.size, im.mode)
        r.append(r)

    if len(channels) == 3:
        output_texture = Image.merge("RGB", (channels[0], channels[1], channels[2]))
        with open(output_texture_path, "wb") as f:
            f.write(output_texture)

    if len(channels) == 3:
        output_texture = Image.merge("RGBA", (channels[0], channels[1], channels[2], channels[3]))
        with open(output_texture_path, "wb") as f:
            f.write(output_texture)


def push_maps_to_unreal(list_of_packed_maps):
    pass


def find_groups(diff, packing_group):
    files_to_search = change_slashes(diff.files_created + diff.files_modified)

    groups = {}
    for file in files_to_search:
        file_name = file.split("/")[-1]
        extension = file_name.split(".")[-1]
        identifier = file_name.split("_")[0]
        asset_name = file_name[len(identifier):-len(extension)]

        if extension not in settings["extensions"]:
            continue
        if asset_name not in groups.keys():
            groups[asset_name] = []
        groups[asset_name].append((identifier, extension, file))

    print("Groups:")
    pprint(groups)


diff = detect_changes(settings.get("sync_asset_dir"))
find_groups(diff, settings.get("packing_groups")[0])




