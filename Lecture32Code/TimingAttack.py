#!/usr/bin/env python

##  TimingAttack.py

##  Avi Kak (kak@purdue.edu)
##  April 13, 2015

##  This script demonstrates the basic idea of how the Timing Attack can be
##  used to infer the bits of the private exponent used in calculating RSA
##  based digital signatures.

##  CAVEATS: This simple implementation is based on one possible
##           interpretation of the original paper on timing attacks by Paul
##           Kocher.  Note that this implementation has only been tried on
##           8-bit moduli. 

##           I am quite certain that this extremely simpleminded implementation
##           will NOT to work on RSA moduli of the size that are actually used 
##           in working algorithms.

##           For a more credible timing attack, you would need to include
##           in this implementation the probabilstic logic described in the
##           paper "A Practical Implementation of the Timing Attack'' by
##           Dhem, Koeune, Leroux, Mestre, Quisquater, and Willems.

import time
import random
import math

class TimingAttack( object ):                                                           #(I1)

    def __init__( self, **kwargs ):                                                     #(J2)
        if kwargs.has_key('num_messages'): num_messages = kwargs.pop('num_messages')    #(J3)
        if kwargs.has_key('num_trials'): num_trials = kwargs.pop('num_trials')          #(J3)
        if kwargs.has_key('private_exponent'): private_exponent = kwargs.pop('private_exponent')
                                                                                        #(J4)
        if kwargs.has_key('modulus_width'): modulus_width = kwargs.pop('modulus_width') #(J5)
        self.num_messages = num_messages                                                #(J6)
        self.num_trials = num_trials                                                    #(J7)
        self.modulus_width = modulus_width                                              #(J8)
        self.d  = private_exponent                                                      #(J9)
        self.d_reversed = '{:b}'.format(private_exponent)[::-1]                        #(J10)
        self.modulus =  None                                                           #(J11)
        self.list_of_messages = []                                                     #(J12)
        self.times_taken_for_messages = []                                             #(J13)
        self.bits_discovered_for_d = []                                                #(J14)
        self.correlations_cache = {}                                                   #(J15)

    def gen_modulus(self):                                                              #(G1)
        modulus =  self.gen_random_num_of_specified_width(self.modulus_width/2) * \
                        self.gen_random_num_of_specified_width(self.modulus_width/2)    #(G2)
        print "modulus is: ", modulus                                                   #(G3)
        self.modulus = modulus                                                          #(G4)
        return modulus                                                                  #(G5)


    def gen_random_num_of_specified_width(self, width):                                 #(R1)
        '''
        This function generates a random number of specified bit field width:
        '''
        candidate = random.getrandbits(width )                                          #(R2)
        if candidate & 1 == 0: candidate += 1                                           #(R3)
        candidate |= (1 << width - 1)                                                   #(R4)
        candidate |= (2 << width - 3)                                                   #(R5)
        return candidate                                                                #(R6)
    
    def modular_exponentiate(self, A, B):                                               #(X1)
        '''
        This is our basic function for modular exponentiation as explained in
        Section 12.5.1 of Lecture 12:
        '''
        if self.modulus is None:                                                        #(X2)
            raise SyntaxError("You must first set the modulus")                         #(X3)
        time_trace = []                                                                 #(X4)
        result = 1                                                                      #(X5)
        while B > 0:                                                                    #(X6)
            if B & 1:                                                                   #(X7)
                result = ( result * A ) % self.modulus                                  #(X8)
            B = B >> 1                                                                  #(X9)
            A = ( A * A ) % self.modulus                                               #(X10)
        return  result                                                                 #(X11)
    
    def correlate(self, series1, series2):                                              #(C1)
        if len(series1) != len(series2):                                                #(C2)
            raise ValueError("the two series must be of the same length")               #(C3)
        mean1, mean2 = sum(series1)/float(len(series1)),sum(series2)/float(len(series2))#(C4)
        mseries1, mseries2 = [x - mean1 for x in series1], [x - mean2 for x in series2] #(C5)
        products = [mseries1[i] * mseries2[i] for i in range(len(mseries1))]            #(C6)
        mseries1_squared, mseries2_squared = [x**2 for x in mseries1], [x**2 for x in mseries2]
                                                                                        #(C7)
        correlation = sum(products) / math.sqrt(sum(mseries1_squared) * sum(mseries2_squared))
                                                                                        #(C8)
        return correlation                                                              #(C9)
    
    def gen_messages(self):                                                             #(M1)
        '''
        Generate a list of randomly created messages.  The messages must obey the usual
        constraints on the two most significant bits:
        '''
        self.correlations_cache = {}                                                    #(M2)
        self.times_taken_for_messages = []                                              #(M3)
        self.list_of_messages = []                                                      #(M4)
        for i in range(self.num_messages):                                              #(M5)
            message = self.gen_random_num_of_specified_width(self.modulus_width)        #(M6)
            self.list_of_messages.append(message)                                       #(M7)
        print "Finished generating %d messages" % (self.num_messages)                   #(M8)
    
    def get_exponentiation_times_for_messages(self):                                    #(T1)
        '''
        For each message in list_of_messages, find the time it takes to calculate its 
        signature.  Average each time measurement over num_trials:
        '''
        if self.modulus is None:                                                        #(T2)
            raise SyntaxError("You must first set the modulus")                         #(T3)
        for message in self.list_of_messages:                                           #(T4)
            times = []                                                                  #(T5)
            for j in range(self.num_trials):                                            #(T6)
                start = time.time()                                                     #(T7)
                self.modular_exponentiate(message, self.d)                              #(T8)
                elapsed = time.time() - start                                           #(T9)
                times.append(elapsed)                                                  #(T10)
            avg = sum(times) / float(len(times))                                       #(T11)
            self.times_taken_for_messages.append(avg)                                  #(T12)
        print "Finished calculating signatures for all messages"                       #(T13)
        
    def find_next_bit_of_private_key(self, list_of_previous_bits):                      #(F1)
        '''
        Starting with the LSB, given a sequence of previously computed bits of the 
        private exponent d, now compute the next bit:
        '''
        num_set_bits = reduce(lambda x,y: x+y, \
                                 filter(lambda x: x == 1, list_of_previous_bits))       #(F2)
        correlation0,correlation1 = None,None                                           #(F3)
        arg_list1, arg_list2 = list_of_previous_bits[:], list_of_previous_bits[:]       #(F4)
        B = int(''.join(map(str, list(reversed(arg_list1)))), 2)                        #(F5)
        print "\nB = ", B                                                               #(F6)
        if B in self.correlations_cache:                                                #(F7)
            correlation0 = self.correlations_cache[B]                                   #(F8)
        else:                                                                           #(F9)
            times_for_partial_exponentiation = []                                      #(F10)
            for message in self.list_of_messages:                                      #(F11)
                signature = None                                                       #(F12)
                times = []                                                             #(F13)
                for j in range(self.num_trials):                                       #(F14)
                    start = time.time()                                                #(F15)
                    self.modular_exponentiate(message, B)                              #(F16)
                    elapsed = time.time() - start                                      #(F17)
                    times.append(elapsed)                                              #(F18)
                avg = sum(times) / float(len(times))                                   #(F19)
                times_for_partial_exponentiation.append(avg)                           #(F20)
            correlation0 = self.correlate(self.times_taken_for_messages, \
                                            times_for_partial_exponentiation)          #(F22)
            correlation0 /= num_set_bits                                               #(F23)
            self.correlations_cache[B] = correlation0                                  #(F24)
        print "correlation0: ", correlation0                                           #(F25)
        # Now let's see the correlation when we try 1 for the next bit
        arg_list2.append(1)                                                            #(F26)
        B = int(''.join(map(str, list(reversed(arg_list2)))), 2)                       #(F27)
        print "B = ", B                                                                #(F28)
        if B in self.correlations_cache:                                               #(F29)
            correlation1 = self.correlations_cache[B]                                  #(F30)
        else:                                                                          #(F31)
            times_for_partial_exponentiation = []                                      #(F32)  
            for message in self.list_of_messages:                                      #(F33)
                signature = None                                                       #(F34)
                times = []                                                             #(F35)
                for j in range(self.num_trials):                                       #(F36)
                    start = time.time()                                                #(F37)
                    self.modular_exponentiate(message, B)                              #(F38)
                    elapsed = time.time() - start                                      #(F39)
                    times.append(elapsed)                                              #(F40)
                avg = sum(times) / float(len(times))                                   #(F41)
                times_for_partial_exponentiation.append(avg)                           #(F42)
            correlation1 = self.correlate(self.times_taken_for_messages, \
                                                  times_for_partial_exponentiation)    #(F43)
            correlation1 /= (num_set_bits + 1)                                         #(F44)
            self.correlations_cache[B] = correlation1                                  #(F45)
        print "correlation1: ", correlation1                                           #(F46)
        if correlation1 > correlation0:                                                #(F47)
            return 1                                                                   #(F48)
        else:                                                                          #(F49)
            return 0                                                                   #(F50) 

    def discover_private_exponent_bits(self):                                           #(D1)
        '''
        Assume that the private exponent will always be odd and that, therefore, its
        LSB will always be 1.  Now try to discover the other bits.
        '''  
        discovered_bits = [1]                                                           #(D2)
        for bitpos in range(1, self.modulus_width):                                     #(D3)
            nextbit = self.find_next_bit_of_private_key(discovered_bits)                #(D4)
            print "value of next bit: ", nextbit                                        #(D5)
            print "its value should be: ", self.d_reversed[bitpos]                      #(D6)
            if nextbit != int(self.d_reversed[bitpos]):                                 #(D7)
                raise ValueError("Wrong result for bit at index %d" % bitpos)           #(D8)
            discovered_bits.append(nextbit)                                             #(D9)
            print "discovered bits: ", discovered_bits                                 #(D10)
        self.bits_discovered_for_d = discovered_bits                                   #(D11)
        return discovered_bits                                                         #(D12)

if __name__ == '__main__':

    private_exponent = 0b11001011                                                       #(A1)
    timing_attack = TimingAttack(                                                       #(A2)
                          num_messages = 100000,                                        #(A3)
                          num_trials = 1000,                                            #(A4)
                          modulus_width = 8,                                            #(A5)
                          private_exponent = private_exponent,                          #(A6)
                    )
    modulus_to_discovered_bits = {}                                                     #(A7)
    for i in range(10):                                                                 #(A8)
        print "\n\n============Starting run %d of the overall experiment=============\n" % i
                                                                                        #(A9)
        discovered_bits = []                                                           #(A10)
        timing_attack.gen_messages()                                                   #(A11)
        modulus = timing_attack.gen_modulus()                                          #(A12)
        timing_attack.get_exponentiation_times_for_messages()                          #(A13)
        try:                                                                           #(A14)
            discovered_bits = timing_attack.discover_private_exponent_bits()           #(A15)
        except ValueError, e:                                                          #(A16)
            print "exception caught in main:", e                                       #(A17)
            e = str(e).strip()                                                         #(A18)
            if e[-1].isdigit():                                                        #(A19)
                pos = int(e.split()[-1])                                               #(A20)
                print "\n                                  Got %d bits!!!" % pos       #(A21)
            continue                                                                   #(A22)
        if discovered_bits:                                                            #(A23)
            modulus_to_discovered_bits[i] = \
                       (modulus, ''.join(map(str, list(reversed(discovered_bits)))))   #(A24)
        print "\n                                                SUCCESS!!!!!!!"       #(A25)

#d = 0b11001011                                                       #(A1)
