#!/usr/bin/env python

##  A5_1.py
##  Avi Kak (kak@purdue.edu)
##  April 21, 2015

##  This is a Python implementation of the C code provided by Marc Briceno, Ian
##  Goldberg, and David Wagner at the following website:
##
##     http://www.scard.org/gsm/a51.html      
##
##  For accuracy, I have compared the output of this Python code against the test
##  vector provided by them.

##  The A5/1 algorithm is used in 2G GSM for over-the-air encryption of voice and SMS
##  data. On the basis of the cryptanalysis of this cipher and the more recent
##  rainbow table attacks, the A5/1 algorithm is now considered to provide virtually
##  no security at all.  Nonetheless, it forms an interesting case study that shows
##  that when security algorithm are not opened up to public scrutiny (because some
##  folks out there believe in "security through obscurity"), it is possible for such
##  an algorithm to become deployed on a truly global basis before its flaws become
##  evident.

##  The A5/1 algorithm is a bit-level stream cipher based on three LFSR (Linear
##  Feedback Shift Register). The basic operation you carry out in an LFSR at each
##  clock tick consists of the following three steps: (1) You record the bits at the
##  feedback taps in the register; (2) You shift the register by one bit position
##  towards the MSB; and (3) You set the value of the LSB to an XOR of the feedback
##  bits.  When you are first initializing a register with the encryption key, you
##  add a fourth step, which is to XOR the LSB with the key bit corresponding to that
##  clock tick, etc.

from BitVector import *

#  The three shift registers
R1,R2,R3 = BitVector(size=19),BitVector(size=22),BitVector(size=23)                     #(1)

# Feedback taps
R1TAPS,R2TAPS,R3TAPS = BitVector(size=19),BitVector(size=22),BitVector(size=23)         #(2)
R1TAPS[13] = R1TAPS[16] = R1TAPS[17] = R1TAPS[18] = 1                                   #(3)
R2TAPS[20] = R2TAPS[21] = 1                                                             #(4)
R3TAPS[7] = R3TAPS[20] = R3TAPS[21] = R3TAPS[22] = 1                                    #(5)

print "R1TAPS: ", R1TAPS                                                                #(6)
print "R2TAPS: ", R2TAPS                                                                #(7)
print "R3TAPS: ", R3TAPS                                                                #(8)

keybytes = [BitVector(hexstring=x).reverse() for x in ['12', '23', '45', '67', \
                                                       '89', 'ab', 'cd', 'ef']]         #(9)
key = reduce(lambda x,y: x+y, keybytes)                                                #(10)
print "encryption key: ", key                                                          #(11)

frame = BitVector(intVal=0x134, size=22).reverse()                                     #(12)
print "frame number: ", frame                                                          #(13)

##  We will store the two output keystreams in these two BitVectors, each of size 114
##  bits.  One is for the uplink and the other for the downlink:
AtoBkeystream  = BitVector(size = 114)                                                 #(14)
BtoAkeystream  = BitVector(size = 114)                                                 #(15)

##  This function used by the clockone() function.  As each shift register is
##  clocked, the feedback consists of the parity of all the tap bits:
def parity(x):                                                                         #(16)
    countbits = x.count_bits()                                                         #(17)
    return countbits  % 2                                                              #(18)

##  In order to decide whether or not a shift register should be clocked at a given
##  clock tick, we need to examine the clocking bits in each register and see what the
##  majority says:
def majority():                                                                        #(19)
    sum = R1[8] + R2[10] + R3[10]                                                      #(20)
    if sum >= 2:                                                                       #(21)
        return 1                                                                       #(22)
    else:                                                                              #(23)
        return 0                                                                       #(24)

##  This function clocks just one register that is supplied as the first arg to the
##  function.  The second argument must indicate the bit positions of the feedback
##  taps for the register.
def clockone(register, taps):                                                          #(25)
    tapsbits = register & taps                                                         #(26)
    register.shift_right(1)                                                            #(27)
    register[0] = parity(tapsbits)                                                     #(28)

##  This function is needed for initializing the three shift registers.
def clockall():                                                                        #(29)
    clockone(R1, R1TAPS)                                                               #(30)
    clockone(R2, R2TAPS)                                                               #(31)
    clockone(R3, R3TAPS)                                                               #(32)

##  This function initializes the three shift registers with, first, the 64-bit
##  encryption key, then with the 22 bits of frame number, and, finally, by simply
##  clocking the registers 100 times to create the 'avalanche' effect.  Note that
##  during the avalanche creation, clocking of each register now depends on the
##  clocking bits in all three registers.
def setupkey():                                                                        #(33)
    #  Clock into the registers the 64 bits of the encryption key:
    for i in range(64):                                                                #(34)
        clockall()                                                                     #(35)
        R1[0] ^= key[i]; R2[0] ^= key[i]; R3[0] ^= key[i]                              #(36)
    #  Clock into the registers the 22 bits of the frame number:
    for i in range(22):                                                                #(37) 
        clockall()                                                                     #(38)
        R1[0] ^= frame[i]; R2[0] ^= frame[i]; R3[0] ^= frame[i]                        #(39)
    #  Now clock all three registers 100 times, but this time let the clocking
    #  of each register depend on the majority voting of the clocking bits:
    for i in range(100):                                                               #(40)
        maj = majority()                                                               #(41)
        if (R1[8]  != 0) == maj: clockone(R1, R1TAPS)                                  #(42)
        if (R2[10] != 0) == maj: clockone(R2, R2TAPS)                                  #(43)
        if (R3[10] != 0) == maj: clockone(R3, R3TAPS)                                  #(44)

##  After the three shift registers are initialized with the encryption key and the
##  frame number, you are ready to run the shift registers to produce the two bit 114
##  bits long keystreams, one for the uplink and the other for the downlink.
def run():                                                                             #(45)
    global AtoBkeystream, BtoAkeystream                                                #(46)
    keystream = BitVector(size=228)                                                    #(47)
    for i in range(228):                                                               #(48)
        maj = majority()                                                               #(49)
        if (R1[8]  != 0) == maj: clockone(R1, R1TAPS)                                  #(50)
        if (R2[10] != 0) == maj: clockone(R2, R2TAPS)                                  #(51)
        if (R3[10] != 0) == maj: clockone(R3, R3TAPS)                                  #(62)
        keystream[i] = R1[-1] ^ R2[-1] ^ R3[-1]                                        #(53)
    AtoBkeystream = keystream[:114]                                                    #(54)
    BtoAkeystream = keystream[114:]                                                    #(55)

##  Initialize the three shift registers:
setupkey()                                                                             #(56)
##  Now produce the keystreams:
run()                                                                                  #(57)

##  Display the two keystreams:
print "\nAtoBkeystream:       ", AtoBkeystream                                         #(58)
print "\nBtoAkeystream:       ", BtoAkeystream                                         #(59)

##  Here are the correct values for the two keystreams:
goodAtoB = [BitVector(hexstring = x) for x in ['53','4e','aa','58','2f','e8','15','1a',\
                                               'b6','e1','85','5a','72','8c','00'] ]   #(60)     
goodBtoA = [BitVector(hexstring = x) for x in ['24','fd','35','a3','5d','5f','b6','52',\
                                               '6d','32','f9','06','df','1a','c0'] ]   #(61)
goodAtoB = reduce(lambda x,y: x+y, goodAtoB)                                           #(62)
goodBtoA = reduce(lambda x,y: x+y, goodBtoA)                                           #(63)

print "\nGood: AtoBkeystream: ", goodAtoB[:114]                                        #(64)
print "\nGood: BtoAkeystream: ", goodBtoA[:114]                                        #(65)

if (AtoBkeystream == goodAtoB[:114]) and (AtoBkeystream == goodAtoB[:114]):            #(66)
    print "\nSelf-check succeeded: Everything looks good"                              #(67)
