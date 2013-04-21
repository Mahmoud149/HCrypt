#!/usr/bin/python
#requires having 'numpy' library installed  

import argparse, numpy, cPickle, math
import hill_tools as ht




p = argparse.ArgumentParser(description="Hill quick decoder")
p.add_argument('in_txt',metavar='--in-text')
p.add_argument('in_key',metavar='--in-key')
a = p.parse_args()

## LOAD KEY AND WRITE IT TO FILE ##
f = open(a.in_key,'r')
pre = cPickle.load(f)
f.close()
#print pre
l = int(round(math.sqrt(len(pre))))
#print l
mat = numpy.zeros((l,l),numpy.int8)
t = 0
for i in range(0,len(mat)):
    for j in range(0,len(mat)):
        mat[i][j] = pre[t]
        t += 1
f = open('DECRYPT_K','w')
x = str(mat)
f.write(x)
f.write("\n")
f.write("INVERSE\n")
f.write(str(ht.invert(numpy.matrix(mat))))
f.close()

## LOAD TEXT, DECRYPT, WRITE TO FILE ##
f = open(a.in_txt,'r')
text = f.read()
f.close()
decText = ht.decode(text,mat)
f = open('DECRYPT_T','w')
f.write(decText)
f.close()

