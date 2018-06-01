#!/usr/bin/env python
import os, sys, math, array, operator
from ROOT import gROOT, TFile, TF1, gStyle, gDirectory, TTree, TCanvas, TH1F, TH2F, TH1D, TProfile, TObjArray, TStopwatch, TGaxis, TLegend, TLatex
from ROOT import kBlack, kGreen, kOrange, kGreen, kRed, kBlue, kTeal, kPink, kViolet
from readLumi import readLumiInfo
gROOT.ProcessLine('.L ./fitting.C')
from ROOT import fitting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
TGaxis.SetMaxDigits(3)

def setLeg(histo, legText):
    leg.AddEntry(histo, legText, "pl")
    
def setHisto(histo, xTitle, yTitle, color, legText, D2):
    histo.GetXaxis().SetTitle( xTitle )
    histo.GetYaxis().SetTitle( yTitle )
    histo.GetXaxis().SetTitleOffset(1.2)
    histo.GetYaxis().SetTitleOffset(1.4)
    histo.SetLineWidth(2)
    if D2:
        histo.SetMarkerStyle(7)
        histo.SetMarkerSize(0.2)
        histo.SetMarkerColor(color)
    histo.SetLineColor(color)
    
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

parser.add_option('--inputRunLumiInfo', metavar='P', type='string', action='store',
                  default='run_ls_instlumi_pileup_2018.txt', 
                  dest='inputRunLumiInfo',
                  help='input text file obtained from brilcal')

parser.add_option('--minRun', metavar='P', type='int', action='store',
                  default='315242', 
                  dest='minRun',
                  help='minRun range to extract the info')

parser.add_option('--maxRun', metavar='P', type='int', action='store',
                  default='315259', 
                  dest='maxRun',
                  help='maxRun range to extract the info')

parser.add_option('--inputNTupleFile', metavar='P', type='string', action='store',
                  default='Ntuple_75.root', 
                  dest='inputNTupleFile',
                  help='input ntuple file')


(options,args) = parser.parse_args()
# ==========end: options =============
verbose = options.verbose
plotdir = options.plotDir
minRun  = options.minRun
maxRun  = options.maxRun
inFile  = options.inputRunLumiInfo
inNtuple= options.inputNTupleFile

f = TFile.Open(inNtuple)
t = f.Get("trajTree")

timer = TStopwatch()
timer.Start()

# produce map of runs, ls, inst. lumi or int. lumi, and PU
lMaps = readLumiInfo(minRun, maxRun, inFile)
#print lMaps.map_runls_instLumi_PU
#print lMaps.map_run_totLumi_instLumi_avePU
print ('loading the lumi and PU maps ...')

# declare maps of 2D histograms
group_ch    = ['chL1VsIntlumi', 'chL2VsIntlumi', 'chL3VsIntlumi', 'chL4VsIntlumi', 'chD1VsIntlumi', 'chD2VsIntlumi', 'chD3VsIntlumi']
group_sizeX = ['sXL1VsIntlumi', 'sXL2VsIntlumi', 'sXL3VsIntlumi', 'sXL4VsIntlumi', 'sXD1VsIntlumi', 'sXD2VsIntlumi', 'sXD3VsIntlumi']
group_all   = group_ch #+ group_sizeX 

histo = {}
for det_ch in group_all:
    histo[det_ch] = TH2F(det_ch, det_ch, 50, 0.0, 50.0, 70, 0.0, 120.)
#histo_sort = sorted(histo.items(), key=operator.itemgetter(0))


# run over ntuple branch/leaves    
nEventsAnalyzed = 0  
for iev in xrange(t.GetEntries()):
    nEventsAnalyzed = nEventsAnalyzed + 1
    if iev % 100000 == 0: print 'event: ', iev
    #if iev == 10000: break 
    t.GetEntry(iev)
    run = getattr(t, 'event/run')
    ls  = getattr(t, 'event/ls')
    runls = float(run) * 100000 + float(ls)
    # cuts   
    barrel =  getattr(t, 'mod_on/det') == 0
    endcap =  getattr(t, 'mod_on/det') == 1
    layer1 =  (getattr(t, 'mod_on/layer') == 1) and barrel
    layer2 =  (getattr(t, 'mod_on/layer') == 2) and barrel
    layer3 =  (getattr(t, 'mod_on/layer') == 3) and barrel
    layer4 =  (getattr(t, 'mod_on/layer') == 4) and barrel
    disk1  =  (getattr(t, 'mod_on/disk') == 1) and endcap
    disk2  =  (getattr(t, 'mod_on/disk') == 2) and endcap
    disk3  =  (getattr(t, 'mod_on/disk') == 3) and endcap
    normCharge = getattr(t, 'traj/norm_charge')
    normChargeCuts = normCharge > 0 and normCharge < 120
    
   
    # inst lumi map: incredibly combersome :TANJA DO YOU HAVE A BETTER IDEA?
    '''
    for runls_m, inslumi_m, pu_m in map_runls_instLumi_PU:
        run_m = int(str(runls_m)[0:6])
        if run_m < 315242 or run_m > 315259: continue
        if runls  == runls_m:
            #print 'runls: ', runls_m, ' runs: ', runs_m, ' inslumi: ', inslumi_m, ' pu: ', pu_m
            if normChargeCuts:
                #print 'lumi : ', inslumi_m, ' ch : ', normCharge
                histo['chVsInslumi'].Fill(inslumi_m, normCharge)
    '''
    
    # integrated lumi map
    for run_m, intlumi_m, inslumi_m, pu_m in lMaps.map_run_totLumi_instLumi_avePU:
        if run_m < minRun or run_m > maxRun: continue
        if run == run_m:
            if layer1: 
                if normChargeCuts: histo['chL1VsIntlumi'].Fill(intlumi_m/1000., normCharge)
            if layer2:
                if normChargeCuts: histo['chL2VsIntlumi'].Fill(intlumi_m/1000., normCharge)
            if layer3:
                if normChargeCuts: histo['chL3VsIntlumi'].Fill(intlumi_m/1000., normCharge)
            if layer4:
                if normChargeCuts: histo['chL4VsIntlumi'].Fill(intlumi_m/1000., normCharge)
            if disk1:
                if normChargeCuts: histo['chD1VsIntlumi'].Fill(intlumi_m/1000., normCharge)
            if disk2:
                if normChargeCuts: histo['chD2VsIntlumi'].Fill(intlumi_m/1000., normCharge)
            if disk3:
                if normChargeCuts: histo['chD3VsIntlumi'].Fill(intlumi_m/1000., normCharge)         


leg = TLegend(0.70,0.88,0.85,0.55)
leg.SetBorderSize(0)
leg.SetFillColor(10)
leg.SetLineColor(10)
leg.SetLineWidth(0)
                

h_1D = []
h_2D = []
h_fit = []
chMaxYRange = 0
intLMaxXRange = 0
aveChMax = 0
for h in histo:
    n =  histo[h].GetName()  
    hist2D = histo[h].Clone()
    histY = hist2D.ProjectionY()
    histY.SetName(n+"_projY")
    if 'chL1' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (pb^{-1})", "Norm. on-trk. charge (ke)", kBlack, "L1", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", kBlack, "L1", 0)
        setLeg(histY, "Layer 1")
        
    if 'chL2' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (pb^{-1})", "Norm. on-trk. charge (ke)", kBlue, "L2", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", kBlue, "L2", 0)
        setLeg(histY, "Layer 2")
        
    if 'chL3' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (pb^{-1})", "Norm. on-trk. charge (ke)", kGreen, "L3", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", kGreen, "L3", 0)
        setLeg(histY, "Layer 3")
        
    if 'chL4' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (pb^{-1})", "Norm. on-trk. charge (ke)", kOrange, "L4", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", kOrange, "L4", 0)
        setLeg(histY, "Layer 4")
        
    if 'chD1' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (pb^{-1})", "Norm. on-trk. charge (ke)", kTeal, "D1", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", kTeal, "D1", 0)
        setLeg(histY, "Disk 1")
        
    if 'chD2' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (pb^{-1})", "Norm. on-trk. charge (ke)", kPink, "D2", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", kPink, "D2", 0)
        setLeg(histY, "Disk 2")
        
    if 'chD3' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (pb^{-1})", "Norm. on-trk. charge (ke)", kViolet, "D3", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", kViolet, "D3", 0)
        setLeg(histY, "Disk 3")
        
    if 'ch' in n:
        if histY.GetMaximum() > chMaxYRange: chMaxYRange = histY.GetMaximum()
        if histY.GetMean() > aveChMax: aveChMax = histY.GetMean()
        
    # note the order is very important here, as later we will map h_2D and h_fit for FitSliceY,
    # where h_fit will be the TH1 with which we will fit each slice of the h_2D in Y-direction
    
    h_1D.append(histY)
    h_2D.append(hist2D)
    h_fit.append(fitting(histY))
 
###################
#                 #
#     Plots:      #
#                 #
###################

# ----------------------------------------------
# Plot MP of charge vs intergrated Lumi.
# https://www.slac.stanford.edu/BFROOT/www/doc/tutorials/PhysicsWeekApril2000/RootTutorial-Histograms-intro.html
# ----------------------------------------------
c_ch_MP_intL = TCanvas('c_ch_MP_intL', 'c_ch_MP_intL', 800, 640)
for h in range(len(h_2D)):
    n =  h_2D[h].GetName()
    #print h_fit[h].GetParameter('MP')
    aSlices = TObjArray()
    fitS = h_2D[h].FitSlicesY(h_fit[h], 0, 120, 0, "QNR", aSlices)
    aSlices[1].GetYaxis().SetRangeUser(0., 30.)
    if 'chL1' in n: setHisto(aSlices[1], "Integrated Luminosity - 2018 (pb^{-1})", "MP Norm. on-trk. charge (ke)", kBlack, "L1", 1)
    if 'chL2' in n: setHisto(aSlices[1], "Integrated Luminosity - 2018 (pb^{-1})", "MP Norm. on-trk. charge (ke)", kBlue, "L2", 1)
    if 'chL3' in n: setHisto(aSlices[1], "Integrated Luminosity - 2018 (pb^{-1})", "MP Norm. on-trk. charge (ke)", kGreen, "L3", 1)
    if 'chL4' in n: setHisto(aSlices[1], "Integrated Luminosity - 2018 (pb^{-1})", "MP Norm. on-trk. charge (ke)", kOrange, "L4", 1)
    if 'chD1' in n: setHisto(aSlices[1], "Integrated Luminosity - 2018 (pb^{-1})", "MP Norm. on-trk. charge (ke)", kTeal, "D1", 1)
    if 'chD2' in n: setHisto(aSlices[1], "Integrated Luminosity - 2018 (pb^{-1})", "MP Norm. on-trk. charge (ke)", kPink, "D2", 1)
    if 'chD3' in n: setHisto(aSlices[1], "Integrated Luminosity - 2018 (pb^{-1})", "MP Norm. on-trk. charge (ke)", kViolet, "D3", 1)
    aSlices[1].Draw("same")
leg.Draw()
c_ch_MP_intL.SaveAs("fitChargeLumiPlot.pdf")

# ----------------------------------------------
# Plot Ave value of charge vs intergrated Lumi.
# ----------------------------------------------
c_ch_intL = TCanvas('c_ch_intL', 'c_ch_intL', 800, 640)

for h in range(len(h_2D)):
    h1 =  h_2D[h].ProfileX()
    h1.GetYaxis().SetTitle("Ave Norm. on-trk. charge (ke)")
    h1.GetYaxis().SetRangeUser(0., 30.)
    h1.Draw("same")       
leg.Draw()
c_ch_intL.SaveAs("AveChargeLumiPlot.pdf")

# ----------------------------------------------
# Plot charge profile overlayed by the fitted curve.
# ----------------------------------------------
c_ch = TCanvas('c_ch', 'c_ch', 800, 640)
lb = TLatex()
for h in range(len(h_1D)):
    h_1D[h].SetMaximum(chMaxYRange*1.10)
    h_1D[h].SetMinimum(0.01)
    h_1D[h].Draw("same hist")
    h_fit[h].Draw("lsame")    
leg.Draw()
c_ch.SaveAs("fitChargePlot.pdf")

raw_input('wait a bit ...')
# Stop our timer
timer.Stop()
    
# Print out our timing information
rtime = timer.RealTime(); 
ctime = timer.CpuTime();
if verbose:
    print("Analyzed events: {0:6d}").format(nEventsAnalyzed)
    print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds").format(rtime,ctime)
    print("{0:4.2f} events / RealTime second .").format( nEventsAnalyzed/rtime)
    print("{0:4.2f} events / CpuTime second .").format( nEventsAnalyzed/ctime)
    print("---------------")    
