#!/usr/bin/python
#requires having 'numpy' library installed  

import numpy, hill_tools, argparse, cPickle, anal
from collections import Counter

KEY_LEN = 4


def determinant_inverse(m): # returns inverse of numpy.matrix M's determinant
    detM = round(numpy.linalg.det(m))
    detM = detM % hill_tools.CHAR_LENGTH
    return __mod_inverse__(int(detM))

def looper(pT,cT):
    for i in range(2,100):
        #if i > 7:
        print "currently @",i,"by key size"
        x,y,z = anal.do_process(pT,cT,None,i)
        for j in range(0,min(len(z),KEY_LEN)):
            dc = hill_tools.decode(y,z[j])
            c = Counter(dc)
            f = c.most_common(3)
            if f[0][0] == " " and f[1][0] == "e" and f[2][0] == "t":
                return z[j]

##### CLI STUFF ########
if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Cryptanalyze hill cipher')
    p.add_argument('plaintext', metavar='pt')
    p.add_argument('ciphertext',metavar='ct')
    arg = p.parse_args()
    
    c = looper(arg.plaintext,arg.ciphertext)

    if c != None:
        ess = []
        q = numpy.array(c)
    
        for j in range(0,len(q)):
            for h in range(0,len(q)):
                ess.append(q[j][h])
    
        f = open("KEY",'w')
        cPickle.dump(ess,f)
        f.close()
        
        print "wrote key file out"
    else:
        print "no key found; try manual"
