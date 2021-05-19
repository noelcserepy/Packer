import os



class Helpers():
    def __init__(self):
        self.ok = '\033[92m' #GREEN
        self.warning = '\033[93m' #YELLOW
        self.fail = '\033[91m' #RED
        self.reset = '\033[0m' #RESET COLOR


    def change_slashes(self, to_change):
        return [s.replace("\\", "/") for s in to_change]


    def print_changes(self, diff):
        """ 
        Takes <class 'watchdog.utils.dirsnapshot.DirectorySnapshotDiff'> 
        Prints all the changes in directory structure since last time directories were saved with nice colours. 
        """
        print(self.warning + "Directories Modified:")
        print(self.change_slashes(diff.dirs_modified))
        print("Files Modified:")
        print(self.change_slashes(diff.files_modified))

        print(self.ok + "Directories Created:")
        print(self.change_slashes(diff.dirs_created))
        print("Files Created:")
        print(self.change_slashes(diff.files_created))

        print(self.fail + "Directories Deleted:")
        print(self.change_slashes(diff.dirs_deleted))
        print("Files Deleted:")
        print(self.change_slashes(diff.files_deleted))

        print(self.reset)
