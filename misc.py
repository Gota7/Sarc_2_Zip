from struct import *


# My idea behind this code is to keep unpacking the
# Buffer until the Buffer hit a Null (or None in python)
# value. Then the program would stop doing this. But, becuase
# of how the code works, it also factors in a Null, however the if
# statement catches this. Just keep this in mind when using .tell()
class ReadStringUntilNull(object):
    def __init__(stringFromFile):
        stringTempOutput = b''
        stringBuffer = unpack('<1s', stringFromFile.read(1))[0]
        stringTempOutput += stringBuffer
        while stringBuffer != b'\x00':
            stringBuffer = unpack('<1s', stringFromFile.read(1))[0]
            if stringBuffer != b'\x00':
                stringTempOutput += stringBuffer
            else:
                pass
            stringOutput = stringTempOutput.decode("utf-8")
        return stringOutput

class Writefile:
    def __init__(self, newName, newData):
        NewFile = open(newName, mode='bw', buffering=0)
        NewFile.write(newData)
        NewFile.close()
