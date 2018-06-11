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
                  default='run_ls_instlumi_pileup_fill_6650_6759.txt', 
                  dest='inputRunLumiInfo',
                  help='input text file obtained from brilcal')

parser.add_option('--minRun', metavar='P', type='int', action='store',
                  default='316109', 
                  dest='minRun',
                  help='minRun range to loop over ntuple entries')

parser.add_option('--maxRun', metavar='P', type='int', action='store',
                  default='316109', 
                  dest='maxRun',
                  help='maxRun range to loop over ntuple entries')

parser.add_option('--minInstLumi', metavar='P', type='float', action='store',
                  default='3.0', 
                  dest='minInstLumi',
                  help='minInstLumi range to consider in runls maps')

parser.add_option('--maxInstLumi', metavar='P', type='float', action='store',
                  default='6.0', 
                  dest='maxInstLumi',
                  help='maxInstLumi range to consider in runls maps')

parser.add_option('--inputNTupleFile', metavar='P', type='string', action='store',
                  default='Efficiency_316109.root', 
                  dest='inputNTupleFile',
                  help='input ntuple file')


(options,args) = parser.parse_args()
# ==========end: options =============
verbose     = options.verbose
plotdir     = options.plotDir
minRun      = options.minRun
maxRun      = options.maxRun
minInstLumi = options.minInstLumi
maxInstLumi = options.maxInstLumi
inFile      = options.inputRunLumiInfo
inNtuple    = options.inputNTupleFile

f = TFile.Open(inNtuple)
t = f.Get("trajTree")

timer = TStopwatch()
timer.Start()

# produce map of runs, ls, inst. lumi or int. lumi, and PU
#lMaps = readLumiInfo(minRun, maxRun, minInstLumi, maxInstLumi, inFile)
lMaps = readLumiInfo(314090, 316994, minInstLumi, maxInstLumi, 'run_ls_instlumi_pileup_2018_1.txt')
#print lMaps.map_runls_instLumi_PU
#print lMaps.map_run_totLumi_instLumi_avePU
print ('loading the lumi and PU maps ...')

#exit()
# declare maps of 2D histograms
group_ch    = ['chL1VsIntlumi', 'chL2VsIntlumi', 'chL3VsIntlumi', 'chL4VsIntlumi', 'chD1VsIntlumi', 'chD2VsIntlumi', 'chD3VsIntlumi']
group_sizeX = ['sXL1VsIntlumi', 'sXL2VsIntlumi', 'sXL3VsIntlumi', 'sXL4VsIntlumi', 'sXD1VsIntlumi', 'sXD2VsIntlumi', 'sXD3VsIntlumi']
group_sizeY = ['sYL1VsIntlumi', 'sYL2VsIntlumi', 'sYL3VsIntlumi', 'sYL4VsIntlumi', 'sYD1VsIntlumi', 'sYD2VsIntlumi', 'sYD3VsIntlumi']
group_all   = group_ch + group_sizeX + group_sizeY 

histo = {}
for subdet in group_all:
    if 'ch' in subdet: histo[subdet] = TH2F(subdet, subdet, 20, 0.0, 20.0, 70, 0.0, 120.0)
    if 'X'  in subdet: histo[subdet] = TH2F(subdet, subdet, 20, 0.0, 20.0, 20, 0.5, 20.5)
    if 'Y'  in subdet: histo[subdet] = TH2F(subdet, subdet, 20, 0.0, 20.0, 20, 0.5, 20.5)

# run over ntuple branch/leaves    
nEventsAnalyzed = 0  
for iev in xrange(t.GetEntries()):
    nEventsAnalyzed = nEventsAnalyzed + 1
    if iev % 100000 == 0: print 'event: ', iev
    if iev == 10000: break 
    t.GetEntry(iev)
    run = getattr(t, 'event/run')
    ls  = getattr(t, 'event/ls')
    runls = float(run) * 100000 + float(ls)
    
    # cuts and variables   
    barrel         = getattr(t, 'mod_on/det') == 0
    endcap         = getattr(t, 'mod_on/det') == 1
    layer1         = (getattr(t, 'mod_on/layer') == 1) and barrel
    layer2         = (getattr(t, 'mod_on/layer') == 2) and barrel
    layer3         = (getattr(t, 'mod_on/layer') == 3) and barrel
    layer4         = (getattr(t, 'mod_on/layer') == 4) and barrel
    disk1          = (getattr(t, 'mod_on/disk') == 1) and endcap
    disk2          = (getattr(t, 'mod_on/disk') == 2) and endcap
    disk3          = (getattr(t, 'mod_on/disk') == 3) and endcap    
    normCharge     = getattr(t, 'traj/norm_charge')
    normSizeX      = getattr(t, 'clust/sizeX')
    normSizeY      = getattr(t, 'clust/sizeY')
    normChargeCuts = normCharge > 0 and normCharge < 120    
    normSizeXCuts  = normSizeX > 0.
    normSizeYCuts  = normSizeY > 0.
    
   
    # inst lumi map: incredibly combersome :TANJA DO YOU HAVE A BETTER IDEA?
    '''
    for runls_m, inslumi_m, pu_m in lMaps.map_runls_instLumi_PU:
        run_m = int(str(runls_m)[0:6])
        if run_m < minRun or run_m > maxRun: continue
        if runls  == runls_m:
            #print 'runls: ', runls_m, ' runs: ', runs_m, ' inslumi: ', inslumi_m, ' pu: ', pu_m
            if normChargeCuts:
                #print 'lumi : ', inslumi_m, ' ch : ', normCharge
                histo['chVsInslumi'].Fill(inslumi_m, normCharge)
    '''
    keepEntry = 0
    for runls_m, inslumi_m, pu_m in lMaps.map_runls_instLumi_PU:
        run_m = int(str(runls_m)[0:6])
        if run_m <  minRun  or run_m >  maxRun : continue
        #print 'runls : ', runls, 'runls in map : ', runls_m
        if runls  == runls_m:
            keepEntry = 1
            break
    if keepEntry == 0: continue    
   
    # integrated lumi map
    for run_m, intlumi_m, inslumi_m, pu_m in lMaps.map_run_totLumi_instLumi_avePU:
        if run_m < minRun or run_m > maxRun: continue
        if run == run_m:
            totlumi = intlumi_m/1000000. #(fb-1)
            if layer1: 
                if normChargeCuts: histo['chL1VsIntlumi'].Fill(totlumi, normCharge)
                if normSizeXCuts:  histo['sXL1VsIntlumi'].Fill(totlumi, normSizeX)
                if normSizeYCuts:  histo['sYL1VsIntlumi'].Fill(totlumi, normSizeY)
            if layer2:
                if normChargeCuts: histo['chL2VsIntlumi'].Fill(totlumi, normCharge)
                if normSizeXCuts:  histo['sXL2VsIntlumi'].Fill(totlumi, normSizeX)
                if normSizeYCuts:  histo['sYL2VsIntlumi'].Fill(totlumi, normSizeY)
            if layer3:
                if normChargeCuts: histo['chL3VsIntlumi'].Fill(totlumi, normCharge)
                if normSizeXCuts:  histo['sXL3VsIntlumi'].Fill(totlumi, normSizeX)
                if normSizeYCuts:  histo['sYL3VsIntlumi'].Fill(totlumi, normSizeY)
            if layer4:
                if normChargeCuts: histo['chL4VsIntlumi'].Fill(totlumi, normCharge)
                if normSizeXCuts:  histo['sXL4VsIntlumi'].Fill(totlumi, normSizeX)
                if normSizeYCuts:  histo['sYL4VsIntlumi'].Fill(totlumi, normSizeY)
            if disk1:
                if normChargeCuts: histo['chD1VsIntlumi'].Fill(totlumi, normCharge)
                if normSizeXCuts:  histo['sXD1VsIntlumi'].Fill(totlumi, normSizeX)
                if normSizeYCuts:  histo['sYD1VsIntlumi'].Fill(totlumi, normSizeY)
            if disk2:
                if normChargeCuts: histo['chD2VsIntlumi'].Fill(totlumi, normCharge)
                if normSizeXCuts:  histo['sXD2VsIntlumi'].Fill(totlumi, normSizeX)
                if normSizeYCuts:  histo['sYD2VsIntlumi'].Fill(totlumi, normSizeY)
            if disk3:
                if normChargeCuts: histo['chD3VsIntlumi'].Fill(totlumi, normCharge)
                if normSizeXCuts:  histo['sXD3VsIntlumi'].Fill(totlumi, normSizeX)
                if normSizeYCuts:  histo['sYD3VsIntlumi'].Fill(totlumi, normSizeY)
                
# Write the 2D plots to an output ROOT file
f_out = TFile("2DHistos_"+str(minRun)+"_"+str(maxRun)+".root", "RECREATE")
f_out.cd()
for h in sorted(histo):
    histo[h].Write()
f_out.Close()
'''
###################
#                 #
#     Plots:      #
#                 #
###################

leg = TLegend(0.70,0.88,0.85,0.55)
leg.SetBorderSize(0)
leg.SetFillColor(10)
leg.SetLineColor(10)
leg.SetLineWidth(0)                

h_1D_ch = []
h_2D_ch = []
h_fit = []
chMaxYRange = 0
h_1D_sX = []
h_2D_sX = []
sXMaxYRange = 0
h_1D_sY = []
h_2D_sY = []
sYMaxYRange = 0
    
for h in sorted(histo):
    n =  histo[h].GetName()
    #print n
    hist2D = histo[h].Clone()
    histY = hist2D.ProjectionY()
    histY.SetName(n+"_projY")
      
    #for subdet, color in colorMap.items():
    #    setColor(hist2D, color)
    #    setColor(histY, color)
        
    # store the charge related histograms        
    if 'ch' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (fb^{-1})", "Norm. on-trk. charge (ke)", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", 0)
        h_fit.append(fitting(histY))       
        # note the order is very important here, as later we will map h_2D_ch and h_fit for FitSliceY,
        # where h_fit will be the TH1 with which we will fit each slice of the h_2D_ch in Y-direction    
        h_1D_ch.append(histY)
        h_2D_ch.append(hist2D)
        if histY.GetMaximum() > chMaxYRange: chMaxYRange = histY.GetMaximum()

    # store the sizeX related histograms     
    if 'X' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (fb^{-1})", "On-Track cluster size in x-direction (pixel)", 1)
        setHisto(histY, "On-Track cluster size in x-direction (pixel)", "clusters", 0)
        h_1D_sX.append(histY)
        h_2D_sX.append(hist2D)
        if histY.GetMaximum() > sXMaxYRange: sXMaxYRange = histY.GetMaximum()

    # store the sizeY related histograms     
    if 'Y' in n:
        setHisto(hist2D, "Integrated Luminosity - 2018 (fb^{-1})", "On-Track cluster size in y-direction (pixel)", 1)
        setHisto(histY, "On-Track cluster size in y-direction (pixel)", "clusters", 0)
        h_1D_sY.append(histY)
        h_2D_sY.append(hist2D)
        if histY.GetMaximum() > sYMaxYRange: sYMaxYRange = histY.GetMaximum()    

lsColor   = [kBlack, kBlue, kGreen, kOrange, kTeal, kPink, kViolet]
lsMarker  = [20, 21, 22, 24, 28, 29, 27 ]

h1DChColorMap = zip(h_1D_ch, lsColor, lsMarker)
h2DChColorMap = zip(h_2D_ch, lsColor, lsMarker)
h1DSXColorMap = zip(h_1D_sX, lsColor, lsMarker)
h2DSXColorMap = zip(h_2D_sX, lsColor, lsMarker)
h1DSYColorMap = zip(h_1D_sY, lsColor, lsMarker)
h2DSYColorMap = zip(h_2D_sY, lsColor, lsMarker)

for h, c, m in h1DChColorMap:
    setColor(h,c,m)

for h, c, m  in h2DChColorMap:
    setColor(h,c,m)

for h, c, m in h1DSXColorMap:
    setColor(h,c,m)

for h, c, m in h2DSXColorMap:
    setColor(h,c,m)

for h, c, m in h1DSYColorMap:
    setColor(h,c,m)

for h, c, m in h2DSYColorMap:
    setColor(h,c,m)     

# ----------------------------------------------
# Plot MP of charge vs intergrated Lumi.
# https://www.slac.stanford.edu/BFROOT/www/doc/tutorials/PhysicsWeekApril2000/RootTutorial-Histograms-intro.html
# ----------------------------------------------
h_sliceY = []
c_ch_MP_intL = TCanvas('c_ch_MP_intL', 'c_ch_MP_intL', 800, 640)
c_ch_MP_intL.SetGrid()
for h in range(len(h_2D_ch)):
    n =  h_2D_ch[h].GetName()
    if 'ch' in n:
        print h_fit[h].GetParameter('MP')
        aSlices = TObjArray()
        fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 0, 120, 0, "QNR", aSlices)
        aSlices[1].GetYaxis().SetRangeUser(12., 30.)
        h_sliceY.append(aSlices[1])
        

hSliceYColorMap = zip(h_sliceY, lsColor, lsMarker)
for h, c, m in hSliceYColorMap:
    setColor(h, c, m)
    setHisto(h, "Integrated Luminosity - 2018 (fb^{-1})", "MP Norm. on-trk. charge (ke)", 1)
    h.Draw("same")
    if 'L1' in h.GetName(): setLeg (h, "Layer 1")
    if 'L2' in h.GetName(): setLeg (h, "Layer 2")
    if 'L3' in h.GetName(): setLeg (h, "Layer 3")
    if 'L4' in h.GetName(): setLeg (h, "Layer 4")
    if 'D1' in h.GetName(): setLeg (h, "Disk 1")
    if 'D2' in h.GetName(): setLeg (h, "Disk 2")
    if 'D3' in h.GetName(): setLeg (h, "Disk 3")

#print leg.Print()
leg.Draw()
c_ch_MP_intL.RedrawAxis()
c_ch_MP_intL.SaveAs("fitChargeLumiPlot.pdf")
#raw_input('wait a bit ...')
# ----------------------------------------------
# Plot Ave value of charge vs intergrated Lumi.
# ----------------------------------------------
c_ch_intL = TCanvas('c_ch_intL', 'c_ch_intL', 800, 640)
c_ch_intL.SetGrid()
for h in range(len(h_2D_ch)):
    h1 =  h_2D_ch[h].ProfileX()
    setHisto(h1, "Integrated Luminosity - 2018 (fb^{-1})", "Ave Norm. on-trk. charge (ke)", 1)
    h1.GetYaxis().SetRangeUser(12., 30.)
    h1.Draw("same")    
leg.Draw()
c_ch_intL.RedrawAxis()
c_ch_intL.SaveAs("AveChargeLumiPlot.pdf")
#raw_input('wait a bit ...')
# ----------------------------------------------
# Plot charge profile overlayed by the fitted curve.
# ----------------------------------------------
c_ch = TCanvas('c_ch', 'c_ch', 800, 640)
c_ch.SetGrid()
lb = TLatex()
#print chMaxYRange
for h in range(len(h_1D_ch)):
    h_1D_ch[h].SetMaximum(chMaxYRange*1.10)
    h_1D_ch[h].SetMinimum(0.01)
    h_1D_ch[h].Draw("same hist")
    h_fit[h].Draw("lsame")
leg.Draw()
c_ch.RedrawAxis()
c_ch.SaveAs("fitChargePlot.pdf")
# ----------------------------------------------
# Plot Ave value of clustSizeX vs intergrated Lumi.
# ----------------------------------------------
c_sX_intL = TCanvas('c_sX_intL', 'c_sX_intL', 800, 640)
c_sX_intL.SetGrid()
for h in range(len(h_2D_sX)):
    h1 =  h_2D_sX[h].ProfileX()
    setHisto(h1, "Integrated Luminosity - 2018 (fb^{-1})", "Ave Norm. on-trk. cluster size in x-direction", 1)
    h1.GetYaxis().SetRangeUser(0., 3.)
    h1.Draw("same")    
leg.Draw()
c_sX_intL.RedrawAxis()
c_sX_intL.SaveAs("AveClusterXLumiPlot.pdf")
#raw_input('wait a bit ...')
# ----------------------------------------------
# Plot clustSizeX profile.
# ----------------------------------------------
c_sX = TCanvas('c_sX', 'c_sX', 800, 640)
c_sX.SetGrid()    
for h in range(len(h_1D_sX)):
    h_1D_sX[h].SetMaximum(sXMaxYRange*1.10)
    h_1D_sX[h].SetMinimum(0.01)
    h_1D_sX[h].Draw("same hist")
leg.Draw()
c_sX.RedrawAxis()    
c_sX.SaveAs("fitClusterXPlot.pdf")
# ----------------------------------------------
# Plot Ave value of clustSizeY vs intergrated Lumi.
# ----------------------------------------------
c_sY_intL = TCanvas('c_sY_intL', 'c_sY_intL', 800, 640)
c_sY_intL.SetGrid()
for h in range(len(h_2D_sY)):
    h1 =  h_2D_sY[h].ProfileX()
    setHisto(h1, "Integrated Luminosity - 2018 (fb^{-1})", "Ave Norm. on-trk. cluster size in y-direction", 1)
    h1.GetYaxis().SetRangeUser(0., 3.)
    h1.Draw("same")    
leg.Draw()
c_sY_intL.RedrawAxis()
c_sY_intL.SaveAs("AveClusterYLumiPlot.pdf")
#raw_input('wait a bit ...')
# ----------------------------------------------
# Plot clustSizeX profile.
# ----------------------------------------------
c_sY = TCanvas('c_sY', 'c_sY', 800, 640)
c_sY.SetGrid()    
for h in range(len(h_1D_sX)):
    h_1D_sY[h].SetMaximum(sYMaxYRange*1.10)
    h_1D_sY[h].SetMinimum(0.01)
    h_1D_sY[h].Draw("same hist")
leg.Draw()
c_sY.RedrawAxis()    
c_sY.SaveAs("fitClusterYPlot.pdf")

#raw_input('wait a bit ...')
'''
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
