#!/usr/bin/env python

"""
Convert a binary file to an ASM file.
"""

def b2a(fin, fout):
	while True:
		b = fin.read(16)
		h = ['$%02x' % ord(c) for c in b]
		if h:
			fout.write('\tdc.b\t%s\n' % ','.join(h))
		if len(h) < 16:
			break
		

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
		fout = open(argv[2], 'w')
	else:
		stderr.write('Usage: %s [<BIN input file> [<ASM output file>]]\n' % argv[0])
		exit(1)

	b2a(fin, fout)
