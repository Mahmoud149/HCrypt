#!/usr/bin/env python


import argparse, numpy, cPickle, math, sys, hill_tools

p = argparse.ArgumentParser()
p.add_argument("in_text")
p.add_argument("in_key")
p.add_argument("out_text")
p.add_argument("out_key")
a = p.parse_args()


keyFlat = [int(c) for c in open(a.in_key,'r').read().split()]
ht = hill_tools.Hill(open(a.in_text,'r').read(),int(round(math.sqrt(len(keyFlat)))))

key = numpy.zeros((ht.kL,ht.kL))
for i in range(0,ht.kL):
    x = i*ht.kL
    key[i] = keyFlat[x:x+ht.kL]

print "Checking that your key can be used to decode..."
det = ht.mod_inverse(ht.laplace(key))
if det == None:
    zeb = "a"
    while zeb[0].lower() != 'y':
        zeb = raw_input("Your key is unable to decode. Continue? [Y/N]: ")
        if zeb[0].lower() == 'n':
            print "Try again with another key."
            sys.exit(0)


out = open(a.out_text,'w')
out.write(ht.encode(key))
out.close()

out = open(a.out_key,'w')
cPickle.dump((key,det),out)

print "Wrote file out to",a.out_text
print "wrote dec.py compatible key out to",a.out_key
