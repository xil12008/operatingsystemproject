import heapq
from collections import deque
import pdb
import sys
import string
import Queue as Q
import logging
logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

from CPU import CPU
from processqueue import ProcessQueue 
from processinfo import ProcessInfo 
from simulator import Simulator 


"""
NOTE: THIS PROGRAM IS DEVELOPED UNDER PYTHON 2.7
      In python 3.0, the notation for queue is different than ver. < 3.0
"""

if(__name__=="__main__"):
    infile = r"./processes.txt"
    if len(sys.argv)>1 and str(sys.argv[1]):
        infile = str(sys.argv[1]) 
    with open(infile) as f:
        f = f.readlines()
    processList = []
    linecount = 0
    for line in f:
         if(line.strip() and line[0]=='#'):
             continue 
         segments = line.strip().split('|')
         if(len(segments)!=6):
             #print "Wrong Input Line:", line 
             continue
         else:
             linecount += 1
             processList.append( (linecount,\
                                 segments[0],\
                                 int(segments[1]),\
                                 int(segments[2]),\
                                 int(segments[3]),\
                                 int(segments[4]),\
				 int(segments[5]) )   
                                )

    #queueTypeList = ['FCFS', 'SRT', 'PWA']
    #queueTypeList = ['SRT']
    queueTypeList = ['SRT', 'RR']
    memTypeList = ['nextfit', 'bestfit', 'firstfit']
  
    burst_num = 0
    urg_burst_sum = 0 
    for ptuple in processList:
        burst_num += ptuple[3]
        urg_burst_sum += ptuple[2] * ptuple[3] 

    outfile = open("simout.txt", "w")
    for qtype in queueTypeList: 
        for mtype in memTypeList:
            print "time 0ms: Simulator started for RR (t_slice 80) and ",
            sys.stdout.write(mtype[:-3].capitalize()+"-"+mtype[-3:].capitalize())
            print ""
            cpu = CPU(queuetype=qtype, memtype = mtype)
            for ptuple in processList:
                cpu.addProcess(ProcessInfo(*ptuple)) 
            cpu.run()
	    print ""
	    print ""
            outfile.write("Algorithm %s with %s\n" %(qtype, mtype))
            #outfile.write("-- average CPU burst time: %.2f ms\n" % (1.0 * cpu.burstTimeSum/burst_num))
            outfile.write("-- average CPU burst time: %.2f ms\n" % (1.0 * urg_burst_sum/burst_num))
            outfile.write("-- average wait time: %.2f ms\n" %(1.0 * cpu.waitTimeSum/ cpu.waitTimeNum)) 
            outfile.write("-- average turnaround time: %.2f ms\n" %(1.0 * cpu.waitTimeSum/ cpu.waitTimeNum + urg_burst_sum/burst_num))
            outfile.write("-- time spent on defragmentation : %.2f  ms %.2f/100\n" %(cpu.defragtime, (100.0 * cpu.defragtime / urg_burst_sum) )) 
            outfile.write("-- total number of context switches: %d\n" % cpu.contentSwitchSum)
    outfile.close()




    
