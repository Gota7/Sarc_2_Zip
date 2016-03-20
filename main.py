from sarc import *
from saht import *
from misc import *
import os
import argparse
import glob

parser = argparse.ArgumentParser(description='This program can extract both \'safe\''
                                             'and \'unsafe\' SARC files. By default, the'
                                             'endian is set to little endian for the 3DS files')
parser.add_argument("SARC", help="put the location of the SARC file. "
                                 "This is an official Nintendo container format"
                                 " used to store game files in.", type=str)
parser.add_argument("--SAHT", help="Put the location of the SAHT file. "
                                   "These files contain the real file names"
                                   " for the hashes", type=str)
parser.add_argument("-b", "--Big", help="Set the endian to big endian. (Wii U SARC files "
                               "are big endian while 3DS SARC files are little "
                               "endian.", action="store_true")
parser.parse_args()
args = parser.parse_args()

if args.Big:
    inputendian = '>'
else:
    inputendian = '<'

for currentInput in glob.glob(args.SARC):
    memorySARCDatabase = {}
    nintendoSarc.extract(currentInput, memorySARCDatabase, inputendian)
    mainRootPath = currentInput + '.d'
    os.mkdir(mainRootPath)

    print("")
    print(memorySARCDatabase.keys())
    for key in memorySARCDatabase.keys():
        FileData = memorySARCDatabase[key]["Data"]
        if 'String' in memorySARCDatabase[key]:
            FileNameValue = memorySARCDatabase[key]['String']['File']
            if "Dir" in memorySARCDatabase[key]['String']:
                DirNameValue = memorySARCDatabase[key]['String']["Dir"]
                CreateDirOnlyIfNoneExist(os.path.join(mainRootPath, DirNameValue))
                path = os.path.join(mainRootPath, DirNameValue, FileNameValue)
                Writefile(path, FileData)
            else:
                path = os.path.join(mainRootPath, FileNameValue)
                Writefile(path, FileData)
            print(path)

        elif args.SAHT:
            memorySAHTDatabase = {}
            thirdpartySAHT.extract(args.SAHT, memorySAHTDatabase)
            if key in memorySAHTDatabase.keys():
                FileNameValue = memorySAHTDatabase[key]["File Name"]
                if "Directory Name" in memorySAHTDatabase[key]:
                    DirNameValue = memorySAHTDatabase[key]["Directory Name"]
                    CreateDirOnlyIfNoneExist(os.path.join(mainRootPath, DirNameValue))
                    path = os.path.join(mainRootPath, DirNameValue, FileNameValue)
                    Writefile(path, FileData)
                else:
                    path = os.path.join(mainRootPath, FileNameValue)
                    Writefile(path, FileData)
                print(path)
            else:
                path = os.path.join(mainRootPath, key)
                Writefile(path, FileData)
                print(path)

        else:
            path = os.path.join(mainRootPath, key)
            Writefile(path, FileData)
            print(path)



