#!/usr/bin/env python

"""
Compress and decompress data using the aPACK library (http://ibsensoftware.com/products_aPLib.html).
"""

from ctypes import *
aplib = cdll.aplib

def compress(data):
	size = len(data)
	max_packed_size = max_compressed_size(size)
	destination = create_string_buffer(max_packed_size)
	workmem_size = aplib.aP_workmem_size(size)
	workmem = create_string_buffer(workmem_size)
	packed_size = aplib.aP_pack(c_char_p(data), byref(destination), size, byref(workmem), None, None)
	if packed_size == -1:
		raise Exception('error while compressing data')
	return destination[:packed_size]
	
def decompress(data, size):
	destination = create_string_buffer(size)
	unpacked_size = aplib.aP_depack_asm(c_char_p(data), byref(destination))
	if unpacked_size == -1:
		raise Exception('error while decompressing data')
	assert size == unpacked_size
	return destination[:unpacked_size]

def max_compressed_size(size):
	assert size > 0
	r = aplib.aP_max_packed_size(size)
	if r < 0:
		return 0x100000000L + r
	if r < size:
		raise Exception('size is too large')
	return r

		
if __name__ == '__main__':
	from sys import stdin, stdout, stderr, argv, exit

	if len(argv) == 1:
		fin = stdin
		fout = stdout
	elif len(argv) == 2:
		fin = open(argv[1], 'rb')
		fout = stdout
	elif len(argv) == 3:
		fin = open(argv[1], 'rb')
		fout = open(argv[2], 'wb')
	else:
		stderr.write('Usage: %s [<uncompressed input file> [<compressed output file>]]\n' % argv[0])
		exit(1)
		
	fout.write(compress(fin.read()))
