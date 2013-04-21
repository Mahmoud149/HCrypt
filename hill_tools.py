#!/usr/bin/env python
#requires having 'numpy' library installed  
#Written by Evan Ricketts, April 2013

import numpy as np
import sys, math

CHAR_LENGTH = 256 # the number of chars available to the current alphabet

class Hill(object):

    def __init__(self,infile,kL):
        self.text = self.to_bytes(infile)
        self.byteS = self.prepare_message(self.text,kL)
        self.kL = kL
        self.ciph = None

    
    def update_keyLen(self,newKeyL):
        self.byteS = self.prepare_message(self.text,newKeyL)
        if self.ciph != None:
            self.ciphS = self.prepare_message(self.ciph,newKeyL)
        self.kL = newKeyL
        

    def store_ciph(self,ciph):
        self.ciph = self.to_bytes(ciph)
        self.ciphS = self.prepare_message(self.ciph,self.kL)


    def switch_byteS(self):
        temp = self.byteS
        self.byteS = self.ciphS
        self.ciphS = temp

    def determinant_inverse(self,m): # returns inverse of numpy.matrix M's determinant
        detM = round(np.linalg.det(m))
        detM = detM % CHAR_LENGTH
        return self.__mod_inverse__(int(detM))
    

    def __mod_inverse__(self,m):  # returns (inverse of m) % CHAR_LENGTH
        for i in range(0,CHAR_LENGTH):
            if ((m*i)%CHAR_LENGTH == 1):
                return i
    # else no inverse exists:
        print "There exists no inverse of your key. Sorry!"
        sys.exit(0)


    def __delete_at(self,em,i,j): # return em with row i, column j removed
        m = np.array(em)
        ret = np.zeros((len(m)-1,len(m)-1),np.int8)
        p = 0
        for x in range(0,len(ret)):
            n = 0
            if j == p:
                p += 1
            for y in range(0,len(ret)):
                if i == n:
                    n += 1
                ret[x][y] = m[p][n]
                n += 1
            p += 1
        return ret


    def adjugate(self,m): # make the modulo adjugate matrix of m
        ret = np.zeros((len(m),len(m)),np.int8)
        for i in range(0,len(m)):
            for j in range(0,len(m)):
                ret[j][i] = (((-1)**(i + j)) * (round(np.linalg.det(self.__delete_at(m,j,i))) % CHAR_LENGTH))%CHAR_LENGTH
        return ret

    
    def invert(self,matrix):
        return self.determinant_inverse(matrix) * self.adjugate(matrix)


    def to_bytes(self,string): # puts string in array of bytes representing chars of str
        return [ord(char) for char in string]


    def to_chars(self,byts): # reverse of to_bytes, but returns char array, not string
        return [chr(int(round(byte))) for byte in byts]


    def prepare_message(self,m,kL): # splits byte[] m into kL equal parts
        newM = []
        while (len(m) % kL != 0):
            m.append(m[len(m)-1])
        for i in range(0,(len(m)/kL)):
            splart = []
            for j in range(i*kL,((i*kL)+kL)):
                splart.append(m[j])
            newM.append(splart)
        return newM


    def mult_message(self,m,k):
        newM = []
        for i in range(0,len(m)):
            x = np.matrix(m[i])
            x.resize((len(k),1))
            z = np.array(k * x).reshape(-1).tolist()
            for j in z:
                newM.append(j%CHAR_LENGTH)
        return newM

            

    def encode(self,k): # Hill encodes string s with a key k[n][n]
        key = np.matrix(k)
        return ''.join(self.to_chars(self.mult_message(self.byteS,key)))


    def decode(self,k): # Hill decodes string s with a key k[n][n]
        key = self.invert(np.matrix(k))
        return ''.join(self.to_chars(self.mult_message(self.byteS,key)))

    def decode_sect(self,k):
        key = self.invert(np.matrix(k))
        return ''.join(self.to_chars(self.mult_message(self.byteS[0],key)))

'''
ht = Hill(open("FOT.txt",'r').read(),5)
out = open("UT.txt",'w')
out.write(ht.decode(np.matrix([[9, 10, 0, 20, 7],
                               [4, 3, 14, 23, 16],
                               [7, 2, 5, 7, 5],
                               [21, 1, 25, 3, 1],
                               [1, 5, 4, 3, 0]])))
out.close()
'''
