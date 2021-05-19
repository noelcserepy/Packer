import os
import json
import pickle
from tex_import.texture_search import TextureSearch
from tex_import.helpers import Helpers
from watchdog.utils.dirsnapshot import (
    DirectorySnapshot, 
    DirectorySnapshotDiff, 
    EmptyDirectorySnapshot
)



class FileTool():
    def __init__(self, settings):
        self.settings = settings

    def get_asset_files(self):
        diff = self.detect_changes(self.settings["sync_asset_dir"])
        files_to_search = Helpers().change_slashes(diff.files_created + diff.files_modified)
        ts = TextureSearch(self.settings)
        asset_files = ts.get_files_by_asset(files_to_search)
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