##########################
# Author: Sadia Khalil
# Email:  skhalil@cern.ch
# Date :  May 13th, 2018
#
# Description: Script that reads columns (run number, lumi section, inst. lumi, and pileup) from the input text file
# In a nested loop, a run is matched to the one in previous loop, and total lumi is calculated. Counter indices (j) are stored for the nested loop
# If the indices j are matched to the outer loop index (i), then event is skip until new run arrives
# A map of run, total integrated lumi, ave. inst. lumi, and ave. pileup is produced.
##########################

#!/usr/bin/env python
import os, sys


class readLumiInfo:
    def __init__(self, minRun, maxRun, minInstLumi, maxInstLumi, inputFile):
        self.minR        = minRun
        self.maxR        = maxRun
        self.minInstLumi = minInstLumi
        self.maxInstLumi = maxInstLumi
        self.inF         = inputFile
        #def prepareMaps (self, mapLumi):
        #    self.mapLumi.append(mapLumi)
            
        lumis       = [line.strip() for line in open(self.inF, 'r')]
        ave_instl   = [];
        ave_pu      = [];
        run_list    = [];
        tot_lumi    = [];
        repeat      = []; # indices of matched runs
        runls_list  = [];
        instls_list = [];
        puls_list   = [];
        totLumi = 0
        #print '{0:<6} {1:<6} {2:<6} {3:<6}'.format('run', 'integlumi', 'ave instlumi.', 'ave pu' )
        for i, l in enumerate(lumis):
            run_A, ls_A, instl_A, pileup_A = l.split(' ')
            if run_A < str(minRun) or run_A > str(maxRun) or run_A == '0': continue
            if i in repeat: continue # if the run is counted in bottom loop, then skip it
            del repeat[:] # reset
            #totLumi = 0
            totPileup = 0
            totInstLumi = 0
            runsls = 0
            count = 0 # indices of only good lumisections
            for j, k in enumerate(lumis):
                run_B, ls_B, instl_B, pileup_B = k.split(' ')
                if run_B == '0': continue 
                if run_A == run_B:
                    repeat.append(j)
                    # map the good runls for certain range of lumi-sec
                    if not (float(instl_B)/23.3104 < minInstLumi or float(instl_B)/23.3104 > maxInstLumi):
                        runsls = float(run_B) * 100000 + float(ls_B) # first six digits as run number and last five as lumi-sections
                        runls_list.append(runsls)
                        instls_list.append( round(float(instl_B)/23.3104, 4) )
                        puls_list.append( round(float(pileup_B), 4) )
                    
                    totLumi =  totLumi + float(instl_B) #in nb
                    totPileup = totPileup + float(pileup_B)
                    totInstLumi = totInstLumi + float(instl_B)/23.3104 # /nb/s

                    if instl_B != '0.000000' : count = count+1            
                else: continue
                
            # prepare the lists
            if count != 0 :
                #print '{0:<6} {1:<12.3f} {2:<6.3f} {3:<6.3f}'.format(run_A, totLumi/1000000., totInstLumi/float(count), totPileup/float(count) )
                ave_instl.append(round(totInstLumi/float(count), 4))
                ave_pu.append(round(totPileup/float(count), 4))
            elif totLumi != 0.0:
                #print '{0:<6} {1:<12.3f} {2:<6.3f} {3:<6.3f}'.format(run_A, totLumi/1000000., 0., 0. )
                ave_instl.append(0.0)
                ave_pu.append(0.0)

            run_list.append(int(run_A))
            tot_lumi.append(round(totLumi, 3))

        map_runls_instLumi_PU = zip(runls_list, instls_list, puls_list)
        map_run_totLumi_instLumi_avePU = zip (run_list, tot_lumi, ave_instl, ave_pu)
        self.map_runls_instLumi_PU           = map_runls_instLumi_PU
        self.map_run_totLumi_instLumi_avePU  = map_run_totLumi_instLumi_avePU
       
       
## Test it! #######            
#x = readLumiInfo(314090, 316994, 3.0, 6.0, 'run_ls_instlumi_pileup_2018_1.txt')
#print x.map_runls_instLumi_PU
#print x.map_run_totLumi_instLumi_avePU

## optional
'''
thefile2 = open('map_runls_instLumi_PU.txt', 'w')
for item in x.map_runls_instLumi_PU:
    print>>thefile2, item
    
thefile1 =  open('map_run_totLumi_instLumi_avePU.txt', 'w')
for item in  x.map_run_totLumi_instLumi_avePU:
    print>>thefile1, item  
'''  
#####################
