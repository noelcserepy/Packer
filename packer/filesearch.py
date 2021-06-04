from watchdog.utils.dirsnapshot import (
    DirectorySnapshot, 
    DirectorySnapshotDiff, 
    EmptyDirectorySnapshot
)



class FileSearch():
    def __init__(self, settings):
        self.settings = settings
        self.root_directory = self.settings["sync_asset_dir"]
        self.all_directory_file_paths = list()

        self.find_all_files()


    def find_all_files(self):
        empty_snapshot = EmptyDirectorySnapshot()
        snapshot = DirectorySnapshot(self.root_directory)
        snapshot_diff = DirectorySnapshotDiff(empty_snapshot, snapshot)
        self._print_found_files(snapshot_diff)
        self.all_directory_file_paths = self._change_slashes(snapshot_diff.files_created)


    def _change_slashes(self, to_change):
        return [s.replace("\\", "/") for s in to_change]


    def _print_found_files(self, diff):
        """ 
        Takes <class 'watchdog.utils.dirsnapshot.DirectorySnapshotDiff'> 
        Prints all the changes in directory structure since last time directories were saved with nice colours. 
        """
        ok = '\033[92m' #GREEN
        warning = '\033[93m' #YELLOW
        fail = '\033[91m' #RED
        reset = '\033[0m' #RESET COLOR

        print(warning + "Directories Modified:")
        print(self._change_slashes(diff.dirs_modified))
        print("Files Modified:")
        print(self._change_slashes(diff.files_modified))

        print(ok + "Directories Created:")
        print(self._change_slashes(diff.dirs_created))
        print("Files Created:")
        print(self._change_slashes(diff.files_created))

        print(fail + "Directories Deleted:")
        print(self._change_slashes(diff.dirs_deleted))
        print("Files Deleted:")
        print(self._change_slashes(diff.files_deleted))

        print(reset)


    # def detect_directory_changes(self):
        # if not os.path.exists("data.P"):
        #     empty_snap = EmptyDirectorySnapshot()
        #     snap = DirectorySnapshot(self.root_directory)
        #     diff = DirectorySnapshotDiff(empty_snap, snap)
        #     with open("data.P", "wb") as f:
        #         pickle.dump(snap, f)
        #     Helpers().print_changes(diff)
        #     return diff

        # with open("data.P", "rb") as f:
        #     o_snap = pickle.load(f)

        # snap = DirectorySnapshot(self.root_directory)
        # Helpers().print_changes(diff)
        # return diff