# TrackerMacros

# readLumi.py
A class that takes an input .txt file that is generated using brilcalc and has information of run, lumi section, inst. lumi, and pileup per lumi section. A class called readLumi.py produces desired maps of run, ls, inst. lumi, integ. lumi, and PU for a given run range

The file lumiarray.npy is made using the input text file: run_ls_instlumi_pileup_2018_all.txt. 

#openNumpy.py
The script open the file lumiarray.npy, and trim the table in it to the desired run range, and produces another numpy array output file.

# fitting.C
A standalone macro to perform landau convoluted with gaussian fit to the cluster charge distribution

# drawClusterProperties.py
This macro produces cluster properties (if charge, then both the MP value & Ave value) vs integrated lumi, and also 1D histogram of cluster properties. The entries of the TTree are matched to the run and ls from the maps produced by readLumi.py, and cluster property vs lumi or pileup is produced.  

# plotClusterPropLumi.py
Draw the history plot of cluster property (charge MPV, sizeX, sizeY) vs integrated or instantaneous lumis. 

# plotClusterProp.py
Draw the 1D distribution of cluster property (charge MPV, sizeX, sizeY). 
 
# quickTestFitLandau.py
This is an independent macro that directly draws cluster properties from TTree and can't be maped with the luminosity information 
