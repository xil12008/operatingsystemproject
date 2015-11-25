import heapq
import operator
from collections import deque
import pdb
import sys
import Queue as Q
import logging
logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

class Memory():
    def __init__(self, fitmethod):
        self.cap = 256
        self.mem = ['.' for _ in range(self.cap)]
        self.head = 0
        self.fitmethod = fitmethod
    
    def printmem(self):
        print "=" * 32
        for i in range(8):
            for j in range(32):
                sys.stdout.write(self.mem[i*32+j])
            sys.stdout.write("\n")
        print "=" * 32
 
    def __allocate_put(self, last, size, ID):
        for i in range(last, last+size):
            self.mem[i] = ID 
        self.head = last + size 

    def __allocate_firstfit(self, size, ID, startlocation = 0, endlocation = -1):
        last = -1 
        if endlocation == -1: endlocation = self.cap
        for i in range(startlocation, endlocation): 
            if self.mem[i] == '.':
                if last == -1:
                    last = i 
                if last != -1 and i-last+1 >= size:
                    self.__allocate_put(last, size, ID)
                    return True
            else:
                last = -1
        return False
  
    def __allocate_nextfit(self, size, ID):
        if self.__allocate_firstfit(size, ID, startlocation = self.head) :
            return True
        else:
            return self.__allocate_firstfit(size, ID, endlocation = self.head)

    def __allocate_bestfit(self, size, ID):
        count = {}
        last = -1 
        for i in range(self.cap): 
            if self.mem[i] == '.':
                if last == -1:
                    last = i 
            else:
                if last != -1 :
                    if i - last >= size:
                        count[last] = i - last
                last = -1
        if last != -1: 
            if self.cap - last >= size:
                count[last] = self.cap - last

        if not count: return False
        minpair = min(count.iteritems(), key=operator.itemgetter(1))
        if minpair[1] >= size:
            self.__allocate_put(minpair[0], size, ID)
            return True
        else:
            return False
 
    def deallocate(self, ID):
        for i in range(self.cap):
            if self.mem[i] == ID: 
                self.mem[i] = '.'
    
    def allocate(self, size, ID):
        if self.fitmethod == "firstfit":
            return self.__allocate_firstfit(size, ID)
        elif self.fitmethod == "nextfit":
            return self.__allocate_nextfit(size, ID)
        elif self.fitmethod == "bestfit":
            return self.__allocate_bestfit(size, ID)
   
    def defragment(self):
        newi = 0
        count = 0
        for i in range(self.cap):
            if self.mem[i] != '.': 
                tmp = self.mem[i]
                self.mem[i] = '.'
                self.mem[newi] = tmp 
                if i != newi: count += 1
                newi += 1
        return count 
