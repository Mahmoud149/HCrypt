#!/usr/bin/env python
#requires having 'numpy' library installed  
#Written by Evan Ricketts, April 2013

import numpy as np
import sys, math, cPickle, argparse, math

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


    def laplace(self,array):
        if len(array) < 7:
            return int(round(np.linalg.det(array)))
        else:
            z = 0
            for i in range(0,len(array)):
                a = int(round(math.pow(-1,((1)+(i+1)))))
                b = array[0][i]
                c = self.laplace(self.delete_at(array,i,0)) 
                z += (((a*b*c)) % 256)
            return z  % 256
                

    def mod_inverse(self,m):  # returns (inverse of m) % CHAR_LENGTH
        for i in range(0,CHAR_LENGTH):
            if ((m*i)%CHAR_LENGTH == 1):
                return i
        # else no inverse exists:
        return None


    def delete_at(self,em,i,j): # return em with row i, column j removed
        m = np.array(em)
        ret = np.zeros((len(m)-1,len(m)-1))
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
        ret = np.zeros((len(m),len(m)))#,np.int8)
        for i in range(0,len(m)):
            for j in range(0,len(m)):
                ret[j][i] = ((((-1)**(i+j))) * self.laplace(self.delete_at(m,j,i))) % 256
        return ret

    
    def invert(self,matrix,det=None):
        if det == None:
            x = self.mod_inverse(self.laplace(matrix))
        else:
            x = det
        y = self.adjugate(matrix)
        return x * y
    
    def to_bytes(self,string):
        return [ord(char) for char in string]

    def to_chars(self,byts): # reverse of to_bytes, but returns char array, not string
        return [chr(int(round(byte))) for byte in byts]

    
    def prepare_message(self,m,kL): # splits byte[] m into kL equal parts
        ret = [m[i:i+kL] for i in xrange(0,len(m),kL)]
        lastIdx = len(ret) - 1
        while len(ret[lastIdx]) < kL:
            ret[lastIdx].append(0)
        return ret


    def mult_message(self,m,k):
        newM = []
        for i in range(0,len(m)):
            x = np.zeros((len(m[i]),1))
            for j in range(0,len(m[i])):
                x[j][0] = m[i][j]
            x = np.matrix(x)
            z = np.array(k * x).reshape(-1).tolist()
            for j in z:
                newM.append(j%CHAR_LENGTH)
        return newM

            
    def encode(self,k): # Hill encodes string s with a key k[n][n]
        key = np.matrix(k)
        return ''.join(self.to_chars(self.mult_message(self.byteS,key)))


    def decode(self,k,opt=None,det=None): # Hill decodes string s with a key k[n][n]
        if opt == None:
            fopt = self.byteS
        else:
            fopt = opt
        key = np.matrix(self.invert(np.array(k),det))
        return ''.join(self.to_chars(self.mult_message(fopt,key)))

    
    def decode_sect(self,k,det):
        qq = []
        qq.append(self.byteS[0])
        qq.append(self.byteS[1])
        return self.decode(k,qq,det)
