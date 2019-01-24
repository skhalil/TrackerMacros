#!/usr/bin/env python
import os, sys, math, array, operator
from ROOT import gROOT, TFile, TF1, gPad, gStyle, gDirectory, TTree, TCanvas, TH1F, TH2F, TH1D, TProfile, TObjArray, TStopwatch, TGaxis, TLegend, TLatex
from ROOT import kBlack, kGreen, kOrange, kGreen, kMagenta, kRed, kBlue, kTeal, kPink, kViolet, kCyan, kTRUE
#from readLumi import readLumiInfo
gROOT.ProcessLine('.L ./fitting.C')
#gROOT.SetBatch(True)
from ROOT import fitting
from tdrstyle import *
setTDRStyle()
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetLineWidth(2)
TGaxis.SetMaxDigits(3)

def setLeg(histo, legText, color):   
    if 'D' in histo.GetName():
        if 'ch' in histo.GetName(): 
            ld = legDCh.AddEntry(histo, legText, "")
            ld.SetTextColor(color)
        if 'sX' in  histo.GetName():
            ld = legDSx.AddEntry(histo, legText, "")
            ld.SetTextColor(color)
        if 'sY' in  histo.GetName():
            ld = legDSy.AddEntry(histo, legText, "")
            ld.SetTextColor(color)    
    elif 'L' in histo.GetName():
        if 'ch' in histo.GetName(): 
            ll = legLCh.AddEntry(histo, legText, "")
            ll.SetTextColor(color)
        if 'sX' in  histo.GetName():
            ll = legLSx.AddEntry(histo, legText, "")
            ll.SetTextColor(color)
        if 'sY' in  histo.GetName():
            ll = legLSy.AddEntry(histo, legText, "")
            ll.SetTextColor(color)    

def setColor(histo, color, marker):
    histo.SetLineColor(color)
    #histo.SetMarkerSize(0.5)
    #histo.SetMarkerStyle(marker)
    histo.SetMarkerColor(color)
    
def fix_frame(h, ymax, xmax):
    h_dummy = h.Clone()
    h_dummy.Reset()
    h_dummy.SetMaximum(ymax)
    h_dummy.GetXaxis().SetRangeUser(0., xmax)
    return h_dummy
    #h_dummy.Draw()

def setHisto(histo, xTitle, yTitle, D2):
    histo.GetXaxis().SetTitle( xTitle )
    histo.GetYaxis().SetTitle( yTitle )
    #histo.GetXaxis().SetTitleOffset(1.0)
    #histo.GetYaxis().SetTitleOffset(1.2)#1.2
    
    #histo.GetXaxis().SetTitleSize(0.05)
    #histo.GetYaxis().SetTitleSize(0.05)
    ##histo.GetXaxis().SetTickSize(0.02)
    histo.SetLineWidth(2)
    #if D2:
        #histo.SetMarkerStyle(7)
        #histo.SetMarkerSize(0.2)
        #histo.GetXaxis().SetNdivisions(510)
        #histo.GetYaxis().SetNdivisions(510)
        #histo.SetTickLength(0.06,"X")
        #histo.SetTickLength(0.05,"Y")
        
def drawLabels(sliceL):
    lc = TLatex()
    lc.SetNDC(kTRUE)
    lc.SetTextSize(0.040)
    
    lr = TLatex()
    lr.SetNDC(kTRUE)
    lr.SetTextSize(0.040)
    
    lw = TLatex()
    lw.SetNDC(kTRUE)
    lw.SetTextFont(62)
    lw.SetTextSize(0.050)
    
    lp = TLatex()
    lp.SetNDC(kTRUE)
    lp.SetTextFont(52)
    lp.SetTextSize(0.050)

    le = TLatex()
    le.SetNDC(kTRUE)
    #lw.SetTextFont(62)
    le.SetTextSize(0.050)
    
    if sliceL: lc.DrawLatex(0.40, 0.845, '#bf{#scale[0.90]{L_{inst.}#subset ['+lumiRange+'] nb^{-1}s^{-1}}}')
   
    #lr.DrawLatex(0.40, 0.80, '#bf{Run '+RUN+'}')
    lw.DrawLatex(0.12, 0.95, 'CMS')
    le.DrawLatex(0.67, 0.95, '#bf{#sqrt{s} = 13 TeV}')
    lp.DrawLatex(0.24, 0.95, 'Preliminary 2018')

def setLabels(h, f, list_c):
    if 'ch' in h.GetName():
        MP = round(f.GetParameter('MP'),1)
        MPe = round(f.GetParError(1), 1)
    else:
        MP = round(h.GetMean(), 1)
       
    if 'D1' in h.GetName():
        if 'ch' in h.GetName(): setLeg(h, "MPV "+str(MP), list_c[0])
        else:                   setLeg(h, "Mean "+str(MP), list_c[0])
        lb.DrawLatex(0.40, 0.795, "#bf{#scale[0.90]{#color[633]{#topbar Disk 1}}}")
        
    if 'D2' in h.GetName():
        if 'ch' in h.GetName(): setLeg(h, "MPV "+str(MP), list_c[1])
        else:                   setLeg(h, "Mean "+str(MP), list_c[1])
        lb.DrawLatex(0.40, 0.755, "#bf{#scale[0.90]{#color[618]{#topbar Disk 2}}}")
        
    if 'D3' in h.GetName():
        if 'ch' in h.GetName(): setLeg(h, "MPV "+str(MP), list_c[2])
        else:                   setLeg(h, "Mean "+str(MP), list_c[2])
        lb.DrawLatex(0.40, 0.715, "#bf{#scale[0.90]{#color[601]{#topbar Disk 3}}}")
        
    if 'L1' in h.GetName():
        if 'ch' in h.GetName(): setLeg(h, "MPV "+str(MP), list_c[3])
        else:                   setLeg(h, "Mean "+str(MP), list_c[3])
        lb.DrawLatex(0.40, 0.795, "#bf{#scale[0.90]{#color[633]{#topbar Layer 1}}}")
        
    if 'L2' in h.GetName():
        if 'ch' in h.GetName(): setLeg(h, "MPV "+str(MP), list_c[4])
        else:                   setLeg(h, "Mean "+str(MP), list_c[4])
        lb.DrawLatex(0.40, 0.755, "#bf{#scale[0.90]{#color[618]{#topbar Layer 2}}}")
        
    if 'L3' in h.GetName():
        if 'ch' in h.GetName(): setLeg(h, "MPV "+str(MP), list_c[5])
        else:                   setLeg(h, "Mean "+str(MP), list_c[5])
        lb.DrawLatex(0.40, 0.715, "#bf{#scale[0.90]{#color[601]{#topbar Layer 3}}}")
        
    if 'L4' in h.GetName():
        if 'ch' in h.GetName(): setLeg(h, "MPV "+str(MP), list_c[6])
        else:                   setLeg(h, "Mean "+str(MP), list_c[6])
        lb.DrawLatex(0.40, 0.675, "#bf{#scale[0.90]{#color[433]{#topbar Layer 4}}}")
        
           
def gPadSet():
    #gPad.SetTickx(1)
    #gPad.SetTicky(1)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(1.4)
    #gPad.SetBottomMargin(0.10)
    gPad.SetFrameLineWidth(2)
    gPad.RedrawAxis()
    #gPad.Update()
# ==========
# options
# ===============
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Plots_RelVal/', 
                  dest='plotDir',
                  help='output directory of plots')
parser.add_option('--slicePerInstLumi', metavar='S', action='store_true',
                  default=False, 
                  dest='slicePerInstLumi',
                  help='output directory of plots')
parser.add_option('--lumiRange', metavar='I', type='string', action='store',
                  default='13-15',# 13-15 6-8
                  dest='lumiRange',
                  help='inst. lumi. range')
parser.add_option('--inFile', metavar='F', type='string', action='store',
                  default='ROOT/New/RelVal/out_RelVal_all.root',#'ROOT/intLumi13to15/History/out_all.root',#ROOT/out_317661.root',#ROOT/out_317626.root,317626, 317661, 
                  dest='inFile',
                  help='input file')

(options,args) = parser.parse_args()
# ==========end: options =============
plotdir     = options.plotDir
inFile      = options.inFile
sliceL      = options.slicePerInstLumi
lumiRange   = options.lumiRange
RUN         = inFile.split('_')[1].replace('.root', '')

f = TFile.Open(inFile)

group_ch1D     = ['chL1', 'chL2', 'chL3', 'chL4', 'chD1', 'chD2', 'chD3']
group_sizeX1D  = ['sXL1', 'sXL2', 'sXL3', 'sXL4', 'sXD1', 'sXD2', 'sXD3']
group_sizeY1D  = ['sYL1', 'sYL2', 'sYL3', 'sYL4', 'sYD1', 'sYD2', 'sYD3']
group_all1D    =  group_ch1D + group_sizeX1D + group_sizeY1D  

#print histo1D    
group_ch2D_int    = ['chL1VsIntlumi', 'chL2VsIntlumi', 'chL3VsIntlumi', 'chL4VsIntlumi', 'chD1VsIntlumi', 'chD2VsIntlumi', 'chD3VsIntlumi']               
group_sizeX2D_int = ['sXL1VsIntlumi', 'sXL2VsIntlumi', 'sXL3VsIntlumi', 'sXL4VsIntlumi', 'sXD1VsIntlumi', 'sXD2VsIntlumi', 'sXD3VsIntlumi']
group_sizeY2D_int = ['sYL1VsIntlumi', 'sYL2VsIntlumi', 'sYL3VsIntlumi', 'sYL4VsIntlumi', 'sYD1VsIntlumi', 'sYD2VsIntlumi', 'sYD3VsIntlumi']
group_all2D_int   = group_ch2D_int + group_sizeX2D_int + group_sizeY2D_int

histo2DInt = {}
for subdet in group_all2D_int:
    histo2DInt[subdet] = f.Get(subdet)

histo1D = {}
if sliceL:
    for h in sorted(histo2DInt):
        newN =  histo2DInt[h].GetName().replace('VsIntlumi', '')   
        hist2D = histo2DInt[h].Clone()
        histY = hist2D.ProjectionY()
        histY.SetName(newN)
        histo1D[newN] = hist2D.ProjectionY()
else:
    for subdet in group_all1D:
        histo1D[subdet] = f.Get(subdet)

legDCh = TLegend(0.70,0.88, 0.80, 0.70)#0.76,0.88,0.895,0.55
legDCh.SetTextSize(0.035)
legDCh.SetBorderSize(0)

legDSx = TLegend(0.70,0.88, 0.80, 0.70)
legDSx.SetTextSize(0.035)
legDSx.SetBorderSize(0)

legDSy = TLegend(0.70,0.88, 0.80, 0.70)
legDSy.SetTextSize(0.035)
legDSy.SetBorderSize(0)

legLCh = TLegend(0.70,0.88,0.82,0.70)
legLCh.SetTextSize(0.035)
legLCh.SetBorderSize(0)

legLSx = TLegend(0.70,0.88,0.82,0.70)
legLSx.SetTextSize(0.035)
legLSx.SetBorderSize(0)

legLSy = TLegend(0.70,0.88,0.82,0.70)
legLSy.SetTextSize(0.035)
legLSy.SetBorderSize(0)
#legL.SetFillColor(10)
#legL.SetLineColor(10)
#legL.SetLineWidth(0) 

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

# sort into different cluster property
for h in sorted(histo1D):
    n = histo1D[h].GetName()
    if sliceL: hist1D = histo1D[h].Clone()
    else:
        hist1F = histo1D[h].Clone()
        hist1D = TH1D()
        hist1F.Copy(hist1D)
    if 'ch' in n:
        setHisto(hist1D, "Norm. on-trk. clu. charge (ke)", "On-track Clusters / 1 ke", 0)
        h_fit.append(fitting(hist1D))
        h_1D_ch.append(hist1D)
        if hist1D.GetMaximum() > chMaxYRange: chMaxYRange = hist1D.GetMaximum()
    if 'X' in n:
        setHisto(hist1D, "On-track cluster size x (pixel)", "On-track Clusters / 1 pixel", 0)
        h_1D_sX.append(hist1D)
        if hist1D.GetMaximum() > sXMaxYRange: sXMaxYRange = hist1D.GetMaximum()
    if 'Y' in n:       
        setHisto(hist1D, "On-Track cluster size y (pixel)", "On-track Clusters / 1 pixel", 0)
        h_1D_sY.append(hist1D)       
        if hist1D.GetMaximum() > sYMaxYRange: sYMaxYRange = hist1D.GetMaximum()

       
     
lsColor   = [kRed+1, kMagenta+2, kBlue+1, kRed+1, kMagenta+2, kBlue+1, kCyan+1]
lsMarker  = [20, 21, 22, 24, 28, 29, 27 ]

h1DChColorMap = zip(h_1D_ch, lsColor, lsMarker)
h1DSXColorMap = zip(h_1D_sX, lsColor, lsMarker)
h1DSYColorMap = zip(h_1D_sY, lsColor, lsMarker)

for h, c, m in h1DChColorMap:
    setColor(h,c,m)
for h, c, m in h1DSXColorMap:
    setColor(h,c,m)
for h, c, m in h1DSYColorMap:
    setColor(h,c,m)


h1DChFitColorMap = zip(h_fit, lsColor, lsMarker)
for h, c, m in h1DChFitColorMap:
    setColor(h,c,m)

#lb = TLatex()
#lb.SetNDC(kTRUE)
#lb.SetTextSize(0.04)

#c = TCanvas('c', 'c')
#h_dummy = fix_frame(h_1D_ch[0], 0.18, 80.0)
#h_dummy.Draw()
#h_1D_ch[0].DrawNormalized("hist")

#fit_hist = h_fit[0].GetHistogram()
#fit_hist.Sumw2()
#fit_hist.Scale(1./h_1D_ch[0].GetEntries())
#fit_hist.Draw("l hist same")
#setLabels(h_1D_ch[0], h_fit[0], lsColor)
#raw_input("AAA")
#exit()
    
# ------------------    
lb = TLatex()
lb.SetNDC(kTRUE)
lb.SetTextSize(0.04)
# ----------------------------------------------
# Plot charge dist. overlayed by the fitted curve.
# ----------------------------------------------
c_ch_d = TCanvas('c_ch_d', 'c_ch_d')
#c_ch_d.SetGrid()
h_dummy = fix_frame(h_1D_ch[0], 0.18, 80.0)
h_dummy.Draw()
for i in range(0,3):#3
    #h_1D_ch[i].SetMinimum(0.01)
    #h_1D_ch[i].GetXaxis().SetRange(0, 70)
    #scale = h_1D_ch[i].Integral()/h_1D_ch[i].GetMaximum()
    fit_hist = h_fit[i].GetHistogram()
    fit_hist.Sumw2()
    fit_hist.Scale(1./h_1D_ch[i].GetEntries())
    fit_hist.SetMarkerSize(2)
    fit_hist.SetLineWidth(2)
    #h_1D_ch[h].SetMaximum(1.20)
    
    h_1D_ch[i].DrawNormalized("same hist")
    fit_hist.Draw("l hist same")
    setLabels(h_1D_ch[i], h_fit[i], lsColor)
    
       
drawLabels(sliceL)        
legDCh.Draw()
c_ch_d.RedrawAxis()
gPadSet()

if sliceL: c_ch_d.SaveAs(plotdir+"ch1D_InstLumi_disk_"+lumiRange.replace('-','to')+"_Run_"+RUN+".pdf") 
else: c_ch_d.SaveAs(plotdir+"ch1D_disk_Run_"+RUN+".pdf")

raw_input('press any key to continue ...')

c_ch_b = TCanvas('c_ch_b', 'c_ch_b')
h_dummy = fix_frame(h_1D_ch[3], 0.20, 100.0)
h_dummy.Draw()
for i in range(3,len(h_1D_ch)):
    fit_hist = h_fit[i].GetHistogram()
    fit_hist.Sumw2()
    fit_hist.Scale(1./h_1D_ch[i].GetEntries())
    fit_hist.SetMarkerSize(2)
    fit_hist.SetLineWidth(2)
    h_1D_ch[i].DrawNormalized("same hist")
    fit_hist.Draw("l hist same")
    setLabels(h_1D_ch[i], h_fit[i], lsColor)

drawLabels(sliceL)         
legLCh.Draw()
c_ch_b.RedrawAxis()
gPadSet()

if sliceL: c_ch_b.SaveAs(plotdir+"ch1D_InstLumi_barrel_"+lumiRange.replace('-','to')+"_Run_"+RUN+".pdf") 
else: c_ch_b.SaveAs(plotdir+"ch1D_barrel_Run_"+RUN+".pdf")

raw_input('press any key to continue ...')

# ----------------------------------------------
# Plot sizeX
# ----------------------------------------------
c_sX_d = TCanvas('c_sX_d', 'c_sX_d')
h_dummy = fix_frame(h_1D_sX[0], 0.8, 10.0)
h_dummy.Draw()
for h in range(0, 3):
    h_1D_sX[h].DrawNormalized("same hist")
    setLabels(h_1D_sX[h], h_fit[h], lsColor)
    
drawLabels(sliceL)     
legDSx.Draw()
c_sX_d.RedrawAxis()
gPadSet()

if sliceL: c_sX_d.SaveAs(plotdir+"sX1D_InstLumi_disk_"+lumiRange.replace('-','to')+"_Run_"+RUN+".pdf") 
else: c_sX_d.SaveAs(plotdir+"sX1D_disk_Run_"+RUN+".pdf")

raw_input('press any key to continue ...')

c_sX_b = TCanvas('c_sX_b', 'c_sX_b')
h_dummy = fix_frame(h_1D_sX[3], 0.9, 10.0)
h_dummy.Draw()
for h in range(3, len(h_1D_sX)):
    h_1D_sX[h].DrawNormalized("same hist")
    setLabels(h_1D_sX[h], h_fit[h], lsColor)
    
drawLabels(sliceL)      
legLSx.Draw()
c_sX_b.RedrawAxis()
gPadSet()

if sliceL: c_sX_b.SaveAs(plotdir+"sX1D_InstLumi_barrel_"+lumiRange.replace('-','to')+"_Run_"+RUN+".pdf") 
else: c_sX_b.SaveAs(plotdir+"sX1D_barrel_Run_"+RUN+".pdf")

raw_input('press any key to continue ...')

# ----------------------------------------------
# Plot sizeY
# ----------------------------------------------
c_sY_d = TCanvas('c_sY_d', 'c_sY_d')
h_dummy = fix_frame(h_1D_sY[0], 0.8, 10.0)
h_dummy.Draw()
for h in range(0, 3):
    h_1D_sY[h].DrawNormalized("same hist")
    setLabels(h_1D_sY[h], h_fit[h], lsColor)
    
drawLabels(sliceL)     
legDSy.Draw()
c_sY_d.RedrawAxis()
gPadSet()

if sliceL: c_sY_d.SaveAs(plotdir+"sY1D_InstLumi_disk_"+lumiRange.replace('-','to')+"_Run_"+RUN+".pdf") 
else: c_sY_d.SaveAs(plotdir+"sY1D_disk_Run_"+RUN+".pdf")

raw_input('press any key to continue ...')

c_sY_b = TCanvas('c_sY_b', 'c_sY_b')
h_dummy = fix_frame(h_1D_sY[3], 0.45, 20.0)
h_dummy.Draw()
for h in range(3, len(h_1D_sY)):
    #h_1D_sY[h].SetMaximum(sYMaxYRange*1.10)
    #h_1D_sY[h].GetXaxis().SetRange(0, 20)
    #h_1D_sY[h].SetMinimum(0.01)
    #scale = h_1D_sY[h].Integral()/h_1D_sY[h].GetMaximum()
    #h_1D_sY[h].Scale(1./ h_1D_sY[h].Integral()*scale)
    h_1D_sY[h].DrawNormalized("same hist")
    #h_1D_sY[h].SetMaximum(1.20)
    setLabels(h_1D_sY[h], h_fit[h], lsColor)
    
drawLabels(sliceL)
legLSy.Draw()
c_sY_b.RedrawAxis()
gPadSet()

if sliceL: c_sY_b.SaveAs(plotdir+"sY1D_InstLumi_barrel_"+lumiRange.replace('-','to')+"_Run_"+RUN+".pdf") 
else: c_sY_b.SaveAs(plotdir+"sY1D_barrel_Run_"+RUN+".pdf")

raw_input('press any key to continue ...')
