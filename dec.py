#!/usr/bin/env python
# Small python script to decode a hill enciphered text file with a known key

# Requires numpy and hill_tools
# Evan Ricketts, April 2013

import argparse, numpy, cPickle, math, sys, hill_tools


p = argparse.ArgumentParser(description="Hill quick decoder")
p.add_argument('in_txt',metavar='--in-text')
p.add_argument('in_key',metavar='--in-key')
a = p.parse_args()

f = open(a.in_key,'r')
pre = cPickle.load(f)
f.close()
l = len(pre)
print 'decoding with inverse of\n',str(pre),'as key...'
f = open(a.in_txt,'r')
fil = f.read()
f.close()

ht = hill_tools.Hill(fil,l)

f = open('DECRYPT_KEY','w')
f.write(str(pre))
f.close()

f = open('DECRYPT_TEXT','w')
f.write(ht.decode(numpy.matrix(pre)))
f.close()

print
print 'wrote decrypted text and key file out'
