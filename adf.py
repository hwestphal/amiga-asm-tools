#!/usr/bin/env python

"""
Create an Amiga disk image file (ADF, 880KB).
"""

import struct

def createAdf(data):
	adf = '\0' * (1760 * 512)
	for block in sorted(data.iterkeys()):
		bin = data[block]
		length = min(len(bin), (1760-block) * 512)
		adf = adf[:block*512] + bin[:length] + adf[block*512 + length:]
	assert len(adf) == 1760*512
	return addBootblockChecksum(adf)

	
def addBootblockChecksum(adf):
	if adf[:4] != 'DOS\0':
		return adf
		
	checksum = 0
	for i in range(1024/4):
		thislong = ord(adf[i*4]) << 24
		thislong += ord(adf[i*4+1]) << 16
		thislong += ord(adf[i*4+2]) << 8
		thislong += ord(adf[i*4+3])
		checksum += thislong
		if checksum > 0xFFFFFFFF:
			checksum -= 0x100000000
			checksum += 1
	checksum ^= 0xFFFFFFFF
	return adf[:4] + struct.pack('>L', checksum) + adf[8:]


if __name__ == '__main__':
	from sys import stderr, argv, exit

	if len(argv) < 2:
		stderr.write('Usage: %s <ADF output file> [<block number>=<data file>]*\n' % argv[0])
		exit(1)
	
	data = {}
	for arg in argv[2:]:
		parts = arg.split('=', 1)
		block = int(parts[0])
		with open(parts[1], 'rb') as fin:
			bin = fin.read()
		data[block] = bin
	with open(argv[1], 'wb') as fout:
		fout.write(createAdf(data))
