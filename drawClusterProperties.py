#!/usr/bin/env python
import os, sys, math, array, operator
import numpy as np
from ROOT import gROOT, TFile, TChain, TF1, gStyle, gDirectory, TTree, TCanvas, TH1F, TH2F, TH1D, TProfile, TObjArray, TStopwatch, TGaxis, TLegend, TLatex, TDirectoryFile
from ROOT import kBlack, kGreen, kOrange, kGreen, kRed, kBlue, kTeal, kPink, kViolet
#gROOT.ProcessLine('.L ./fitting.C')
gROOT.SetBatch(True)
#from ROOT import fitting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
TGaxis.SetMaxDigits(3)

def setLeg(histo, legText):
    leg.AddEntry(histo, legText, "pl")

def setColor(histo, color, marker):
    histo.SetLineColor(color)  
    histo.SetMarkerStyle(marker)
    histo.SetMarkerColor(color)
    
def setHisto(histo, xTitle, yTitle, D2):
    histo.GetXaxis().SetTitle( xTitle )
    histo.GetYaxis().SetTitle( yTitle )
    histo.GetXaxis().SetTitleOffset(1.2)
    histo.GetYaxis().SetTitleOffset(1.4)
    histo.SetLineWidth(2)
    if D2:
        #histo.SetMarkerStyle(7)
        #histo.SetMarkerSize(0.2)
        histo.GetXaxis().SetNdivisions(510)
        histo.GetYaxis().SetNdivisions(510)
        
def fillHistos1D(chargeCuts, sizeXCuts, sizeYCuts, chInSubdet, sXInSubdet, sYInSubdet, ch, sX, sY):
    if chargeCuts: histo1D[chInSubdet].Fill(ch)
    if sizeXCuts:  histo1D[sXInSubdet].Fill(sX)
    if sizeYCuts:  histo1D[sYInSubdet].Fill(sY)

def fillHistos2D(chargeCuts, sizeXCuts, sizeYCuts, chInSubdetVsVar, sXInSubdetVsVar, sYInSubdetVsVar, var, ch, sX, sY):
    if chargeCuts: histo[chInSubdetVsVar].Fill(var, ch)
    if sizeXCuts:  histo[sXInSubdetVsVar].Fill(var, sX)
    if sizeYCuts:  histo[sYInSubdetVsVar].Fill(var, sY) 
# =============== 
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--verbose", action='store_true',
                  default=True,
                  dest="verbose",
                  help="print the event discription")

parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Plots/', 
                  dest='plotDir',
                  help='output directory of plots')

#parser.add_option('--inputRunLumiInfo', metavar='P', type='string', action='store',
#                  default='run_ls_instlumi_pileup_2018.txt', 
#                  dest='inputRunLumiInfo',
#                  help='input text file obtained from brilcal')

parser.add_option("--isMC", action='store_true',
                  default=True,
                  dest="isMC",
                  help="plots using MC")

parser.add_option('--minRun', metavar='P', type='int', action='store',
                  default='317650', 
                  dest='minRun',
                  help='minRun range to loop over ntuple entries')

parser.add_option('--maxRun', metavar='P', type='int', action='store',
                  default='317650', #'317650'
                  dest='maxRun',
                  help='maxRun range to loop over ntuple entries')

#parser.add_option('--minInstLumi', metavar='P', type='float', action='store',
#                  default='13.0', 
#                  dest='minInstLumi',
#                  help='minInstLumi range to consider in runls maps')

#parser.add_option('--maxInstLumi', metavar='P', type='float', action='store',
#                  default='15.0', 
#                  dest='maxInstLumi',
#                  help='maxInstLumi range to consider in runls maps')

#parser.add_option('--inputNTupleFile', metavar='P', type='string', action='store',
#                  default='Efficiency_317650_0.root', 
#                  dest='inputNTupleFile',
#                  help='input ntuple file')

parser.add_option('--inputNTupleFiles', metavar='P', type='string', action='store',
                  default='run_MC.txt', #run_317650_0.txt run_MC.txt
                  dest='inputNTupleFiles',
                  help='input ntuple files')

parser.add_option('--outFile', metavar='P', type='string', action='store',
                  default='out_MC.root', #out_317650_0.root out_MC.root
                  dest='outFile',
                  help='output file')

(options,args) = parser.parse_args()
# ==========end: options =============
verbose     = options.verbose
plotdir     = options.plotDir
minRun      = options.minRun
maxRun      = options.maxRun
#minInstLumi = options.minInstLumi
#maxInstLumi = options.maxInstLumi
#inFile      = options.inputRunLumiInfo
inNtuple    = options.inputNTupleFiles
outFile     = options.outFile
isMC        = options.isMC

inChain = TChain("trajTree")
countRoot = 0
for line in open(inNtuple, 'r'):
    countRoot = countRoot+1
    inChain.Add(line.strip())

print 'number of root files', countRoot

#f = TFile.Open(inNtuple)
#t = f.Get("trajTree")
#t = inChain.GetTree()
#print 'tree', t, ', size', t.GetEntries()


timer = TStopwatch()
timer.Start()

if isMC: print "Caution: You are running on MC, hence no data lumi map is required"
else: lMaps = np.load('lumiMap_'+str(maxRun)+'.npy')
    
#for i, row in enumerate(lMaps):
#    print(row[0], row[1], row[2], row[3])

group_ch1D     = ['chL1', 'chL2', 'chL3', 'chL4', 'chD1', 'chD2', 'chD3']
group_sizeX1D  = ['sXL1', 'sXL2', 'sXL3', 'sXL4', 'sXD1', 'sXD2', 'sXD3']
group_sizeY1D  = ['sYL1', 'sYL2', 'sYL3', 'sYL4', 'sYD1', 'sYD2', 'sYD3']
group_all1D    =  group_ch1D + group_sizeX1D + group_sizeY1D  

histo1D = {}
for subdet in group_all1D:
    if 'ch' in subdet: histo1D[subdet] = TH1F(subdet, subdet, 60, 0.0, 120.0)
    if 'X'  in subdet: histo1D[subdet] = TH1F(subdet, subdet, 20, 0.5, 20.5)
    if 'Y'  in subdet: histo1D[subdet] = TH1F(subdet, subdet, 20, 0.5, 20.5)

# declare maps of 2D histograms
group_int_ch_temp    = ['chL1VsIntlumi', 'chL2VsIntlumi', 'chL3VsIntlumi', 'chL4VsIntlumi', 'chD1VsIntlumi', 'chD2VsIntlumi', 'chD3VsIntlumi']
group_int_sizeX_temp = ['sXL1VsIntlumi', 'sXL2VsIntlumi', 'sXL3VsIntlumi', 'sXL4VsIntlumi', 'sXD1VsIntlumi', 'sXD2VsIntlumi', 'sXD3VsIntlumi']
group_int_sizeY_temp = ['sYL1VsIntlumi', 'sYL2VsIntlumi', 'sYL3VsIntlumi', 'sYL4VsIntlumi', 'sYD1VsIntlumi', 'sYD2VsIntlumi', 'sYD3VsIntlumi']

group_int_ch = []; group_int_sizeX = []; group_int_sizeY = [];
inst_group = ['Int6to8', 'Int8to10', 'Int11to13', 'Int13to15']

for i in range(len(group_int_ch_temp)):
    for lumiR in inst_group:
        group_int_ch.append( group_int_ch_temp[i].replace('Int', lumiR))
        group_int_sizeX.append( group_int_sizeX_temp[i].replace('Int', lumiR))
        group_int_sizeY.append( group_int_sizeY_temp[i].replace('Int', lumiR))
        
group_ins_ch    = ['chL1VsInslumi', 'chL2VsInslumi', 'chL3VsInslumi', 'chL4VsInslumi', 'chD1VsInslumi', 'chD2VsInslumi', 'chD3VsInslumi']
group_ins_sizeX = ['sXL1VsInslumi', 'sXL2VsInslumi', 'sXL3VsInslumi', 'sXL4VsInslumi', 'sXD1VsInslumi', 'sXD2VsInslumi', 'sXD3VsInslumi']
group_ins_sizeY = ['sYL1VsInslumi', 'sYL2VsInslumi', 'sYL3VsInslumi', 'sYL4VsInslumi', 'sYD1VsInslumi', 'sYD2VsInslumi', 'sYD3VsInslumi']

group_pu_ch    = ['chL1VsPileup', 'chL2VsPileup', 'chL3VsPileup', 'chL4VsPileup', 'chD1VsPileup', 'chD2VsPileup', 'chD3VsPileup']
group_pu_sizeX = ['sXL1VsPileup', 'sXL2VsPileup', 'sXL3VsPileup', 'sXL4VsPileup', 'sXD1VsPileup', 'sXD2VsPileup', 'sXD3VsPileup']
group_pu_sizeY = ['sYL1VsPileup', 'sYL2VsPileup', 'sYL3VsPileup', 'sYL4VsPileup', 'sYD1VsPileup', 'sYD2VsPileup', 'sYD3VsPileup']

group_all   = group_pu_ch + group_pu_sizeX + group_pu_sizeY + group_ins_ch + group_ins_sizeX + group_ins_sizeY + group_int_ch + group_int_sizeX + group_int_sizeY


histo = {}
for subdet in group_all:
    if 'ch' in subdet and 'Int' in subdet: histo[subdet] = TH2F(subdet, subdet, 68, 0.0, 68.0, 60, 0.0, 120.0)
    if 'X'  in subdet and 'Int' in subdet: histo[subdet] = TH2F(subdet, subdet, 68, 0.0, 68.0, 20, 0.5, 20.5)
    if 'Y'  in subdet and 'Int' in subdet: histo[subdet] = TH2F(subdet, subdet, 68, 0.0, 68.0, 20, 0.5, 20.5)
    if 'ch' in subdet and 'Ins' in subdet: histo[subdet] = TH2F(subdet, subdet, 35, 0.0, 35.0, 60, 0.0, 120.0)
    if 'X'  in subdet and 'Ins' in subdet: histo[subdet] = TH2F(subdet, subdet, 35, 0.0, 35.0, 20, 0.5, 20.5)
    if 'Y'  in subdet and 'Ins' in subdet: histo[subdet] = TH2F(subdet, subdet, 35, 0.0, 35.0, 20, 0.5, 20.5)    
    if 'ch' in subdet and 'Pileup' in subdet: histo[subdet] = TH2F(subdet, subdet, 40, 20.0, 60.0, 60, 0.0, 120.0)
    if 'X'  in subdet and 'Pileup' in subdet: histo[subdet] = TH2F(subdet, subdet, 40, 20.0, 60.0, 20, 0.5, 20.5)
    if 'Y'  in subdet and 'Pileup' in subdet: histo[subdet] = TH2F(subdet, subdet, 40, 20.0, 60.0, 20, 0.5, 20.5)
#print histo

# run over ntuple branch/leaves
nEventsAnalyzed = 0
tSize = inChain.GetEntriesFast() #inChain.GetEntries()

#print 'size of EntriesFast', tSize
print 'size of Entries', inChain.GetEntries()
#for ich in xrange(tSize):
for iev in xrange(inChain.GetEntries()):   
    #iev = inChain.LoadTree(ich)   
    if (iev % 10000) == 0 : print 'event: ', iev
    
    # sample every 10th entry if the size of tree has more than 100k entries to manage the time
    if isMC==False:
        if (iev % 10) != 0: continue
    nEventsAnalyzed = nEventsAnalyzed + 1

    #t = inChain.GetTree()
    inChain.GetEntry(iev)
    #t.GetEntry(iev)
    
    run = getattr(inChain, 'event/run')
    ls  = getattr(inChain, 'event/ls')
    event = getattr(inChain, 'event/evt')
    pileup = getattr(inChain, 'event/pileup')
    runls = float(run) * 100000 + float(ls)
    #print runls
    # cuts and variables   
    barrel         = getattr(inChain, 'mod_on/det') == 0
    endcap         = getattr(inChain, 'mod_on/det') == 1
    layer1         = (getattr(inChain, 'mod_on/layer') == 1) and barrel
    layer2         = (getattr(inChain, 'mod_on/layer') == 2) and barrel
    layer3         = (getattr(inChain, 'mod_on/layer') == 3) and barrel
    layer4         = (getattr(inChain, 'mod_on/layer') == 4) and barrel
    disk1          = (getattr(inChain, 'mod_on/disk') == 1) and endcap
    disk2          = (getattr(inChain, 'mod_on/disk') == 2) and endcap
    disk3          = (getattr(inChain, 'mod_on/disk') == 3) and endcap    
    normCharge     = getattr(inChain, 'traj/norm_charge')
    normSizeX      = getattr(inChain, 'clust/sizeX')
    normSizeY      = getattr(inChain, 'clust/sizeY')
    normChargeCuts = normCharge > 0 and normCharge < 120    
    normSizeXCuts  = normSizeX > 0.
    normSizeYCuts  = normSizeY > 0.

    # Fill the 1D histograms, and 2D histograms for pileup in case running on MC

    if layer1:
        fillHistos1D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL1', 'sXL1', 'sYL1', normCharge, normSizeX, normSizeY)
        if isMC: fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL1VsPileup', 'sXL1VsPileup', 'sYL1VsPileup', pileup, normCharge, normSizeX, normSizeY)
    if layer2:
        fillHistos1D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL2', 'sXL2', 'sYL2', normCharge, normSizeX, normSizeY)
        if isMC: fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL2VsPileup', 'sXL2VsPileup', 'sYL2VsPileup', pileup, normCharge, normSizeX, normSizeY)
    if layer3:
        fillHistos1D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL3', 'sXL3', 'sYL3', normCharge, normSizeX, normSizeY)
        if isMC: fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL3VsPileup', 'sXL3VsPileup', 'sYL3VsPileup', pileup, normCharge, normSizeX, normSizeY)
    if layer4:
        fillHistos1D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL4', 'sXL4', 'sYL4', normCharge, normSizeX, normSizeY)
        if isMC: fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL4VsPileup', 'sXL4VsPileup', 'sYL4VsPileup', pileup, normCharge, normSizeX, normSizeY)
    if disk1:
        fillHistos1D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD1', 'sXD1', 'sYD1', normCharge, normSizeX, normSizeY)
        if isMC: fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD1VsPileup', 'sXD1VsPileup', 'sYD1VsPileup', pileup, normCharge, normSizeX, normSizeY)
    if disk2:
        fillHistos1D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD2', 'sXD2', 'sYD2', normCharge, normSizeX, normSizeY)
        if isMC: fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD2VsPileup', 'sXD2VsPileup', 'sYD2VsPileup', pileup, normCharge, normSizeX, normSizeY)
    if disk3:
        fillHistos1D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD3', 'sXD3', 'sYD3', normCharge, normSizeX, normSizeY)
        if isMC: fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD3VsPileup', 'sXD3VsPileup', 'sYD3VsPileup', pileup, normCharge, normSizeX, normSizeY)
        
    if isMC==False:
        for i, row in enumerate(lMaps):       
            runls_m   = row[0]
            inslumi_m = row[1]
            intlumi_m = row[2]
            pu_m      = row[3]       
            run_m     = int(str(row[0])[0:6])
        
            if run_m < minRun or run_m > maxRun : continue
        
            if runls == runls_m:
                if layer1:
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL1VsInslumi', 'sXL1VsInslumi', 'sYL1VsInslumi', inslumi_m, normCharge, normSizeX, normSizeY)
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL1VsPileup', 'sXL1VsPileup', 'sYL1VsPileup', pu_m, normCharge, normSizeX, normSizeY)
                if layer2:
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL2VsInslumi', 'sXL2VsInslumi', 'sYL2VsInslumi', inslumi_m, normCharge, normSizeX, normSizeY)
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL2VsPileup', 'sXL2VsPileup', 'sYL2VsPileup', pu_m, normCharge, normSizeX, normSizeY)
                if layer3:
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL3VsInslumi', 'sXL3VsInslumi', 'sYL3VsInslumi', inslumi_m, normCharge, normSizeX, normSizeY)
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL3VsPileup', 'sXL3VsPileup', 'sYL3VsPileup', pu_m, normCharge, normSizeX, normSizeY)
                if layer4:
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL4VsInslumi', 'sXL4VsInslumi', 'sYL4VsInslumi', inslumi_m, normCharge, normSizeX, normSizeY)
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chL4VsPileup', 'sXL4VsPileup', 'sYL4VsPileup', pu_m, normCharge, normSizeX, normSizeY)
                if disk1:
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD1VsInslumi', 'sXD1VsInslumi', 'sYD1VsInslumi', inslumi_m, normCharge, normSizeX, normSizeY)
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD1VsPileup', 'sXD1VsPileup', 'sYD1VsPileup', pu_m, normCharge, normSizeX, normSizeY)
                if disk2:
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD2VsInslumi', 'sXD2VsInslumi', 'sYD2VsInslumi', inslumi_m, normCharge, normSizeX, normSizeY)
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD2VsPileup', 'sXD2VsPileup', 'sYD2VsPileup', pu_m, normCharge, normSizeX, normSizeY)
                if disk3:
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD3VsInslumi', 'sXD3VsInslumi', 'sYD3VsInslumi', inslumi_m, normCharge, normSizeX, normSizeY)
                    fillHistos2D(normChargeCuts, normSizeXCuts, normSizeYCuts, 'chD3VsPileup', 'sXD3VsPileup', 'sYD3VsPileup', pu_m, normCharge, normSizeX, normSizeY)
                    
                for i in range(len(inst_group)):
                    minLumi = float(inst_group[i].replace('Int', '').split('to')[0])
                    maxLumi = float(inst_group[i].replace('Int', '').split('to')[1])
                    #print minLumi, maxLumi
                    if (inslumi_m >= minLumi and inslumi_m <= maxLumi):
                        if layer1:
                            #print 'runls : ', runls, 'inst lumi :', inslumi_m, 'int lumi :', intlumi_m, 'ch:',  normCharge
                            if normChargeCuts: histo['chL1Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normCharge)
                            if normSizeXCuts:  histo['sXL1Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeX)
                            if normSizeYCuts:  histo['sYL1Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeY)
                        if layer2:
                            if normChargeCuts: histo['chL2Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normCharge)
                            if normSizeXCuts:  histo['sXL2Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeX)
                            if normSizeYCuts:  histo['sYL2Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeY)
                        if layer3:
                            if normChargeCuts: histo['chL3Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normCharge)
                            if normSizeXCuts:  histo['sXL3Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeX)
                            if normSizeYCuts:  histo['sYL3Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeY)
                        if layer4:
                            if normChargeCuts: histo['chL4Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normCharge)
                            if normSizeXCuts:  histo['sXL4Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeX)
                            if normSizeYCuts:  histo['sYL4Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeY)
                        if disk1:
                            if normChargeCuts: histo['chD1Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normCharge)
                            if normSizeXCuts:  histo['sXD1Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeX)
                            if normSizeYCuts:  histo['sYD1Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeY)
                        if disk2:
                            if normChargeCuts: histo['chD2Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normCharge)
                            if normSizeXCuts:  histo['sXD2Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeX)
                            if normSizeYCuts:  histo['sYD2Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeY)
                        if disk3:
                            if normChargeCuts: histo['chD3Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normCharge)
                            if normSizeXCuts:  histo['sXD3Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeX)
                            if normSizeYCuts:  histo['sYD3Vs'+inst_group[i]+'lumi'].Fill(intlumi_m, normSizeY)    


# Write the 2D plots to an output ROOT file
f_out       = TFile(outFile, "RECREATE")
if isMC==False:
    myDir6to8   = f_out.mkdir("inslumi6to8",   "inslumi6to8")
    myDir8to10  = f_out.mkdir("inslumi8to10",  "inslumi8to10")
    myDir11to13 = f_out.mkdir("inslumi11to13", "inslumi11to13")
    myDir13to15 = f_out.mkdir("inslumi13to15", "inslumi13to15")


for h in sorted(histo1D):
    f_out.cd()
    histo1D[h].Write()

    
   
for h in sorted(histo):
    
    if 'Pileup' in histo[h].GetName() :
        f_out.cd()
        histo[h].Write()
        
    if isMC==False:
        if 'Ins' in histo[h].GetName() :
            f_out.cd()
            histo[h].Write()
        if 'Int6to8' in histo[h].GetName() :
            myDir6to8.cd()
            histo[h].Write()
        if 'Int8to10' in histo[h].GetName() :
            myDir8to10.cd()
            histo[h].Write()     
        if 'Int11to13' in histo[h].GetName() :
            myDir11to13.cd()
            histo[h].Write()
        if 'Int13to15' in histo[h].GetName() :
            myDir13to15.cd()
            histo[h].Write()     
#f_out.Close()
#f_out.Write()
f_out.Close()
# Stop our timer
timer.Stop()

del histo1D
del histo

# Print out our timing information
rtime = timer.RealTime(); 
ctime = timer.CpuTime();
if verbose:
    print("Analyzed events: {0:6d}").format(nEventsAnalyzed)
    print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds").format(rtime,ctime)
    print("{0:4.2f} events / RealTime second .").format( nEventsAnalyzed/rtime)
    print("{0:4.2f} events / CpuTime second .").format( nEventsAnalyzed/ctime)
    print("---------------")    
