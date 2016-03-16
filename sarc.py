from struct import *
from misc import ReadStringUntilNull
import os


class nintendoSarc(object):
    def extract(sarc_file, dictionary_name):
        # First Start off by opening the file
        importSARCFile = open(sarc_file, mode='br', buffering=0)

        # Now the program is going to analyse the SARC section
        SARCHeader = unpack('<4s', importSARCFile.read(4))[0]
        SARCHeaderLength = unpack('<h', importSARCFile.read(2))[0]
        SARCByteOrderMarker = importSARCFile.read(2)
        SARCFileLength = unpack('<i', importSARCFile.read(4))[0]
        SARCAbsoluteDataOffset = unpack('<i', importSARCFile.read(4))[0]
        SARCUnknown = unpack('<i', importSARCFile.read(4))[0]

        # Then it is going to check the SFAT
        SFATHeaderSeek = importSARCFile.tell()
        SFATHeader = unpack('<4s', importSARCFile.read(4))[0]
        SFATHeaderLength = unpack('<h', importSARCFile.read(2))[0]
        SFATNodeCount = unpack('<h', importSARCFile.read(2))[0]
        SFATFilenameHashMultiplier = unpack('<i', importSARCFile.read(4))[0]

        for i in range(0, SFATNodeCount):
            hasRealFile = False

            SFATNameHash = hex(unpack('<I', importSARCFile.read(4))[0])
            SFAT_SFNT_FilenameOffset = unpack('<i', importSARCFile.read(4))[0]
            if SFAT_SFNT_FilenameOffset is not 0:
                hasRealFile = True

                SFATCurrentSeek = importSARCFile.tell()
                bufferSFNTFilenameOffset = pack('i', SFAT_SFNT_FilenameOffset)
                SFNTDataString = unpack('i', bufferSFNTFilenameOffset[:3] + b'\x00')[0]
                # If you are wondering where the 16 came, Think
                # about how each node takes sixteen bytes
                # Also the 8 came from the SFNT Header size
                beginningString = SFATHeaderSeek + SFATHeaderLength + \
                                  (SFATNodeCount * 16) + 8 + (SFNTDataString * 4)

                importSARCFile.seek(beginningString)
                extractedString = ReadStringUntilNull.__init__(importSARCFile)
                filePath = os.path.split(extractedString)
                importSARCFile.seek(SFATCurrentSeek)

            SFATFileDataStart = unpack('<i', importSARCFile.read(4))[0]
            SFATFileDataEnd = unpack('<i', importSARCFile.read(4))[0]
            SFATSeekOffset = importSARCFile.tell()

            dataStartingPoint = SARCAbsoluteDataOffset + SFATFileDataStart
            DataSize = SFATFileDataEnd - SFATFileDataStart
            importSARCFile.seek(dataStartingPoint)
            extractedData = importSARCFile.read(DataSize)
            importSARCFile.seek(SFATSeekOffset)

            if hasRealFile:
                if filePath[0] is not '':
                    dictionary_name[SFATNameHash] = {'Data': extractedData, 'Size': DataSize,
                                                     'String': {'Dir': filePath[0], 'File': filePath[1]}}
                else:
                    dictionary_name[SFATNameHash] = {'Data': extractedData, 'Size': DataSize,
                                                     'String': {'File': filePath[1]}}
            else:
                dictionary_name[SFATNameHash] = {'Data': extractedData, 'Size': DataSize}
