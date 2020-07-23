# Lightroom Reader
import sys
from argparse import ArgumentParser
import sqlite3

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

SQL_SELECT = """
SELECT
  root.name AS root_name,
  folder.pathFromRoot AS folder_path_from_root,
  file.originalFilename AS file_original_name,
  root.absolutePath AS root_absolute_path,
  root.relativePathFromCatalog AS root_rel_path_from_catalog,
  file.baseName AS file_base_name,
  file.extension AS file_extension,
  root.id_local AS root_id,
  folder.id_local AS folder_id,
  file.id_local AS file_id
FROM AgLibraryRootFolder root
JOIN AgLibraryFolder folder ON root.id_local = folder.rootFolder
JOIN AgLibraryFile file ON folder.id_local = file.folder
ORDER BY root.name, folder.pathFromRoot, file.originalFilename;
"""

class LightroomFileFinder():
    db = None
    cursor = None
    path = None
    verbose = None

    def __init__(self, path, verbose=False):
        self.path = path
        self.verbose = verbose

    def __iter__(self):
        try:
            self.db = sqlite3.connect(self.path_to_uri(self.path), uri=True)
        except:
            if self.verbose:
                e = sys.exc_info()[0]
                print(f"\nException: {e}", file=sys.stderr)
                print(f"Invalid path, permission or lock: {self.path}\n", file=sys.stderr)
            raise ValueError(f"Invalid path, permission or lock: {self.path}\n")
        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(SQL_SELECT)
        except:
            if self.verbose:
                e = sys.exc_info()[0]
                print(f"\nException: {e}", file=sys.stderr)
                print(f"Database/table Problem: {self.path}\n", file=sys.stderr)
            raise RuntimeError(f"Database/table Problem: {self.path}\n")

        return self

    def __next__(self):
        try:
            row = self.cursor.fetchone()
        except:
            if self.verbose:
                e = sys.exc_info()[0]
                print(f"\nException: {e}", file=sys.stderr)
                print(f"Row Fetch Problem: {self.path}\n", file=sys.stderr)
            raise RuntimeError(f"Row Fetch Problem: {self.path}\n")
        if row is None:
            raise StopIteration
        return dict_factory(self.cursor, row)

    def path_to_uri(self, path):
        return 'file:' + str(path) + '?mode=ro'


def main():
    parser = ArgumentParser(
            description="Lightroom Reader - Search for image files in Lightroom SQLite DB and output records with useful info."
        )
    parser.add_argument(
            "path",
            nargs=1,
            help="Relative or absolute path to a Lightroom SQLite database."
        )
    parser.add_argument("--full", help="Print full record, default is partial record printing", action="store_true")
    parser.add_argument("-v", "--verbose", help="Enable verbose mode", action="store_true")
    args = vars(parser.parse_args())

    if args['verbose']:
        print("path:", args['path'][0], file=sys.stderr)
        print("full:", args['full'], file=sys.stderr)
        print("verbose:", args['verbose'], file=sys.stderr)

    lrff = LightroomFileFinder(args['path'][0], args['verbose'])

    for record in lrff:
        if args['full']:
            print(record)
        else:
            print(f"{record['root_name']}/{record['folder_path_from_root']}{record['file_original_name']}")


if __name__ == "__main__":
    main()
