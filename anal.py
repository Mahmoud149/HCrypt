#!/usr/bin/env python
#requires having 'numpy' library installed  

# A python script for running cryptanalysis on a known plaintext/ciphertext
# hill cipher pairing; requires a suspected length be specified
# by Evan Ricketts, April 2013

# Note: apparently numpy has issues with doing determinants reliably
# on larger matrices, hence the usage of more CPU costly Laplace expansion here 

import numpy as np
import hill_tools 
import sys, math, argparse, cPickle


MKEY_LEN = 4

class Anal(object):

    def __init__(self,pTp,cTp,keyL):
        self.plaintext = open(pTp,'r').read()
        self.ciphertext = open(cTp,'r').read()
        self.keylen = keyL
        self.ht = hill_tools.Hill(self.plaintext,self.keylen)
        self.ht.store_ciph(self.ciphertext)

    def update_keyLen(self,newKeyLen):
        self.ht.update_keyLen(newKeyLen)
        self.keylen = newKeyLen


    def do(self):
        plainLen = len(self.ht.text)
        zed = []
        offset = 0
        plainBytes = np.zeros((self.keylen,self.keylen))
        ciphBytes = np.zeros((self.keylen,self.keylen))
        while True:
            track = offset
            for i in range(0,self.keylen):
                for j in range(0,self.keylen):
                    plainBytes[i][j] = self.ht.text[track]
                    ciphBytes[i][j] = self.ht.ciph[track]
                    track += 1
            inv = self.ht.mod_inverse(self.ht.laplace(plainBytes))
            
            if (inv != None):
                invPt = (inv * np.matrix(self.ht.adjugate(plainBytes)))%hill_tools.CHAR_LENGTH
                
                x = (np.array(invPt * np.matrix(ciphBytes)))%hill_tools.CHAR_LENGTH
                x = np.swapaxes(x,0,1)
                key_det = self.ht.mod_inverse(self.ht.laplace(x))

                if key_det != None:
                    zed.append((x,key_det))
            offset += 1
            if (offset+(self.keylen*self.keylen) > plainLen) or len(zed) > MKEY_LEN: 
                return zed


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument("plain")
    a.add_argument("ciph")
    a.add_argument("ks",type=int)
    p = a.parse_args()

    anal = Anal(p.plain,p.ciph,p.ks)
    q = anal.do()
    print "Found",str(len(q)),"possible keys; writing out now."
    
    for i in range(0,len(q)):
        f = open(("out/"+str(i)),'w')
        cPickle.dump(q[i],f)
        f.close()
