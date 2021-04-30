import os
import json
import pickle
from pprint import pprint
from PIL import Image
from tex_import.texture_search import TextureSearch
from watchdog.utils.dirsnapshot import (
    DirectorySnapshot, 
    DirectorySnapshotDiff, 
    EmptyDirectorySnapshot
)


 
"""
1. Search all dirs for changed/added files    
2. Find textures within those files
3. Create packing groups from changed files
4. Pack textures
5. Import to Unreal
"""


settings = json.load(open("settings.json"))

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR


def get_asset_files():
    diff = detect_changes(settings["sync_asset_dir"])
    files_to_search = change_slashes(diff.files_created + diff.files_modified)
    ts = TextureSearch(settings)
    asset_textures = ts.get_files_by_asset(files_to_search)
    pprint(asset_textures)
    return asset_textures


def detect_changes(dir):
    """ 
    Takes main directory to search.
    Returns <class 'watchdog.utils.dirsnapshot.DirectorySnapshotDiff'> containing all subdirectories in which changes have been detected. 
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


def pack_maps(output_texture_path, file_list):
    """ 
    Packs 3 or 4 files into a single texture and saves it with a given identifier and extension (set by match group settings).
    Sets channels with missing files to black (user setting?). 
    """

    channels = []
    for file in file_list:
        texture_map = Image.open(file)
        r, *_ = texture_map.split()
        print(r.format, r.size, r.mode)
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


def change_slashes(to_change):
    return [s.replace("\\", "/") for s in to_change]


def print_changes(diff):
    """ 
    Takes <class 'watchdog.utils.dirsnapshot.DirectorySnapshotDiff'> 
    Prints all the changes in directory structure since last time directories were saved with nice colours. 
    """
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

def get_all_files(dir, all_files):
        """ Gets all files in a given directory """
        dir_files = [f"{dir}/{x}" for x in os.listdir(dir)]
        for file in dir_files:
            print(file)
            if os.path.isdir(file):
                get_all_files(file, all_files)
            elif os.path.isfile(file):
                all_files.append(file)
        return all_files