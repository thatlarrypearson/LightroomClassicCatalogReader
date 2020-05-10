# Lightroom Classic Catalog Image File Reader

The program, ```lr_reader.py```, will extract and output image file data from Lightroom Classic databases.

The program and associated class ```LightroomFileFinder``` uses the [SQLite library](https://docs.python.org/3/library/sqlite3.html) included in most Python 3 distributions.  Normally, other than Python 3.6 and newer, no additional software would need to be installed.

## Installation

### Developer Mode Install

Developers who wish to modify the code can clone from ```github``` and install with pip.  This enables changes made in the code to appear immediately as though they were happening in the library.

```bash
python3.8 -m pip install pip --upgrade
python3.8 -m pip install setuptools --upgrade
python3.8 -m pip install wheel --upgrade
git clone https://github.com/thatlarrypearson/LightroomClassicCatalogReader.git
cd LightroomClassicCatalogReader
python3.8 -m pip install -e .
```

### Check Installation

Launch the ```python``` interpreter ```python3.8``.`

```python
from lr_reader import LightroomFileFinder
```

An alternative to the above approach is to simply run the program as shown below.

```PowerShell
python3.8 -m lr_reader --help
```

If this doesn't error out then you are installed!

## Lightroom Classic Catalog Image File Reader Program

### USAGE

```PowerShell
PS Lightroom\src> python3.8 -m lr_reader --help
usage: lr_reader.py [-h] [--full] [-v] path

Lightroom Reader - Search for image files in Lightroom SQLite DB and output records with useful info.

positional arguments:
  path           Relative or absolute path to a Lightroom SQLite database.

optional arguments:
  -h, --help     show this help message and exit
  --full         Print full record, default is partial record printing
  -v, --verbose  Enable verbose mode
PS Lightroom\src>
```

### OUTPUT

Program output is either a python dictionary coverted to text or a file name including relative path.  Below are samples of output.

#### Sample Partial Output Lines (```--full``` was not specified)

> Windows 10 Users may notice that ```lr_reader.py``` output uses ```/``` instead of ```\``` for directory path separators.  That is because Lightroom uses the Unix/Linux/Mac directory path separator convention ```/```.

```text
2019/2019-12-29/20191229-2019-12-29 08.20.46.png
2019/2019-12-29/20191229-2019-12-29 08.35.47.png
2019/2019-12-29/20191229-2019-12-29 08.36.06.png
2019/2019-12-29/20191229-2019-12-29 18.54.43.png
2019/2019-12-29/20191229-2019-12-29 18.54.57.png
2019/2019-12-31/20191231-2019-12-31 12.22.03.png
```

#### Sample Full Output Line (```--full``` was specified)

```text
{'root_id': 53016, 'folder_id': 53019, 'file_id': 53102, 'root_absolute_path': 'C:/Users/human/Pictures/2010/', 'root_name': '2010', 'root_rel_path_from_catalog': '../2010/', 'folder_path_from_root': '2010-05-04/', 'file_base_name': '20100504-IMG_7360', 'file_extension': 'CR2', 'file_original_name': '20100504-IMG_7360.CR2'}
```

#### Fields

* ```root_name``` is often something like ```2019``` but can be different if the Lightroom owner has chosen a different way of cataloging photos/videos.

* ```folder_path_from_root``` is the directory or directories between the image/video file and the root folder.  Using ```C:\Users\human\Pictures\2019\2019-12-31\20191231-2019-12-31 12.22.03.png``` as an example, the folder path from root is the portion ```2019-12-31\``` because the root name is ```2019``` and the absolute root path is ```C:\Users\human\Pictures\2019```.

* ```root_absolute_path``` is the full path of the root Lightroom Classic folder on the host system.  E.g. on Windows 10, it might be something like ```C:\Users\human\Pictures\2019``` for photos/videos taken in 2019.

* ```file_original_name``` is the original file name assigned by Lightroom Classic when the image/video was first imported.

* ```root_rel_path_from_catalog``` on my system is usually something like ```..\2019``` assuming the photo was taken in 2019.  This is because the ```folder``` is in ```C:\Users\human\Pictures``` and the catalogs are in ```C:\Users\human\Pictures\Lightroom```.  This changes when images/movies have been migrated to another drive (E.g. F:\) attached to the system.  When Lightroom Classic users store some portion of their catalog on external USB drives, this value will reflect the relative directory path all the way to the folder containing pictures on that drive.  Something like ```..\..\..\..\F:\```.  These are Windows 10 examples.  On an Apple Mac system, ```\```'s become ```/```'s and the drives won't have letters.

* ```file_base_name``` is the file name given image and video files on import into Lightroom Classic.  These are generally not the exact same file name of the image/movie as it came out of the camera but they will be similar.

* ```file_extension``` will be a file extension associated with either an image or movie file.  E.e. ```.jpg```, ```.gif```, ```.png```, ```.CR2``` and ```.MOV```.

* ```root_id```, ```folder_id``` and ```file_id``` are the primary key values uniquely identifying the specific row in each of the three database tables used to compile this line of output.

## Lightroom Classic Catalog Image File Reader Class

### ```LightroomFileFinder(path, verbose=False)```

The ```LightroomFileFinder``` class implements an iterator (used in ```for``` loops) returning a dictionary representing a image file information found in the database.  See programing example below.

* ```path``` can be relative or absolute and includes the database file name.  E.g. ```Lightroom 5 Catalog.lrcat```, ```C:\Users\human\Pictures\Lightroom\Lightroom Catalog-2.lrcat``` and ```..\..\Pictures\Lightroom\Lightroom Catalog.lrcat```.

  > When working in Python on Windows systems, don't forget to escape the ```\``` character.  E.g. ```C:\\Users\\human\\Pictures\\Lightroom\\Lightroom Catalog-2.lrcat```.

* ```verbose``` defaults to False.  When set to True, additional error information is provided that may better show underlying failer causes.

### Error Handling

#### Specified Lightroom Classic Catalog File Doesn't Exist

* ```ValueError``` Exception.

#### Required Tables Missing From Lightroom Classic Catalog File

* ```RuntimeError``` Exception.

#### Database Files Locked By Running Lightroom Classic Program

> NOTE:
> Before mucking around with Lightroom Classic ```.lrcat``` files, make copies of the files and then work from the copies.

* ```ValueError``` Exception.

#### Unknown Error When Reading Records From Database

* ```RuntimeError``` Exception.

### Python 3 Programming Example

```python
from lr_reader import LightroomFileFinder

lightroom_reader = LightroomFileFinder('Pictures\\Lightroom\\Lightroom 5 Catalog.lrcat')

for record in lightroom_reader():
  print(record)
```

## Exploring Lightroom Classic SQLite Schema With Command Line Tools

SQLite command line tools are available from [SQLite](https://sqlite.org).  These tools were used to identify database table structure for data related to image files.

> NOTE:
> Before mucking around with Lightroom Classic ```.lrcat``` files, make copies of the files and then work from the copies.

```bash
SQLite3 Command Line Tools
$ sqlite3
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen a persistent database.
sqlite> .shell dir
 Volume in drive L is WD-931GB
 Volume Serial Number is 46EE-388C

 Directory of L:\Lightroom\catalogs

05/03/2020  10:06 AM    <DIR>          .
05/03/2020  10:06 AM    <DIR>          ..
12/22/2019  09:01 PM        16,502,784 Lightroom Catalog-4.lrcat
12/22/2019  08:59 PM        25,022,464 Lightroom 5 Catalog.lrcat
11/01/2019  08:14 PM       726,310,912 Lightroom Catalog.lrcat
05/02/2020  02:06 PM       755,748,864 Lightroom Catalog-2.lrcat
12/22/2019  08:58 PM       736,919,552 Lightroom Catalog-3.lrcat
               5 File(s)  2,260,504,576 bytes
               2 Dir(s)  997,888,884,736 bytes free
sqlite> .open 'Lightroom Catalog-2.lrcat'
sqlite> .databases
main: L:\Lightroom\catalogs\Lightroom Catalog-2.lrcat
sqlite> .schema main.* --indent
CREATE TABLE Adobe_variablesTable(
  id_local INTEGER PRIMARY KEY,
  id_global UNIQUE NOT NULL,
  name,
  type,
  value NOT NULL DEFAULT ''
);
CREATE TABLE Adobe_variables(
  id_local INTEGER PRIMARY KEY,
  id_global UNIQUE NOT NULL,
  name,
  value
);

. . .
. . .
. . .


/* fsdir(name,mode,mtime,data) */;
/* fts3tokenize(input,token,start,"end",position) */;
/* json_each("key",value,type,atom,id,parent,fullkey,path) */;
/* json_tree("key",value,type,atom,id,parent,fullkey,path) */;
/* pragma_database_list(seq,name,file) */;
/* pragma_module_list(name) */;
/* sqlite_dbdata(pgno,cell,field,value) */;
/* sqlite_dbpage(pgno,data) */;
/* sqlite_dbptr(pgno,child) */;
/* sqlite_stmt(sql,ncol,ro,busy,nscan,nsort,naidx,nstep,reprep,run,mem) */;
/* zipfile(name,mode,mtime,sz,rawdata,data,method) */;
sqlite>
sqlite> .once '..\\lrcat-2.schema'
sqlite> .schema main.* --indent
sqlite>
```

> NOTE: On Windows 10, the following ```.shell dir ..``` caused BitDefender antivirus software to freakout and kill ```sqlite3``` command and all of its helping tools.  Turning off the antivirus software was a temporary solution.

```bash
sqlite> .shell dir ..
 Volume in drive L is WD-931GB
 Volume Serial Number is 46EE-388C

 Directory of L:\Lightroom

05/03/2020  10:06 AM    <DIR>          .
05/03/2020  10:06 AM    <DIR>          ..
05/03/2020  10:06 AM    <DIR>          catalogs
05/03/2020  11:06 AM            52,679 lrcat-2.schema
               1 File(s)         52,679 bytes
               3 Dir(s)  997,887,836,160 bytes free
sqlite> sqlite> .once '..\\lrcat-2.dump'
sqlite> .dump
sqlite> .shell dir ..
 Volume in drive L is WD-931GB
 Volume Serial Number is 46EE-388C

 Directory of L:\Lightroom

05/03/2020  10:06 AM    <DIR>          .
05/03/2020  10:06 AM    <DIR>          ..
05/03/2020  10:06 AM    <DIR>          catalogs
05/03/2020  11:06 AM            52,679 lrcat-2.schema
05/03/2020  11:20 AM       872,552,457 lrcat-2.dump
               2 File(s)    872,605,136 bytes
               3 Dir(s)  997,013,323,776 bytes free

sqlite> .excel
sqlite> SELECT * FROM agLibraryFile;
sqlite> .excel
sqlite> SELECT * FROM agLibraryFolder;
sqlite>
sqlite> .quit
$
```

## Table Definitions For Tables Used In This Software

```SQL
CREATE TABLE AgLibraryRootFolder(
  id_local INTEGER PRIMARY KEY,
  id_global UNIQUE NOT NULL,
  absolutePath UNIQUE NOT NULL DEFAULT '',
  name NOT NULL DEFAULT '',
  relativePathFromCatalog
);
CREATE TABLE AgLibraryFolder(
  id_local INTEGER PRIMARY KEY,
  id_global UNIQUE NOT NULL,
  parentId INTEGER,
  pathFromRoot NOT NULL DEFAULT '',
  rootFolder INTEGER NOT NULL DEFAULT 0,
  visibility INTEGER
);
CREATE TABLE AgLibraryFile(
  id_local INTEGER PRIMARY KEY,
  id_global UNIQUE NOT NULL,
  baseName NOT NULL DEFAULT '',
  errorMessage,
  errorTime,
  extension NOT NULL DEFAULT '',
  externalModTime,
  folder INTEGER NOT NULL DEFAULT 0,
  idx_filename NOT NULL DEFAULT '',
  importHash,
  lc_idx_filename NOT NULL DEFAULT '',
  lc_idx_filenameExtension NOT NULL DEFAULT '',
  md5,
  modTime,
  originalFilename NOT NULL DEFAULT '',
  sidecarExtensions
);
```

## Join Statement For Getting Files

```SQL
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
ORDER BY ORDER BY root.name, folder.pathFromRoot, file.originalFilename;
```

## Example Linux/Mac Shell Commands To Find All Image File Names Contained in Multiple Lightroom Classic Catalogs

```bash
#!/bin/bash

for db in Lightroom*.lrcat
do
  python3.8 lr_reader.py --verbose "${db}"
done | sed 's/F:\/Pictures\///g' | sed 's/F:\///g' | sort -u | tee image-files.txt
```

After copying each of the Lightroom Classic ```.lrcat``` catalog files in ```C:\Users\human\Pictures\Lightroom``` to another directory, the above Linux shell commands were run against the catalog file copies.  The goal was to clean up the data and remove duplicate file names from the combined output of multiple Lightroom catalog files.

The script logic goes something like this:

* For each of the Lightroom catalog database files run the ```lr_reader.py``` program on the current catalog file.
* Take all of the output from each ```lr_reader.py``` run and remove every instance of the string ```F:\Picture\``` from the output.
* Taking the output from the first ```sed``` command, have the second ```sed``` command remove every instance of the string ```F:\``` from the output.
* Takeing the output from the second ```sed``` command, sort all of the file names and remove any duplicate entries so that each file name in the output is unique.
* Finally, send the output from the ```sort``` command to both the screen and the file ```image-files.txt```.
