import os
import pickle
from datetime import datetime
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
        diff = self.detect_directory_changes(self.settings["sync_asset_dir"])
        files_to_search = Helpers().change_slashes(diff.files_created + diff.files_modified)
        asset_files = self.get_files_by_asset(files_to_search)
        return asset_files


    def detect_directory_changes(self, dir):
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
            if os.path.isdir(file):
                self.get_all_files(file, all_files)
            elif os.path.isfile(file):
                all_files.append(file)
        return all_files


    def get_files_by_asset(self, files):
        """ 
        Takes a list of files.
        Returns dictionary of assets, each with a list of textures belonging to that asset e.g. {asset_name: [available textures]}.
        """
        asset_files = {}
        for file in files:
            try:
                texture = Texture(self.settings, file).get_texture_data()
                if not texture:
                    raise Exception("Texture does not exist")
                
                asset_name = texture["asset_name"]
                if asset_name not in asset_files.keys():
                    asset_files[asset_name] = []

                asset_files[asset_name].append(texture)
            except:
                continue
        return asset_files


    
class Texture():
    def __init__(self, settings, path):
        self.path = path
        self.settings = settings
        self.filename_full = self.path.split("/")[-1]
        self.filename, self.extension = self.filename_full.split(".")
        self.directory = self.path[:-len(self.filename_full)]
        self.scan_timestamp = datetime.now().timestamp()
        self.asset_name = str()
        self.preferred_filename = str()
        self.texture_type = str()
        self.preferred_identifier = str()

        self._identify_texture()

        
    def _identify_texture(self):
        for tex in self.settings["textures"]:
            self.texture_type = tex["name"]
            if self.extension.upper() not in tex["extensions"]:
                continue
            self.preferred_identifier = tex["preferred_identifier"]
            for id in tex["identifiers"]:
                self._differentiate_start_and_end(id)


    def _differentiate_start_and_end(self, id):
        if id[1] == "end":
            if self.filename.endswith(id[0]):
                self.asset_name = self.filename[:-len(id[0])]
                self._create_preferred_filename(self.preferred_identifier, self.asset_name)
        if id[1] == "start":
            if self.filename.startswith(id[0]):
                self.asset_name = self.filename[len(id[0]):]
                self._create_preferred_filename(self.preferred_identifier, self.asset_name)


    def _create_preferred_filename(self, preferred_identifier, asset_name):
        if preferred_identifier[1] == "start":
            new_filename = f"{preferred_identifier[0]}{asset_name}"
        if preferred_identifier[1] == "end":
            new_filename = f"{asset_name}{preferred_identifier[0]}"
        self.preferred_filename = f"{new_filename}.{self.extension}"


    def get_texture_data(self):
        texture_data = {
            "asset_name": self.asset_name,
            "path": self.path,
            "dir": self.directory,
            "current_filename": self.filename_full,
            "preferred_filename": self.preferred_filename,
            "texture_type": self.texture_type,
            "scan_timestamp": self.scan_timestamp
        }
        print(texture_data)
        return texture_data