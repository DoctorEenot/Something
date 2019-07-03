'''
Graphic engine for console, Maybe I should die
after import clears screen.
'''

#!/usr/bin/env python
from __future__ import print_function
import subprocess as sub
import time
def Logo():
    print("Created by DrEenot, inspired by Saitan")
Logo()
time.sleep(0.6)
sub.call('cls',shell=True)

class WorkArea:
    def __init__(self,size,MainSymbol):
        #sub.call('cls',shell=True)
        '''
        
        size is typle (width,height)
        Main Symbol is a symbol, which will be used for creating borders of work area
        '''
        self.size = size
        try:
            self.MainSymbol = str(MainSymbol)
        except:
            raise Exception('Something wrong with symbol, try another')
    def Write(self,buffer):
        '''
        Writes raw buffer of pixels
        buffer is array of 'pixels' - Example : symbols [['#','!','*'],
                                                         ['#','!','*']]
        Nothing = ' '
        '''
        if len(buffer) > self.size[0]:
            raise Exception('Wrong Number of lines in input buffer expected ' + str(self.size[0]))

        print(self.MainSymbol * (self.size[0] + 2),end = '\n')

        for y in range(self.size[1]):
            print(self.MainSymbol,end = '')
            print(''.join(buffer[y]) , end = '')
            print(self.MainSymbol,end = '\n')
            #time.sleep(0.01)
        print(self.MainSymbol * (self.size[0] + 2),end = '\n')

    def Clear(self):
        sub.call('cls',shell=True)

class Scene:
    def __init__(self,size,Symbol):
        self.size = size
        self.Symbol = Symbol
        self.scene = []
    def CreateScene(self):
        buf = []
        for i in range(self.size[0]):
            buf.append(self.Symbol)
        for i in range(self.size[1]):
            self.scene.append(buf.copy())