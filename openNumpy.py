#!/usr/bin/env python
import os, sys
import numpy as np

data = np.load('lumiarray.npy')

#print data
RUN = '323376'


#for i, row in enumerate(data):
#    print(row[0], row[1], row[2], row[3])
#    if str(row[0])[0:6] != RUN: np.delete(data, i, 0)

indices = [i for (i, row) in  enumerate(data) if str(row[0])[0:6] != RUN]
print('Keeping {0:<3.0f} rows out of {1:<3.0f} rows for RUN {2:s}' ).format((data.shape[0] - len(indices)),  data.shape[0], RUN)
b = np.delete(data, indices, 0)
print('b', b)
np.save('lumiMap_'+RUN+'.npy', b)

#unmatched = [i for (i,v) in enumerate(    
#for x in np.nditer(data):
#    print x   

#for (x, y), value in np.ndenumerate(data):
#    print x,y

