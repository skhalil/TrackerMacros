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
import numpy as np
from ROOT import TH2F, TFile


class readLumiInfo:
    def __init__(self, minRun, maxRun, minInstLumi, maxInstLumi, inputFile):
        self.minR        = minRun
        self.maxR        = maxRun
        self.minInstLumi = minInstLumi
        self.maxInstLumi = maxInstLumi
        self.inF         = inputFile

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
        print '{0:<6} {1:<6} {2:<6} {3:<6}'.format('run', 'integlumi', 'ave instlumi.', 'ave pu' )
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
                    #map the good runls for certain range of lumi-sec
                    #if not (float(instl_B)/23.3104 < minInstLumi or float(instl_B)/23.3104 > maxInstLumi):
                    runsls = float(run_B) * 100000 + float(ls_B) # first six digits as run number and last five as lumi-sections
                    runls_list.append(runsls)
                    instls_list.append( float(instl_B)/23.3104)
                    puls_list.append( float(pileup_B) )
                    
                    totLumi =  totLumi + float(instl_B) #in nb
                    totPileup = totPileup + float(pileup_B)
                    totInstLumi = totInstLumi + float(instl_B)/23.3104 # /nb/s

                    if instl_B != '0.000000' : count = count+1            
                else: continue
                
            # prepare the lists
            if count != 0 :         
                if run_A == str(maxRun): print '{0:<6} {1:<12.3f} {2:<6.3f} {3:<6.3f}'.format(run_A, totLumi/1000000., totInstLumi/float(count), totPileup/float(count) )
                ave_instl.append(totInstLumi/float(count))
                ave_pu.append(totPileup/float(count))
            elif totLumi != 0.0:
                if run_A == str(maxRun): print '{0:<6} {1:<12.3f} {2:<6.3f} {3:<6.3f}'.format(run_A, totLumi/1000000., 0., 0. )
                ave_instl.append(0.0)
                ave_pu.append(0.0)

            run_list.append(int(run_A))
            tot_lumi.append(totLumi)
        print 'len runls: ', len(runls_list), 'len instls: ', len(instls_list), 'len puls: ', len(puls_list), 'len integ lumi per event: ', len(tot_lumi)
        
        
        map_runls_instLumi_PU           = zip(runls_list, instls_list, puls_list)
        map_run_totLumi                 = zip(run_list, tot_lumi)        
        self.map_runls_instLumi_PU      = map_runls_instLumi_PU
        self.map_run_totLumi            = map_run_totLumi

        total_lumi = []
        for runls_m, instlumi_m, pu_m in map_runls_instLumi_PU:
            for run_m, totlumi_m in map_run_totLumi:
                if int(str(runls_m)[0:6]) == run_m:
                    total_lumi.append(totlumi_m/1000000)
        print 'size of total lumi', len(total_lumi)            

        map_runls_instLumi_intLumi_PU = zip(runls_list, instls_list, total_lumi, puls_list)
        self.map_runls_instLumi_intLumi_PU = map_runls_instLumi_intLumi_PU
        #print map_runls_instLumi_intLumi_PU 
## Test it! #######            
#lMaps = readLumiInfo(314090, 317696, 0.0, 1000.0, 'run_ls_instlumi_pileup_2018.txt')###
#lMaps = readLumiInfo(316715, 316716, 0.0, 1000.0, 'run_ls_instlumi_pileup_2018.txt')
lMaps = readLumiInfo(314090, 326483, 0.0, 1000.0, 'run_ls_instlumi_pileup_2018_all.txt')#315782
a = []
for item in lMaps.map_runls_instLumi_intLumi_PU:
    #print item[0]
    a.append([item[0], item[1], item[2], item[3]])
    #b.append(item[1])
    #print a
atest = np.array(a)
print atest
print atest.shape

np.save('lumiarray.npy', atest)

# map of inst lumi vs integrated lumi
#hist = TH2F('InstVsInt', 'InstVsInt', 30, 0.0, 35.0, 25, 0.0, 25.0)
#hist.GetXaxis().SetTitle('Integrated Lumi (fb^{-1})')
#hist.GetYaxis().SetTitle('Instantaneous Lumi (nb^{-1} s^{-1})')
#for runls_m, instlumi_m, pu_m in lMaps.map_runls_instLumi_PU:
#    for run_m, totlumi_m in lMaps.map_run_totLumi:
#        if int(str(runls_m)[0:6]) == run_m:
#            hist.Fill(totlumi_m/1000000., instlumi_m)
            #print 'totlumi',   totlumi_m/1000000., 'inst lumi', instlumi_m
#f_out = TFile('lumiMap.root', "RECREATE")
#hist.Write()
#f_out.Close()

#print x.map_runls_instLumi_PU
#print x.map_run_totLumi

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
#thefile = open('map_runls_instLumi_intLumi_PU.txt', 'w')
#for item in lMaps.map_runls_instLumi_intLumi_PU:
#    print>>thefile, item
