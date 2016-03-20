from struct import *
from misc import ReadStringUntilNull
import os


class nintendoSarc(object):
    def extract(sarc_file, dictionary_name, endian):
        # First Start off by opening the file
        importSARCFile = open(sarc_file, mode='br', buffering=0)

        # Now the program is going to analyse the SARC section
        SARCHeader = unpack(endian + '4s', importSARCFile.read(4))[0]
        SARCHeaderLength = unpack(endian + 'h', importSARCFile.read(2))[0]
        SARCByteOrderMarker = importSARCFile.read(2)
        SARCFileLength = unpack(endian + 'i', importSARCFile.read(4))[0]
        SARCAbsoluteDataOffset = unpack(endian + 'i', importSARCFile.read(4))[0]
        SARCUnknown = unpack(endian + 'i', importSARCFile.read(4))[0]
        SARCDict = {"Header": SARCHeader,
                    "Length": SARCHeaderLength,
                    "ByteOrder": SARCByteOrderMarker,
                    "FileSize": SARCFileLength,
                    "AbsoluteDataOffset": SARCAbsoluteDataOffset,
                    "Unknown": SARCUnknown}
#        print(SARCDict)

        # Then it is going to check the SFAT
        SFATHeader = unpack(endian + '4s', importSARCFile.read(4))[0]
        SFATHeaderLength = unpack(endian + 'h', importSARCFile.read(2))[0]
        SFATNodeCount = unpack(endian + 'h', importSARCFile.read(2))[0]
        SFATFilenameHashMultiplier = unpack(endian + 'i', importSARCFile.read(4))[0]
        SFATHeaderDict = {"Header": SFATHeader,
                          "Length": SFATHeaderLength,
                          "NodeCount": SFATNodeCount,
                          "FilenameHashMultipler": SFATFilenameHashMultiplier}
        SFATNodeDict = {}
        for i in range(0, SFATHeaderDict["NodeCount"]):
            SFATNameHash = hex(unpack(endian + 'I', importSARCFile.read(4))[0])
            SFAT_SFNT_FilenameOffset = unpack(endian + 'i', importSARCFile.read(4))[0]
            SFATFileDataStart = unpack(endian + 'i', importSARCFile.read(4))[0]
            SFATFileDataEnd = unpack(endian + 'i', importSARCFile.read(4))[0]
            SFATNodeDict[SFATNameHash] = {"FilenameOffset": SFAT_SFNT_FilenameOffset,
                                          "FileDataStart": SFATFileDataStart,
                                          "FileDataEnd": SFATFileDataEnd}
#        print(SFATHeaderDict)
#        print(SFATNodeDict)

        # And then finally the SFNT Section
        SFNTHeader = unpack(endian + '4s', importSARCFile.read(4))[0]
        SFNTHeaderLength = unpack(endian + 'h', importSARCFile.read(2))[0]
        SFNTUnknown = unpack(endian + 'h', importSARCFile.read(2))[0]
        SFNTDataStart = importSARCFile.tell()
        SFNTDict = {"Header": SFNTHeader,
                    "Length": SFNTHeaderLength,
                    "Unknown": SFNTUnknown,
                    "StringLocation": SFNTDataStart}
#        print(SFNTDict)

        for FileHash in SFATNodeDict.keys():
            # First lets extract the actual files from
            # the SARC and also gets it's size.
            importSARCFile.seek(SARCDict["AbsoluteDataOffset"] +
                                SFATNodeDict[FileHash]["FileDataStart"])
            DataSize = SFATNodeDict[FileHash]["FileDataEnd"] - \
                       SFATNodeDict[FileHash]["FileDataStart"]
            ExtractedData = importSARCFile.read(DataSize)

            hasRealString = 0
            if SFATNodeDict[FileHash]["FilenameOffset"] is not 0:
                # To explain, there is a 01 that is irrelevant to finding the real string
                # Within the SARC file. I am just getting rid of that 01. (The 01 is there
                # to say, hey I have the real string inside me, the SARC file!)
                # Also the strings in the SFNT Data are aligned by 4. That is where the
                # times 4 comes from.
                hasRealString = 1
                bufferSFNTFilenameOffset = pack('<i', SFATNodeDict[FileHash]["FilenameOffset"])
                SFNTDataString = unpack('<i', bufferSFNTFilenameOffset[:3] + b'\x00')[0]
                importSARCFile.seek(SFNTDict["StringLocation"] + (SFNTDataString * 4))
                RealString = ReadStringUntilNull.__init__(importSARCFile)
                filePath = os.path.split(RealString)
            else:
                pass

            if hasRealString:
                if filePath[0] is not '':
                    dictionary_name[FileHash] = {'Data': ExtractedData, 'Size': DataSize,
                                                 'String': {'Dir': filePath[0], 'File': filePath[1]}}
                else:
                    dictionary_name[FileHash] = {'Data': ExtractedData, 'Size': DataSize,
                                                 'String': {'File': filePath[1]}}
            else:
                dictionary_name[FileHash] = {'Data': ExtractedData, 'Size': DataSize}
