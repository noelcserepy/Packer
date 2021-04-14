import os
import json



# To be replaced with inputs from tex_import.py
settings = json.load(open("settings.json"))
dir = settings["sync_asset_dir"]
valid_extensions = settings["extensions"]
default_replacements = settings["default_replacements"]


class RenameError(Exception):
    """ Base error class for formatting errors """


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


def format_filename_identifiers(file, replacements):
    """ Replaces existing identifier of given file with desired identifier of that filetype e.g. "Roughness_Chair" or "Chair_r" -> "R_Chair".  """
    filename_full = file.split("/")[-1]
    filename, extension = filename_full.split(".")
    directory = file[:-len(filename_full)]

    if extension not in valid_extensions:
        raise RenameError("While formatting file, detected invalid file extension.")

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


def format_paths(paths, replacements=default_replacements):
    """ Calls format_filename_identifiers() for every element of list of paths. """
    new_paths = []
    for file in paths:
        try:
            new_path = format_filename_identifiers(file, replacements)
            if not new_path:
                raise RenameError("New path does not exist-")
            new_paths.append(new_path)
        except:
            continue
    return new_paths


def format_all_files_in_dir(dir):
    all_files = []
    get_all_files(dir, all_files)
    new_paths = format_paths(all_files)
    return new_paths

