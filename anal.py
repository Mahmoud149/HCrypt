#!/usr/bin/env python
#requires having 'numpy' library installed  
# 3x3: 1 34 54 8 69 2 5 5 1 

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


    def det_inv(self,mat):
        detM = round(np.linalg.det(mat))
        detM = detM % hill_tools.CHAR_LENGTH
        return self.mod_inv(int(detM))
    
    
    def mod_inv(self,n):
        for i in range(0,hill_tools.CHAR_LENGTH):
            if ((n*i)%hill_tools.CHAR_LENGTH == 1):
                return i
        return None


    def do(self):
        plainLen = len(self.ht.byteS)
        zed = []
        offset = 0
        plainBytes = np.zeros((self.keylen,self.keylen),np.int8)
        ciphBytes = np.zeros((self.keylen,self.keylen),np.int8)

        while True:
            track = offset
            for i in range(0,self.keylen):
                for j in range(0,self.keylen):
                    plainBytes[i][j] = self.ht.text[track]
                    ciphBytes[i][j] = self.ht.ciph[track]
                    track += 1
            inv = self.det_inv(np.matrix(plainBytes))
            
            
            if (offset+1+(self.keylen*self.keylen) > plainLen) or (len(zed) == MKEY_LEN) or (offset > 15*self.keylen):
                return zed
            elif (inv != None):
                invPt = (inv * self.ht.adjugate(np.matrix(plainBytes)))%hill_tools.CHAR_LENGTH
                x = (np.array(invPt * np.matrix(ciphBytes)))#%hill_tools.CHAR_LENGTH
                for i in range(0,len(x)):
                    for j in range(0,len(x)):
                        x[i][j] %= hill_tools.CHAR_LENGTH
                z = []
                for i in range(0,len(x)):
                    for j in range(0,len(x)):
                        z.append(x[j][i])
                tr = 0
                for i in range(0,len(x)):
                    for j in range(0,len(x)):
                        x[i][j] = z[tr]
                        tr += 1
                if self.det_inv(np.matrix(x)) != None:
                    zed.append(np.matrix(x))
                offset += 1
            else:
                offset += 1
        
'''
anal = Anal("OUT.txt","FOT.txt",5)
q = anal.do()
for j in q:
    print j
'''
