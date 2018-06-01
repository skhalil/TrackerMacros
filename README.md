# TrackerMacros

# readLumi.py
A class that takes an input .txt file that is generated using brilcalc and has information of run, lumi section, inst. lumi, and pileup per lumi section. A class called readLumi.py produces desired maps of run, ls, inst. lumi, integ. lumi, and PU for a given run range

# fitting.C
A standalone macro to perform landau convoluted with gaussian fit to the cluster charge distribution

# drawClusterProperties.py:
This macro produces cluster properties (if charge, then both the MP value & Ave value) vs integrated lumi, and also 1D histogram of cluster properties. The entries of the TTree are matched to the run and ls from the maps produced by readLumi.py, and cluster property vs lumi or pileup is produced.  

# quickTestFitLandau.py
This is an independent macro that directly draws cluster properties from TTree and can't be maped with the luminosity information 
