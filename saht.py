from struct import *

class thirdpartySAHT(object):
	def extract (saht_file, dictionary_name):
		importSAHTFile = open(saht_file, mode='br', buffering=0)

		SAHTHeader = unpack('<4s', importSAHTFile.read(4))[0]
		SAHTFileSize = unpack('<i', importSAHTFile.read(4))[0]
		SAHTDataOffset = unpack('<i', importSAHTFile.read(4))[0]
		SAHTNrEntries = unpack('<i', importSAHTFile.read(4))[0]

		for i in range(0, SAHTNrEntries):
			StartingPoint = importSAHTFile.tell()
			SAHTHash = hex(unpack('<I', importSAHTFile.read(4))[0])

			SAHTString = b''
			hasDirectory = False
			Buffer = unpack('<1s', importSAHTFile.read(1))[0]
			SAHTString += Buffer
			while Buffer != b'\x00':
        		# My idea behind this code is to keep unpacking the
        		# Buffer until the Buffer hit a Null (or None in python)
       			# value. Then the program would stop doing this. But, becuase
        		# of how the code works, it also factors in a Null, however the if
        		# statement catches this. Just keep this in mind when using .tell()
				Buffer = unpack('<1s', importSAHTFile.read(1))[0]
				if Buffer != b'\x00' and Buffer != b'/':
					SAHTString += Buffer
				elif Buffer == b'/':
					hasDirectory = True
					DirectorySAHTString = SAHTString.decode("utf-8")
					Buffer = unpack('<1s', importSAHTFile.read(1))[0]
					SAHTString = b''
					if Buffer != b'\x00':
						SAHTString += Buffer
					else:
						pass
				else:
 					pass
            #The .decode is to convert it from a byte to string
			FileSAHTString = SAHTString.decode("utf-8")

			HitNullPoint = importSAHTFile.tell()
			if (HitNullPoint - StartingPoint) % SAHTDataOffset == 0:
				pass
			else:
				NextHashPoint = SAHTDataOffset - ((HitNullPoint - StartingPoint) % SAHTDataOffset)
				importSAHTFile.seek(HitNullPoint + NextHashPoint)

			if hasDirectory == True:
				dictionary_name[SAHTHash] = {"Directory Name": DirectorySAHTString, "File Name": FileSAHTString}
			else:
				dictionary_name[SAHTHash] = {"File Name": FileSAHTString}
