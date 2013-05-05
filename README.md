UPDATE MAY 1
============
way faster again, so that total.py is actually usable. specify plaintext, ciphertext & ciphertext 2 paths like:

    python total.py plaintext.txt ciphertext.txt to-decode.txt

and it will do its thing.

Individual Commands
-------------------
**hill_tools.py** has no interface.

**anal.py** takes 3 paramaters: the first is the plaintext of the plaintext/ciphertext (p/c) pair, the second is the ciphertext of the p/c pair, and the third is the suspected key length.
for greater control, anal.py's global variable MKEY_LENGTH can be manually edited to return a greater or smaller number of possible keys.

**enc.py** is for quick encoding & key creation; the first argument is the thing to encode, second is the key to use, third is where to save enciphered text, and fourth is where to save **dec.py** compatible key.
the key must be supplied in a text file as a string of numbers seperated by spaces. **enc.py** will also check to make sure that your key can be used to decipher and warn you if it cannot.

**dec.py** is made for quick decoding: the first paramater is the path to the ciphertext, and the second paramater is the path to the key (cPickle'd numpy array format- what **anal.py** produces).

**total.py** is the automated decoder; it tries all possible keys of all possible lengths given the restrictions of the p/c pair length. The first paramater is plaintext, second is ciphertext of p/c pair, and the third paramater is the cipher text you wish to decode.

