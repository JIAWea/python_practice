import struct


headPack = struct.pack("!3I", *(123111,123,123))
print("len: ", headPack.__len__())
print(headPack)

headunPack = struct.unpack('!3I', headPack)
print(headunPack)