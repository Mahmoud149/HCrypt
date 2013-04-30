#!/usr/bin/env python

import numpy, hill_tools, argparse, cPickle, anal, math

class Total(object):

    def __init__(self,pTp,cTp):
        self.ana = anal.Anal(pTp,cTp,2)


    def looper(self):
        plaint = self.ana.plaintext
        for i in range(2,int(round(math.sqrt(len(plaint))))+1):
            print "currently @",i,"by key size"
            self.ana.update_keyLen(i)
            keys = self.ana.do()
            self.ana.ht.switch_byteS()
            for j in range(0,len(keys)):
                decoded = self.ana.ht.decode_sect(keys[j])#partial decode;faster
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
    p.add_argument('to_decode')
    p.add_argument('-s',metavar='--start',type=int,help='start value for key size to test')
    arg = p.parse_args()

    t = Total(arg.plaintext,arg.ciphertext).looper()
    
    if t != None:
        print 'Found key:'
        print t
        print
        print 'Writing decrypted files out...'
        ess = []
        q = numpy.array(t)
    
        for j in range(0,len(q)):
            for h in range(0,len(q)):
                ess.append(q[j][h])

        f = open("DP_KEY",'w')
        cPickle.dump(ess,f)
        f.close()

        f = open("DECRYPT_KEY",'w')
        f.write(str(q))
        f.close()

        g = open(arg.cp2,'r').read()
        h2 = hill_tools.Hill(g,len(t))
        f = open("DECRYPT_TXT",'w')
        f.write(h2.decode(t))
        f.close()
    else:
        print "no key found; try manual"
