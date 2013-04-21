#!/usr/bin/env python

import argparse, numpy, cPickle, math
import hill_tools


p = argparse.ArgumentParser(description="Hill quick decoder")
p.add_argument('in_txt',metavar='--in-text')
p.add_argument('in_key',metavar='--in-key')
a = p.parse_args()

f = open(a.in_key,'r')
pre = cPickle.load(f)
f.close()
l = int(round(math.sqrt(len(pre))))
ht = hill_tools.Hill(open(a.in_txt,'r').read(),l)
mat = numpy.zeros((l,l),numpy.int8)
t = 0
for i in range(0,l):
    for j in range(0,l):
        mat[i][j] = pre[t]
        t += 1
f = open('DECRYPT_KEY','w')
f.write(str(mat))
f.write("\n")
f.write("INVERSE\n")
f.write(str(ht.invert(numpy.matrix(mat))))
f.close()

f = open('DECRYPT_T','w')
f.write(ht.decode(mat))
f.close()
