#!/usr/bin/python
#requires having 'numpy' library installed  
#Written by Evan Ricketts, April 2013

import numpy as np
import sys, math

CHAR_LENGTH = 256 # the number of chars available to the current alphabet


def make_identity(length,n=1): # make an identity matrix of size length x length
    x = np.zeros((length,length),np.int8)
    for i in range(0,length):
        x[i][i] = n
    return x

def make_id_s(length):
    x = make_identity(length)
    y = []
    for r in x:
        for c in r:
            y.append(c)
    return ''.join(to_chars(y))

def determinant_inverse(m): # returns inverse of numpy.matrix M's determinant
    detM = round(np.linalg.det(m))
    detM = detM % CHAR_LENGTH
    return __mod_inverse__(int(detM))
    

def __mod_inverse__(m):  # returns (inverse of m) % CHAR_LENGTH
    for i in range(0,CHAR_LENGTH):
        if ((m*i)%CHAR_LENGTH == 1):
            return i
    # else no inverse exists:
    print "There exists no inverse of your key. Sorry!"
    sys.exit(0)


def __delete_at(em,i,j): # return em with row i, column j removed
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


def adjugate(m): # make the modulo adjugate matrix of m
    ret = np.zeros((len(m),len(m)),np.int8)
    for i in range(0,len(m)):
        for j in range(0,len(m)):
            ret[j][i] = (((-1)**(i + j)) * (round(np.linalg.det(__delete_at(m,j,i))) % CHAR_LENGTH))%CHAR_LENGTH
    return ret


def invert(matrix):
    adj = adjugate(matrix)
    det = determinant_inverse(matrix)
    return det * adj


def to_bytes(string): # puts string in array of bytes representing chars of str
    return [ord(char) for char in string]


def to_chars(byts): # reverse of to_bytes, but returns char array, not string
    return [chr(int(round(byte))) for byte in byts]


def prepare_message(m,kL): # splits byte[] m into kL equal parts
    newM = []
    for i in range(0,(len(m)/kL)):
        splart = []
        for j in range(i*kL,((i*kL)+kL)):
            splart.append(m[j])
        newM.append(splart)
    return newM


def mult_message(m,k):
    newM = []
    for i in range(0,len(m)):
        x = np.matrix(m[i])
        x.resize((len(k),1))
        z = np.array(k * x).reshape(-1).tolist()
        for j in z:
            newM.append(j%CHAR_LENGTH)
    return newM

            

def encode(s,k): # Hill encodes string s with a key k[n][n]
    byteS = to_bytes(s)
    key = np.matrix(k)
    while (len(byteS) % len(k) != 0):
        byteS.append(byteS[len(byteS)-1])
    byteS = prepare_message(byteS,len(k))
    byteE = mult_message(byteS,key)
    return ''.join(to_chars(byteE))


def decode(s,k): # Hill decodes string s with a key k[n][n]
    byteS = to_bytes(s)
    key = invert(np.matrix(k))
    byteS = prepare_message(byteS,len(k))
    byteE = mult_message(byteS,key)
    return ''.join(to_chars(byteE))
