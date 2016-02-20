# Unsafe-SARC-Extractor
This programs allows you to extract SARC files and use SAHT files to find their real names. It must be used with Python 3 (Python 2 gives errors). This has been tested on both Windows and Linux.

### Usage

```
usage: main.py [-h] [--SAHT SAHT] SARC

This program can extract 'unsafe' SARC files

positional arguments:
  SARC         put the location of the SARC file. This is an official Nintendo
               container format used to store game files in.

optional arguments:
  -h, --help   show this help message and exit
  --SAHT SAHT  Put the location of the SAHT file. These files contain the real
               file names for the hashes
```
If you don't put in a SAHT file or if the hash is not in the SAHT file, the file will be named by it's hash instead.

##Credits
Gericom: For EveryFileExplorer (I used the source code to figure out the the SAHT format) and the HashTable.saht

Pabloh&g and Mkgirlism: For the leaked Nintendo sdk (Allows me to understand the format more better)

ObsidianX: For the documentation on the SARC files on 3dbrew

