#!/usr/bin/python
#requires having 'numpy' library installed  
# 3x3: 1 34 54 8 69 2 5 5 1 

import numpy as np
import hill_tools as ht
import sys, math, argparse, cPickle
#from sets import Set


KEY_LEN = 4



def determinant_inverse(m): # returns inverse of numpy.matrix M's determinant
    detM = round(np.linalg.det(m))
    detM = detM % ht.CHAR_LENGTH
    return __mod_inverse__(int(detM))

def __mod_inverse__(m):  # returns (inverse of m) % CHAR_LENGTH
    for i in range(0,ht.CHAR_LENGTH):
        if ((m*i)%ht.CHAR_LENGTH == 1):
            return i
    else:
        return None


def analyze(m,plain,ciph):
    #sys.exit(0)
    zed = []
    offset = 0
    pB = np.zeros((m,m),np.int8)
    cB = np.zeros((m,m),np.int8)
    while True:
        track = offset
        for i in range(0,m):
            for j in range(0,m):
                pB[i][j] = plain[track]
                cB[i][j] = ciph[track]
                track += 1

        inv = determinant_inverse(np.matrix(pB))
        if (offset+1+(m*m)) > len(plain)-1 or (len(zed) == KEY_LEN) or (offset > 15*m):
            return zed
        elif (inv != None):
            invPt = (inv * ht.adjugate(np.matrix(pB)))%ht.CHAR_LENGTH
            x = np.array(invPt * np.matrix(cB))#%ht.CHAR_LENGTH
            for i in range(0,len(x)):
                for j in range(0,len(x)):
                    x[i][j] %= ht.CHAR_LENGTH
            z = []
            for i in range(0,len(x)):
                for j in range(0,len(x)):
                    z.append(x[j][i])
            tr = 0
            for i in range(0,len(x)):
                for j in range(0,len(x)):
                    x[i][j] = z[tr]
                    tr += 1
            if determinant_inverse(np.matrix(x)) != None:
                zed.append(np.matrix(x))
            offset += 1
        else:
            offset += 1
                    

def anal(upto, plain, ciph):
    return analyze(upto,plain,ciph)


def anal_mult(upto, plain, ciph):
    x = []
    for i in range(2,(upto+1)):
        x.append(analyze(i,plain,ciph))
    return x


def open_file(s):
    return open(s,'r').read()

def do_process(pTd,cTd,upto,suspect):
    try:
        plan = open_file(pTd)
    except IOError:
        print "Plaintext not found"
        sys.exit(0)
    try:
        cih = open_file(cTd)
    except:
        print "Ciphertext not found"
        sys.exit(0)

    plain = ht.to_bytes(plan)
    ciph = ht.to_bytes(cih)

    if upto == None:
        return (plan,cih,anal(suspect, plain, ciph))
    else:
        return (plan,cih,anal_mult(upto, plain, ciph))


def decode(s,k):
    global BYTEM
    if BYTEM == None:
        BYTEM = ht.prepare_message(ht.to_bytes(s),len(k))
    km = ht.invert(np.matrix(k))
    return ''.join(ht.to_chars(ht.mult_message(BYTEM,km)))


BYTEM = None
##### CLI STUFF ########
if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Cryptanalyze hill cipher')
    p.add_argument('plaintext', metavar='pt')
    p.add_argument('ciphertext',metavar='ct')
    p.add_argument('s',metavar='--suspected',type=int)
    p.add_argument('-m',metavar='--more',type=int)
    arg = p.parse_args()


#if (arg.u == None and arg.s == None):
#    print "Please enter key matrix info"
#    sys.exit(0)


    x,y,z = do_process(arg.plaintext,arg.ciphertext,None,arg.s)

    if (len(x) < 15):
        print "Warning: short plaintext/ciphertext lengths"

    if (arg.m > KEY_LEN):
        zek = arg.m
    else:
        zek = KEY_LEN

    base = "out/decrypt"
    base += str(arg.s)
    base += "x"

    if zek > len(z):
        zek = len(z)

    for i in range(0,zek):
        dec = decode(y,z[i])
        f = open((base+(str(i))),'w')
        f.write(dec)
        f.close()
        ess = []
        q = np.array(z[i])

        for j in range(0,len(q)):
            for h in range(0,len(q)):
                ess.append(q[j][h])
    
        f = open((base+(str(i)))+"key",'w')
        cPickle.dump(ess,f)
        f.close()
        print "wrote",zek,"files to out dir"
