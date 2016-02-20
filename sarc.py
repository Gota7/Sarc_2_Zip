from struct import *

class nintendoSarc(object):
	def extract(sarc_file, dictionary_name):
		#First Start off by opening the file
		importSARCFile = open(sarc_file, mode='br', buffering=0)

		#Now the program is going to analyse the SARC section
		SARCHeader = unpack('<4s', importSARCFile.read(4))[0]
		SARCHeaderLength = unpack('<h', importSARCFile.read(2))[0]
		SARCByteOrderMarker = importSARCFile.read(2)
		SARCFileLength = unpack('<i', importSARCFile.read(4))[0]
		SARCAbsoluteDataOffset = unpack('<i', importSARCFile.read(4))[0]
		SARCUnknown = unpack('<i', importSARCFile.read(4))[0]

		#Then it is going to check the SFAT
		SFATHeader = unpack('<4s', importSARCFile.read(4))[0]
		SFATHeaderLength = unpack('<h', importSARCFile.read(2))[0]
		SFATNodeCount = unpack('<h', importSARCFile.read(2))[0]
		SFATFilenameHashMultiplier = unpack('<i', importSARCFile.read(4))[0]

		for i in range(0, SFATNodeCount):
			SFATNameHash = hex(unpack('<I', importSARCFile.read(4))[0])
			SFAT_SFNT_FilenameOffset = unpack('<i', importSARCFile.read(4))[0]
			SFATFileDataStart = unpack('<i', importSARCFile.read(4))[0]
			SFATFileDataEnd = unpack('<i', importSARCFile.read(4))[0]
			SFATSeekOffset = importSARCFile.tell()

			dataStartingPoint = SARCAbsoluteDataOffset + SFATFileDataStart
			DataSize = SFATFileDataEnd - SFATFileDataStart
			importSARCFile.seek(dataStartingPoint)
			extractedData = importSARCFile.read(DataSize)
			importSARCFile.seek(SFATSeekOffset)

			dictionary_name[SFATNameHash] = {'Data': extractedData, 'Size': DataSize}
