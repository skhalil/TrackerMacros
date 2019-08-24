#!/usr/bin/env python
import os, sys
import numpy as np
import json

golden_runs = []
with open('PromptReco_Collisions18_JSON.txt') as json_file:
    golden = json.load(json_file)
    jstr = json.dumps(golden, indent=4, sort_keys=True)
    for key, value in golden.items():
        golden_runs.append(key)
#print (jstr)
#print ('golden runs', golden_runs)
#print('size of golden runs', len(golden_runs))

data = np.load('lumiarray.npy')#lumiarray.npy''lumiMap_323376.npy')
'''
# filter the data array w.r.t golden runs. 
indices = []
for (i, row) in  enumerate(data):
    found = False
    repeatRunInRow = False
    if str(row[0])[6:] != '00001.0': repeatRunInRow=True
    for RUN in golden_runs:
        if str(row[0])[0:6] == RUN: found = True; break;
    if found==False or repeatRunInRow==True: indices.append(i)

data_update = np.delete(data, indices, 0)
print (data_update)
print ('size before', data.shape)
print ('size after', data_update.shape)
 
np.save('reducedlumiMap.npy', data_update)
exit()
'''
data2 = np.load('reducedlumiMap.npy')
# size = 441, root files: 333, so need to check which are missing

# filter runs
lumis = [4., 6., 8., 10., 12., 14., 16., 18., 20., 22., 24., 26., 28., 30., 32., 34., 36., 38, 40., 42., 44., 46., 48., 50., 52., 54., 56., 58., 60., 62., 64., 66., 68., 70.]

for l in range (len(lumis)-1):
    print (lumis[l], 'next:', (lumis[l+1]))

runs = []
dict_run_lumi = {}

for l in range (len(lumis)-1):
    #runs.clear() #python 37 feature
    del runs[:]
    for i, row in enumerate(data2):
        if row[2] < (lumis[l+1]) and row[2] >= lumis[l] :
            runs.append(str(row[0])[0:6])
        #print (len(runs))    
    dict_run_lumi[str(lumis[l])] = runs[:]#runs.copy() python 37 feature
    
#print(dict_run_lumi)
#print(json.dumps(dict_run_lumi, indent=4, sort_keys=True))
print("\n".join(">= {}\t{}".format(k, v) for k, v in dict_run_lumi.items()))





