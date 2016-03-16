from sarc import *
from saht import *
from misc import *
import os
import argparse
import glob

parser = argparse.ArgumentParser(description='This program can extract \'unsafe\' SARC files')
parser.add_argument("SARC", help="put the location of the SARC file. "
                                 "This is an official Nintendo container format"
                                 " used to store game files in.", type=str)
parser.add_argument("--SAHT", help="Put the location of the SAHT file. "
                                   "These files contain the real file names"
                                   " for the hashes", type=str)
parser.parse_args()
args = parser.parse_args()


for currentInput in glob.glob(args.SARC):
    memorySARCDatabase = {}
    nintendoSarc.extract(currentInput, memorySARCDatabase)
    print("")
    print(memorySARCDatabase.keys())
    mainEntryDir = os.path.split(currentInput)[1]
    DirPath = os.path.split(currentInput)[0]
    mainRootPath = os.path.join(DirPath, mainEntryDir+'.d')
    os.mkdir(mainRootPath)

    for key in memorySARCDatabase.keys():
        if 'String' in memorySARCDatabase[key]:
            FileNameValue = memorySARCDatabase[key]['String']['File']
            if "Dir" in memorySARCDatabase[key]['String']:
                DirNameValue = memorySARCDatabase[key]['String']["Dir"]
                try:
                    os.mkdir(os.path.join(mainRootPath, DirNameValue))
                except FileExistsError:
                    pass
                path = os.path.join(mainRootPath, DirNameValue, FileNameValue)
                print(path)
                Writefile(path, memorySARCDatabase[key]["Data"])
            else:
                path = os.path.join(mainRootPath, FileNameValue)
                print(path)
                Writefile(path, memorySARCDatabase[key]["Data"])

        elif args.SAHT:
            memorySAHTDatabase = {}
            thirdpartySAHT.extract(args.SAHT, memorySAHTDatabase)
            if key in memorySAHTDatabase.keys():
                FileNameValue = memorySAHTDatabase[key]["File Name"]
                if "Directory Name" in memorySAHTDatabase[key]:
                    DirNameValue = memorySAHTDatabase[key]["Directory Name"]
                    try:
                        os.mkdir(os.path.join(mainRootPath, DirNameValue))
                    except FileExistsError:
                        pass
                    path = os.path.join(mainRootPath, DirNameValue, FileNameValue)
                    print(path)
                    Writefile(path, memorySARCDatabase[key]["Data"])
                else:
                    path = os.path.join(mainRootPath, FileNameValue)
                    print(path)
                    Writefile(path, memorySARCDatabase[key]["Data"])
            else:
                Writefile(os.path.join(mainRootPath, key), memorySARCDatabase[key]["Data"])

        else:
            Writefile(os.path.join(mainRootPath, key), memorySARCDatabase[key]["Data"])



