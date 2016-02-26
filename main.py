from sarc import *
from saht import *
import os
import argparse
import glob

parser = argparse.ArgumentParser(description=
                                 'This program can extract \'unsafe\' SARC files')
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

    if args.SAHT:
        memorySAHTDatabase = {}
        thirdpartySAHT.extract(args.SAHT, memorySAHTDatabase)

        for key in memorySARCDatabase.keys():
            if key in memorySAHTDatabase.keys():
                FileNameValue = memorySAHTDatabase[key]["File Name"]
                if "Directory Name" in memorySAHTDatabase[key]:
                    DirNameValue = memorySAHTDatabase[key]["Directory Name"]
                    try:
                        os.mkdir(os.path.join(mainRootPath, DirNameValue))
                    except FileExistsError:
                        pass
                    print(os.path.join(mainRootPath, DirNameValue, FileNameValue))
                    path = os.path.join(mainRootPath, DirNameValue, FileNameValue)
                    NewFile = open(path, mode='bw', buffering=0)
                    NewFile.write(memorySARCDatabase[key]["Data"])
                    NewFile.close()
                else:
                    print(os.path.join(mainRootPath, FileNameValue))
                    path = os.path.join(mainRootPath, FileNameValue)
                    NewFile = open(path, mode='bw', buffering=0)
                    NewFile.write(memorySARCDatabase[key]["Data"])
                    NewFile.close()
            else:
                NewFile = open(os.path.join(mainRootPath, key), mode='bw', buffering=0)
                NewFile.write(memorySARCDatabase[key]["Data"])
                NewFile.close()
    else:
        for key in memorySARCDatabase:
            NewFile = open(os.path.join(mainRootPath, key), mode='bw', buffering=0)
            NewFile.write(memorySARCDatabase[key]["Data"])
            NewFile.close()
