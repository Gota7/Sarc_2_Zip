from struct import *
from misc import ReadStringUntilNull
import os


class thirdpartySAHT():
    def extract(saht_file, dictionary_name):
        importSAHTFile = open(saht_file, mode='br', buffering=0)

        SAHTHeader = unpack('<4s', importSAHTFile.read(4))[0]
        SAHTFileSize = unpack('<i', importSAHTFile.read(4))[0]
        SAHTDataOffset = unpack('<i', importSAHTFile.read(4))[0]
        SAHTNrEntries = unpack('<i', importSAHTFile.read(4))[0]

        for i in range(0, SAHTNrEntries):
            StartingPoint = importSAHTFile.tell()
            SAHTHash = hex(unpack('<I', importSAHTFile.read(4))[0])

            stringOutput = ReadStringUntilNull.__init__(importSAHTFile)
            filePath = os.path.split(stringOutput)

            HitNullPoint = importSAHTFile.tell()
            # Tells the pointer where to go
            StringLengthRemainder = (HitNullPoint - StartingPoint) % SAHTDataOffset
            if StringLengthRemainder == 0:
                pass
            else:
                NextHashPoint = SAHTDataOffset - StringLengthRemainder
                importSAHTFile.seek(HitNullPoint + NextHashPoint)

            if filePath[0] is not '':
                dictionary_name[SAHTHash] = {"Directory Name": filePath[0], "File Name": filePath[1]}
            else:
                dictionary_name[SAHTHash] = {"File Name": filePath[1]}
