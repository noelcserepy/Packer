import os
import pickle
from tex_import.helpers import Helpers
from watchdog.utils.dirsnapshot import (
    DirectorySnapshot, 
    DirectorySnapshotDiff, 
    EmptyDirectorySnapshot
)



class TextureSearch():
    def __init__(self, settings):
        self.settings = settings


    def get_asset_files(self):
        diff = self.detect_changes(self.settings["sync_asset_dir"])
        files_to_search = Helpers().change_slashes(diff.files_created + diff.files_modified)
        asset_files = self.get_files_by_asset(files_to_search)
        return asset_files


    def detect_changes(self, dir):
        """ 
        Takes main directory to search.
        Returns <class 'watchdog.utils.dirsnapshot.DirectorySnapshotDiff'> containing all subdirectories in which changes have been detected. 
        """
        if not os.path.exists("data.P"):
            empty_snap = EmptyDirectorySnapshot()
            snap = DirectorySnapshot(dir)
            diff = DirectorySnapshotDiff(empty_snap, snap)
            # with open("data.P", "wb") as f:
            #     pickle.dump(snap, f)
            Helpers().print_changes(diff)
            return diff

        with open("data.P", "rb") as f:
            o_snap = pickle.load(f)

        snap = DirectorySnapshot(dir)
        diff = DirectorySnapshotDiff(o_snap, snap)

        Helpers().print_changes(diff)
        return diff


    def get_all_files(self, dir, all_files):
        """ Gets all files in a given directory """
        dir_files = [f"{dir}/{x}" for x in os.listdir(dir)]
        for file in dir_files:
            print(file)
            if os.path.isdir(file):
                self.get_all_files(file, all_files)
            elif os.path.isfile(file):
                all_files.append(file)
        return all_files


    def _identify_texture(self, file):
        """ 
        Takes in full file path. If file is a texture specified by settings, return a dict of information about that texture.
        """
        filename_full = file.split("/")[-1]
        filename, extension = filename_full.split(".")
        directory = file[:-len(filename_full)]

        for tex in self.settings["textures"]:
            if extension.upper() not in tex["extensions"]:
                continue
            pref_id = tex["preferred_identifier"]
            for id in tex["identifiers"]:
                if id[1] == "end":
                    if filename.endswith(id[0]):
                        asset_name = filename[:-len(id[0])]
                        if pref_id[1] == "start":
                            new_filename = f"{pref_id[0]}{asset_name}"
                        if pref_id[1] == "end":
                            new_filename = f"{asset_name}{pref_id[0]}"
                        new_full_filename = f"{new_filename}.{extension}"
                        texture = {
                            "asset_name": asset_name,
                            "path": file,
                            "dir": directory,
                            "current_filename": filename_full,
                            "preferred_filename": new_full_filename,
                            "texture_type": tex["name"]
                        }
                        return texture

                if id[1] == "start":
                    if filename.startswith(id[0]):
                        asset_name =filename[len(id[0]):]
                        if pref_id[1] == "start":
                            new_filename = f"{pref_id[0]}{asset_name}"
                        if pref_id[1] == "end":
                            new_filename = f"{asset_name}{pref_id[0]}"
                        new_full_filename = f"{new_filename}.{extension}"
                        texture = {
                            "asset_name": asset_name,
                            "path": file,
                            "dir": directory,
                            "current_filename": filename_full,
                            "preferred_filename": new_full_filename,
                            "texture_type": tex["name"]
                        }
                        return texture


    def get_files_by_asset(self, files):
        """ 
        Takes a list of files.
        Returns dictionary of assets, each with a list of textures belonging to that asset e.g. {asset_name: [available textures]}.
        """
        asset_files = {}
        for file in files:
            try:
                texture = self._identify_texture(file)
                if not texture:
                    raise Exception("Texture does not exist")
                
                asset_name = texture["asset_name"]
                if asset_name not in asset_files.keys():
                    asset_files[asset_name] = []

                asset_files[asset_name].append(texture)
            except:
                continue
        return asset_files


    


