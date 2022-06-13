#!/usr/bin/env python

##  FaultInjectionDemo.py
##  Avi Kak (March 30, 2015)

##  This script demonstrates the fault injection exploit on the CRT step of the
##  of the RSA algorithm.

##  GCD calculator (From Lecture 5)
def gcd(a,b):                                                                            #(1)
    while b:                                                                             #(2)
        a,b = b, a%b                                                                     #(3)
    return a                                                                             #(4)

##  The code shown below uses ordinary integer arithmetic implementation of
##  the Extended Euclid's Algorithm to find the MI of the first-arg integer
##  vis-a-vis the second-arg integer. (This code segment is from Lecture 5)
def MI(num, mod):                                                                        #(5)
    '''
    The function returns the multiplicative inverse (MI) of num modulo mod
    '''
    NUM = num; MOD = mod                                                                 #(6)
    x, x_old = 0L, 1L                                                                    #(7)
    y, y_old = 1L, 0L                                                                    #(8)
    while mod:                                                                           #(9)
        q = num // mod                                                                  #(10)
        num, mod = mod, num % mod                                                       #(11)
        x, x_old = x_old - q * x, x                                                     #(12)
        y, y_old = y_old - q * y, y                                                     #(13)
    if num != 1:                                                                        #(14)
        raise ValueError("NO MI. However, the GCD of %d and %d is %u" \
                                                          % (NUM, MOD, num))            #(15)
    else:                                                                               #(16)
        MI = (x_old + MOD) % MOD                                                        #(17)
        return MI                                                                       #(18)


# Set RSA params:
p = 211                                                                                 #(19)
q = 223                                                                                 #(20)
n = p * q                                                                               #(21)
print "RSA parameters:"
print "p = %d     q = %d    modulus = %d" % (p, q, n)                                   #(22)
totient_n = (p-1) * (q-1)                                                               #(23)
# Find a candidate for public exponent:         
for e in range(3,n):                                                                    #(24)
    if (gcd(e,p-1) == 1) and (gcd(e,q-1) == 1):                                         #(25)
        break                                                                           #(26)
print "public exponent e = ", e                                                         #(27)
# Now set the private exponent: 
d = MI(e, totient_n)                                                                    #(28)
print "private exponent d = ", d                                                        #(29)


message = 6789                                                                          #(30)
print "\nmessage = ", message                                                           #(31)

# Implement the Chinese Remainder Theorem to calculate
# message to the power of d mod n:
dp = d % (p - 1)                                                                        #(32)
dq = d % (q - 1)                                                                        #(33)
V_p = ((message % p) ** dp) % p                                                         #(34)
V_q = ((message % q) ** dq) % q                                                         #(35)

signature = (q * MI(q, p) * V_p   + p * MI(p, q) * V_q) % n                             #(36)

print "\nsignature = ", signature                                                       #(37)

import random                                                                           #(38)

print "\nESTIMATION OF q THROUGH INJECTED FAULTS:"
for i in range(10):                                                                     #(39)
    error = random.randrange(1,10)                                                      #(40)
    V_hat_p = V_p + error                                                               #(42)
    print "\nV_p = %d    V_hat_p = %d    error = %d" % (V_p, V_hat_p, error)            #(41)
    signature_hat = (q * MI(q, p) * V_hat_p   + p * MI(p, q) * V_q) % n                 #(43)
    q_estimate = gcd( (signature_hat ** e - message) % n, n)                            #(44)
    print "possible value for q = ", q_estimate                                         #(45)
    if q_estimate == q:                                                                 #(46)
        print "Attack successful!!!"                                                    #(47)
