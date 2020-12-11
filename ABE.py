# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 13:25:26 2020

@author: marti
"""

import numpy as np
import random

def send(key, code):
    if key==1:
        if code==1:
            ang=90
        else:
            ang=0
    else:
        if code==0:
            ang=45
        else:
            ang=-45
    return ang

def recieve(key, ang):
    if ang==45 or ang==-45:
        keyang=0
    else:
        keyang=1
    
    if keyang!=key:
        code=random.randint(0,1)
    else:
        if ang==90 or ang==-45:
            code=1
        else:
            code=0
    return code

def alice(key, code):
    '''
    This function will reproduce the laser signal following the EDU-QCRY1/M setup from thorlabs.
    The first argument should be your key, this will be an array containing 1 and 0 randomly or if you want a specific key put in the 1 and 0 specificly.
    The second argument should be your code written in single bits.
    This will returen an array of angles of the polarisation of the laserbeam.
    '''
    signal=[]
    for i in range(len(code)):
        signal=np.append(signal,[send(key[i%len(key)],code[i])])
    return signal

def bob(key, signal):
    '''
    This function will reproduce the recieving of a lasersignal following the EDU-QCRY1/M setup from thorlabs.
    The first argument should be your key, this will be an array containing 1 and 0 randomly or if you want a specific key put in the 1 and 0 specificly.
    The second argument should be your angle of polarisation send to the reciever.
    '''
    code=[]
    for i in range(len(signal)):
        code=np.append(code,recieve(key[i%len(key)],signal[i]))
    return code.astype(int)

def eve(key, signal):
    '''
    This function is a combination of the bob and alice function in order.
    '''
    code=bob(key, signal)
    send=alice(key,code)
    return code, send

#actual code

keya=np.random.randint(0,2,10)
mesa=np.random.randint(0,2,10)
keyb=np.random.randint(0,2,10)
keye=np.random.randint(0,2,10)

sig=alice(keya,mesa)
mesb=bob(keyb,sig)
mese,sig2=eve(keye,sig)
mesb2=bob(keyb,sig2)
detect=abs(mesb-mesb2)

#saving the file
np.savetxt("ABS.txt", [keya,mesa,sig,keyb,mesb,keye,mese,sig2,mesb2,detect],fmt="%s",delimiter="\t")