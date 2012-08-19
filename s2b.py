#!/usr/bin/env python

"""
Convert a S68 file created by Easy68K (http://www.easy68k.com/) to a binary file.
"""

from binascii import unhexlify

def s2b(fin, fout):
	expectedAddr = None
	startAddr = None
	bytesWritten = 0
	for l in fin:
		l = l.strip()
		assert l[0] == 'S'
		type = int(l[1], 16)
		length = int(l[2:4], 16)
		assert length == (len(l)-4)/2
		
		addr = None
		if type == 1:
			addr = int(l[4:8], 16)
			data = l[8:-2]
			length -= 3
		elif type == 2:
			addr = int(l[4:10], 16)
			data = l[10:-2]
			length -= 4
		elif type == 3:
			addr = int(l[4:12], 16)
			data = l[12:-2]
			length -= 5

		if addr is not None:
			if startAddr is None:
				startAddr = expectedAddr = addr
			assert expectedAddr <= addr
			if expectedAddr < addr:
				delta = addr - expectedAddr
				fout.write('\0' * delta)
				bytesWritten += delta
				expectedAddr = addr
			data = unhexlify(data)
			assert length == len(data)
			fout.write(data)
			bytesWritten += length
			expectedAddr += length

	assert expectedAddr == startAddr + bytesWritten
	return startAddr, bytesWritten
	

if __name__ == '__main__':
	from sys import stdin, stdout, stderr, argv, exit

	if len(argv) == 1:
		fin = stdin
		fout = stdout
		console = stderr
	elif len(argv) == 2:
		fin = stdin
		fout = open(argv[1], 'wb')
		console = stdout
	elif len(argv) == 3:
		fin = open(argv[1], 'r')
		fout = open(argv[2], 'wb')
		console = stdout
	else:
		stderr.write('Usage: %s [[<S68 input file>] <BIN output file>]\n' % argv[0])
		exit(1)

	console.write('addr: $%06x\nsize: %d\n' % s2b(fin, fout))
