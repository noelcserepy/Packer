from db.alchemy import DatabaseHandler
from watchdog.utils.dirsnapshot import (
    DirectorySnapshot,
    DirectorySnapshotDiff,
    EmptyDirectorySnapshot,
)


class FileSearch:
    def __init__(self, settings):
        self.settings = settings
        self.root_directory = self.settings["search_directory"]
        self.dbh = DatabaseHandler()
        self.latest_snapshot = self._get_latest_snapshot()
        self.new_snapshot = DirectorySnapshot(self.root_directory)
        self._make_snapshot_diff()
        self.file_paths = self._change_slashes(self.snapshot_diff.files_created)
        self.dbh.save_snapshot(self.new_snapshot)
        self.dbh.print_snapshots()

    def _make_snapshot_diff(self):
        if self.latest_snapshot:
            self.snapshot_diff = DirectorySnapshotDiff(
                self.latest_snapshot, self.new_snapshot
            )
        else:
            empty_snapshot = EmptyDirectorySnapshot()
            self.snapshot_diff = DirectorySnapshotDiff(
                empty_snapshot, self.new_snapshot
            )

    def _get_latest_snapshot(self):
        try:
            latest_snapshot = self.dbh.get_last_snapshot()
            return latest_snapshot
        except:
            return None

    def _change_slashes(self, to_change):
        return [s.replace("\\", "/") for s in to_change]

    def _print_found_files(self, diff):
        ok = "\033[92m"  # GREEN
        warning = "\033[93m"  # YELLOW
        fail = "\033[91m"  # RED
        reset = "\033[0m"  # RESET COLOR

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
