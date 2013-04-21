#!/usr/bin/env python

import numpy, hill_tools, argparse, cPickle, anal

KEY_LEN = 4

class Total(object):

    def __init__(self,pTp,cTp):
        self.ana = anal.Anal(pTp,cTp,2)

    def looper(self):
        plaint = self.ana.plaintext
        for i in range(2,100):
            print "currently @",i,"by key size"
            self.ana.update_keyLen(i)
            keys = self.ana.do()
            self.ana.ht.switch_byteS()
            for j in range(0,min(len(keys),KEY_LEN)):
                decoded = self.ana.ht.decode_sect(keys[j])
                #print decoded
                bu = True
                for x in range(0,len(decoded)):
                    if decoded[x] != plaint[x]:
                        bu = False
                if bu:
                    return keys[j]
            self.ana.ht.switch_byteS()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Cryptanalyze hill cipher')
    p.add_argument('plaintext', metavar='pt')
    p.add_argument('ciphertext',metavar='ct')
    arg = p.parse_args()

    t = Total(arg.plaintext,arg.ciphertext).looper()
    
    if t != None:
        ess = []
        q = numpy.array(t)
    
        for j in range(0,len(q)):
            for h in range(0,len(q)):
                ess.append(q[j][h])

        f = open("KEY",'w')
        cPickle.dump(ess,f)
        f.close()
        
        print "wrote key file out"
        print
        print q
    else:
        print "no key found; try manual"

