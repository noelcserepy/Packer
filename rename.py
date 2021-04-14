import os
import json



# To be replaced with inputs from tex_import.py
settings = json.load(open("settings.json"))
dir = settings["sync_asset_dir"]
valid_extensions = settings["extensions"]
replacements = [
    ("_c", "D_", "end"),
    ("_r", "R_", "end"),
    ("_o", "AO_", "end"),
    ("_m", "M_", "end"),
    ("_n", "N_", "end"),
    ("Metallic_", "M_", "start"),
    ("Roughness_", "R_", "start"),
    ("Albedo_", "A_", "start"),
    ("Normal_", "N_", "start"),
]


class RenameError(Exception):
    """ Base error class for formatting errors """

class InvalidExtensionError(RenameError):
    """ While formatting file, detected invalid file extension. """


def format_filename(file, replacements):
    filename_full = file.split("/")[-1]
    filename, extension = filename_full.split(".")
    directory = file[:-len(filename_full)]

    if extension not in valid_extensions:
        raise InvalidExtensionError()

    for rep in replacements:
        if rep[2] == "end":
            if filename.endswith(rep[0]):
                    new_filename = f"{rep[1]}{filename[:-len(rep[0])]}"
                    new_path = f"{directory}{new_filename}.{extension}"
                    
                    return new_path

        if rep[2] == "start":
            if filename.startswith(rep[0]):
                    new_filename = f"{rep[1]}{filename[len(rep[0]):]}"
                    new_path = f"{directory}{new_filename}.{extension}"
                    
                    return new_path


def get_all_files(dir, all_files):
    dir_files = [f"{dir}/{x}" for x in os.listdir(dir)]
    for file in dir_files:
        print(file)
        if os.path.isdir(file):
            get_all_files(file, all_files)
        elif os.path.isfile(file):
            all_files.append(file)

    return all_files


def get_renamed_files(dir_files):
    for file in dir_files:
        try:
            new_path = format_filename(file, replacements)
            print(file)
            print(new_path)
        except:
            continue


def rename_all_files(dir):
    all_files = []
    get_all_files(dir, all_files)
    get_renamed_files(all_files)

