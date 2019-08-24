#!/usr/bin/env python
import os, sys, math, array, operator
from ROOT import gROOT, TFile, TF1, gPad, gStyle, gDirectory, TTree, TCanvas, TH1F, TH2F, TH1D, TProfile, TObjArray, TStopwatch, TGaxis, TLegend, TLatex, THStack, TLine, TBox
from ROOT import kBlack, kYellow, kGreen, kOrange, kGreen, kMagenta, kRed, kBlue, kTeal, kPink, kViolet, kCyan, kWhite, kTRUE
gROOT.ProcessLine('.L ./fitting.C')
#gROOT.SetBatch(True)
from ROOT import fitting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
#gStyle.SetLineWidth(2)
TGaxis.SetMaxDigits(3)

def setHistLeg(histo, legText): 
    if 'D' in histo.GetName(): legD.AddEntry(histo, legText, "pl")
    if 'L' in histo.GetName(): legL.AddEntry(histo, legText, "pl")
    
def setColor(histo, color, marker):
    histo.SetLineColor(color)  
    histo.SetMarkerStyle(marker)
    if 19 < marker < 25: histo.SetMarkerSize(0.6)
    histo.SetMarkerColor(color)
    
def setHisto(histo, xTitle, yTitle, D2):
    histo.GetXaxis().SetTitle( xTitle )
    histo.GetYaxis().SetTitle( yTitle )
    histo.GetXaxis().SetTitleOffset(0.9)
    histo.GetYaxis().SetTitleOffset(1.03)
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleSize(0.05)
    histo.GetXaxis().SetTickSize(0.02)
    histo.GetYaxis().SetTickSize(0.02)
    histo.SetLineWidth(2)
    if D2:
        #histo.SetMarkerStyle(7)
        histo.GetXaxis().SetNdivisions(510)
        histo.GetYaxis().SetNdivisions(510)
        histo.SetTickLength(0.02,"X")
        histo.SetTickLength(0.02,"Y")
        
def drawLabels(lumiType):

    lc = TLatex()
    lc.SetNDC(kTRUE)
    #lc.SetTextBox(0)
    lc.SetTextSize(0.040)
    
    lf = TLatex()
    lf.SetNDC(kTRUE)
    lf.SetTextSize(0.040)
    
    lw = TLatex()
    lw.SetNDC(kTRUE)
    lw.SetTextFont(62)
    lw.SetTextSize(0.05)
    
    lp = TLatex()
    lp.SetNDC(kTRUE)
    lp.SetTextFont(52)
    lp.SetTextSize(0.05)

    le = TLatex()
    le.SetNDC(kTRUE)
    le.SetTextSize(0.05)

    if lumiType == 'int': lc.DrawLatex(0.36, 0.80, '#bf{#scale[0.90]{L_{inst.}#subset ['+lumiRange+'] nb^{-1}s^{-1}}}')
    #elif lumiType == 'ins': lf.DrawLatex(0.36, 0.80, 'Fill: '+ fill)

    lw.DrawLatex(0.12, 0.91, 'CMS')
    le.DrawLatex(0.66, 0.91, '#bf{#sqrt{s} = 13 TeV}')
    lp.DrawLatex(0.24, 0.91, 'Preliminary 2018')#Internal 2018')
    
    
def gPadSet():
    gPad.SetTickx(1)
    gPad.SetTicky(1)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(1.4)
    gPad.SetBottomMargin(0.10)
    gPad.SetFrameLineWidth(2)
    gPad.RedrawAxis()
    #gPad.Update()

def setLine(line, X1, Y1, X2, Y2, color, lineStyle, lineWidth):
    line.SetX1(X1)
    line.SetY1(Y1)
    line.SetX2(X2)
    line.SetY2(Y2)    
    line.SetLineColor(color)
    line.SetLineStyle(lineStyle)
    line.SetLineWidth(lineWidth)

def setLineLeg(legLine, fillColor, lineColor, textSize, textAlign, boarderSize, lineWidth):  
    legLine.SetTextSize(textSize)
    legLine.SetTextAlign(textAlign)
    legLine.SetBorderSize(boarderSize)
    legLine.SetFillColor(fillColor)
    legLine.SetLineColor(lineColor)
    legLine.SetLineWidth(lineWidth)
    #return legLine
    
def drawConditionLines (leg, barrel, yMin, yMax):
    
    setLine(line=line3,    X1=HV3Lumi, Y1=yMin, X2=HV3Lumi, Y2=yMax, color=kRed,     lineStyle=7, lineWidth=3) 
    setLine(line=linepiG1, X1=PiGain1, Y1=yMin, X2=PiGain1, Y2=yMax, color=kGreen+2, lineStyle=2, lineWidth=2)
    setLine(line=linepiG2, X1=PiGain2, Y1=yMin, X2=PiGain2, Y2=yMax, color=kGreen+2, lineStyle=2, lineWidth=2)
    setLine(line=linepiG3, X1=PiGain3, Y1=yMin, X2=PiGain3, Y2=yMax, color=kGreen+2, lineStyle=2, lineWidth=2)
    setLine(line=linepiG4, X1=PiGain4, Y1=yMin, X2=PiGain4, Y2=yMax, color=kGreen+2, lineStyle=2, lineWidth=2)  
    setLine(line=linepiA,  X1=PiAneal, Y1=yMin, X2=PiAneal, Y2=yMax, color=kBlue,    lineStyle=2, lineWidth=2)

    line3.Draw()
    linepiA.Draw()
    linepiG1.Draw()
    linepiG2.Draw()
    linepiG3.Draw()
    linepiG4.Draw()

    #legCond = TLegend (0.62, 0.78, 0.80, 0.64)
    setLineLeg(legLine=leg, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)
    leg.Clear()

    if barrel == 1:
        leg.SetY1(0.60); leg.SetY2(0.80)
        setLine(line=line2,    X1=HV2Lumi, Y1=ymin, X2=HV2Lumi, Y2=ymax, color=kYellow,  lineStyle=7, lineWidth=3)
        line2.Draw()
        leg.AddEntry(line2, 'HV, Layer 2-4', "l")
        leg.AddEntry(line3, 'HV, Layer 1', "l")
    else:    
        leg.AddEntry(line3, 'HV, Ring 1', "l")
        
    leg.AddEntry(linepiA, 'Pixel Annealing', "l")
    leg.AddEntry(linepiG1, 'Pixel Gain', "l")    
    leg.Draw()
# ==========
# options
# ===============
def runs(option, opt, value, parser):
    setattr(parser.values, option.dest, value.splt(','))
            
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='PlotsApr/', 
                  dest='plotDir',
                  help='output directory of plots')
parser.add_option('--slicePerInstLumi', metavar='S', action='store_true',
                  default=True, 
                  dest='slicePerInstLumi',
                  help='output directory of plots')
parser.add_option('--sliceDir', metavar='F', type='string', action='store',
                  default='inslumi11to13', 
                  dest='sliceDir',
                  help='ins lumi subdir 6to8,  8to10, 11to13, 13to15')
parser.add_option('--reBin', metavar='P', type='string', action='store',
                  default='2', 
                  dest='reBin',
                  help='reBin value for 2D histos')
parser.add_option('--runList', metavar='l', type='string', action='callback', callback = runs,
                  default= '',
                  dest='runList',
                  help='run list')
parser.add_option('--lumiType', metavar='L', type='string', action='store',
                  default='int', #int #ins #PU
                  dest='lumiType',
                  help='plot cluster property as function of inst. lumi or integ. lumi')
parser.add_option('--inFile', metavar='F', type='string', action='store',
                  default='ROOT/New/out_all.root', #out_317696.root',
                  dest='inFile',
                  help='input file')
parser.add_option('--fill', metavar='F', type='string', action='store',
                  default='',
                  dest='fill',
                  help='fill number')

(options,args) = parser.parse_args()
# ==========end: options =============
plotdir     = options.plotDir
inFile      = options.inFile
sliceL      = options.slicePerInstLumi
lumiType    = options.lumiType
sliceDir    = options.sliceDir
runList     = options.runList.split(',')
fill        = options.fill
rebinSizeX = options.reBin

if sliceL==True :
    if   '13to15' in sliceDir: InsSlice='13to15lumi'; lumiRange='13-15';
    elif '11to13' in sliceDir: InsSlice='11to13lumi'; lumiRange='11-13';
    elif '8to10'  in sliceDir: InsSlice='8to10lumi';  lumiRange='8-10';
    elif '6to8'   in sliceDir: InsSlice='6to8lumi';   lumiRange='6-8';      
    else:                      InsSlice = 'lumi';     lumiRange='';
        
HV2Lumi = 23.6 #L2-L4
HV3Lumi = 55.2 #L1, D1
PiGain1 = 23.6
PiGain2 = 29.2
PiGain3 = 31.4 
PiGain4 = 55.2
PiAneal = 29.5
line2    = TLine()
line3    = TLine()
linepiG1 = TLine()
linepiG2 = TLine()
linepiG3 = TLine()
linepiG4 = TLine()
linepiA  = TLine()

f = TFile.Open(inFile)

group_ch1D     = ['chL1', 'chL2', 'chL3', 'chL4', 'chD1', 'chD2', 'chD3']
group_sizeX1D  = ['sXL1', 'sXL2', 'sXL3', 'sXL4', 'sXD1', 'sXD2', 'sXD3']
group_sizeY1D  = ['sYL1', 'sYL2', 'sYL3', 'sYL4', 'sYD1', 'sYD2', 'sYD3']
group_all1D    =  group_ch1D + group_sizeX1D + group_sizeY1D  

group_ch2D_int    = ['chL1VsInt'+InsSlice, 'chL2VsInt'+InsSlice, 'chL3VsInt'+InsSlice, 'chL4VsInt'+InsSlice, 'chD1VsInt'+InsSlice, 'chD2VsInt'+InsSlice, 'chD3VsInt'+InsSlice]               
group_sizeX2D_int = ['sXL1VsInt'+InsSlice, 'sXL2VsInt'+InsSlice, 'sXL3VsInt'+InsSlice, 'sXL4VsInt'+InsSlice, 'sXD1VsInt'+InsSlice, 'sXD2VsInt'+InsSlice, 'sXD3VsInt'+InsSlice]
group_sizeY2D_int = ['sYL1VsInt'+InsSlice, 'sYL2VsInt'+InsSlice, 'sYL3VsInt'+InsSlice, 'sYL4VsInt'+InsSlice, 'sYD1VsInt'+InsSlice, 'sYD2VsInt'+InsSlice, 'sYD3VsInt'+InsSlice]
group_all2D_int   = group_ch2D_int + group_sizeX2D_int + group_sizeY2D_int

group_ch2D_ins    = ['chL1VsInslumi', 'chL2VsInslumi', 'chL3VsInslumi', 'chL4VsInslumi', 'chD1VsInslumi', 'chD2VsInslumi', 'chD3VsInslumi']               
group_sizeX2D_ins = ['sXL1VsInslumi', 'sXL2VsInslumi', 'sXL3VsInslumi', 'sXL4VsInslumi', 'sXD1VsInslumi', 'sXD2VsInslumi', 'sXD3VsInslumi']
group_sizeY2D_ins = ['sYL1VsInslumi', 'sYL2VsInslumi', 'sYL3VsInslumi', 'sYL4VsInslumi', 'sYD1VsInslumi', 'sYD2VsInslumi', 'sYD3VsInslumi']
group_all2D_ins   = group_ch2D_ins + group_sizeX2D_ins + group_sizeY2D_ins

group_ch2D_pu    = ['chL1VsPileup', 'chL2VsPileup', 'chL3VsPileup', 'chL4VsPileup', 'chD1VsPileup', 'chD2VsPileup', 'chD3VsPileup']               
group_sizeX2D_pu = ['sXL1VsPileup', 'sXL2VsPileup', 'sXL3VsPileup', 'sXL4VsPileup', 'sXD1VsPileup', 'sXD2VsPileup', 'sXD3VsPileup']
group_sizeY2D_pu = ['sYL1VsPileup', 'sYL2VsPileup', 'sYL3VsPileup', 'sYL4VsPileup', 'sYD1VsPileup', 'sYD2VsPileup', 'sYD3VsPileup']
group_all2D_pu   = group_ch2D_pu + group_sizeX2D_pu + group_sizeY2D_pu

histo2D = {}

if lumiType == 'int':
    for subdet in group_all2D_int: histo2D[subdet] = f.Get(sliceDir+"/"+subdet) 
elif lumiType == 'ins':
    for subdet in group_all2D_ins: histo2D[subdet] = f.Get(subdet)
elif lumiType == 'PU':
    for subdet in group_all2D_pu:  histo2D[subdet] = f.Get(subdet)            

histo1D = {}

#sort the histogram lists according to cluster property; only charge distributions will be fitted to Landau+Gaussian shape
h_1D_ch = []; h_2D_ch = []; h_fit = []; chMaxYRange = 0;
h_1D_sX = []; h_2D_sX = [];             sXMaxYRange = 0;
h_1D_sY = []; h_2D_sY = [];             sYMaxYRange = 0;

for h in sorted(histo2D):
    if lumiType == 'int':   newN =  histo2D[h].GetName().replace('VsIntlumi', '')
    elif lumiType == 'ins': newN =  histo2D[h].GetName().replace('VsInslumi', '')
    elif lumiType == 'PU':  newN =  histo2D[h].GetName().replace('VsPileup', '')
    hist2D = histo2D[h].Clone()
    hist2D.RebinX(int(rebinSizeX))
    histY = hist2D.ProjectionY()
    histY.SetAxisRange(0., 70., "X")
    histY.SetName(newN)
    
    # charge
    if 'ch' in newN:
        if   lumiType == 'int': setHisto(hist2D, "Integrated Luminosity (fb^{-1})", "Norm. on-trk. charge (ke)", 1)
        elif lumiType == 'ins': setHisto(hist2D, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Norm. on-trk. charge (ke)", 1)
        elif lumiType == 'PU': setHisto(hist2D, "Pileup", "Norm. on-trk. charge (ke)", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", 0)
        h_fit.append(fitting(histY))
        h_1D_ch.append(histY)
        #if 'L1' in newN:
        #    histY.Draw("hist")
        #    h_fit[3].Draw("same")
        h_2D_ch.append(hist2D)
        if histY.GetMaximum() > chMaxYRange: chMaxYRange = histY.GetMaximum()
        
    # sizeX     
    if 'X' in newN:
        if   lumiType == 'int': setHisto(hist2D, "Integrated Luminosity (fb^{-1})", "On-Track cluster size in x-direction (pixel)", 1)
        elif lumiType == 'ins': setHisto(hist2D, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "On-Track cluster size in x-direction (pixel)", 1)
        elif lumiType == 'PU': setHisto(hist2D, "Pileup",  "On-Track cluster size in x-direction (pixel)", 1)
        setHisto(histY, "On-Track cluster size in x-direction (pixel)", "clusters", 0)
        h_1D_sX.append(histY)
        h_2D_sX.append(hist2D)
        if histY.GetMaximum() > sXMaxYRange: sXMaxYRange = histY.GetMaximum()

    # sizeY     
    if 'Y' in newN:
        if   lumiType == 'int': setHisto(hist2D, "Integrated Luminosity (fb^{-1})", "On-Track cluster size in y-direction (pixel)", 1)
        elif lumiType == 'ins': setHisto(hist2D, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "On-Track cluster size in y-direction (pixel)", 1)
        elif lumiType == 'PU': setHisto(hist2D, "Pileup",  "On-Track cluster size in y-direction (pixel)", 1)
        setHisto(histY, "On-Track cluster size in y-direction (pixel)", "clusters", 0)
        h_1D_sY.append(histY)
        h_2D_sY.append(hist2D)
        if histY.GetMaximum() > sYMaxYRange: sYMaxYRange = histY.GetMaximum()    

# Once historgams are sorted, prepare the Legends

boxc = TLegend(0.36, 0.78, 0.65, 0.84)
setLineLeg(legLine=boxc, fillColor=0, lineColor=0, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

legD = TLegend(0.36,0.78,0.50,0.60) #58
setLineLeg(legLine=legD, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

legL = TLegend(0.36,0.78,0.50,0.62) #58
setLineLeg(legLine=legL, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

legCond = TLegend (0.58, 0.76, 0.88, 0.62)
#setLineLeg(legLine=legCond, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

#legDCh = TLegend(0.70,0.88, 0.80, 0.70)#0.76,0.88,0.895,0.55
#setLineLeg(legLine=legDCh, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

#legDSx = TLegend(0.70,0.88, 0.80, 0.70)
#setLineLeg(legLine=legDSx, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

#legDSy = TLegend(0.70,0.88, 0.80, 0.70)
#setLineLeg(legLine=legDSy, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

#legLCh = TLegend(0.70,0.88,0.82,0.70)
#setLineLeg(legLine=legLCh, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

#legLSx = TLegend(0.70,0.88,0.82,0.70)
#setLineLeg(legLine=legLSx, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

#legLSy = TLegend(0.70,0.88,0.82,0.70)
#setLineLeg(legLine=legLSy, fillColor=10, lineColor=10, textSize=0.035, textAlign=12, boarderSize=0, lineWidth=0)

lsColor   = [633, 618, 601, 633, 618, 601, 433]
lsMarker  = [20, 21, 22, 20, 21, 22, 24]

h1DChColorMap = zip(h_1D_ch, lsColor, lsMarker)
h2DChColorMap = zip(h_2D_ch, lsColor, lsMarker)
h1DSXColorMap = zip(h_1D_sX, lsColor, lsMarker)
h2DSXColorMap = zip(h_2D_sX, lsColor, lsMarker)
h1DSYColorMap = zip(h_1D_sY, lsColor, lsMarker)
h2DSYColorMap = zip(h_2D_sY, lsColor, lsMarker)
fitChColorMap = zip(h_fit,   lsColor, lsMarker)

for h, c, m in h1DChColorMap:  setColor(h,c,m)
for h, c, m in h2DChColorMap:  setColor(h,c,m)
for h, c, m in h1DSXColorMap:  setColor(h,c,m)
for h, c, m in h2DSXColorMap:  setColor(h,c,m)
for h, c, m in h1DSYColorMap:  setColor(h,c,m)
for h, c, m in h2DSYColorMap:  setColor(h,c,m)
for h, c, m in fitChColorMap:  setColor(h,c,m)
   
# ----------------------------------------------
# Plot MP of charge vs intergrated Lumi.
# https://www.slac.stanford.edu/BFROOT/www/doc/tutorials/PhysicsWeekApril2000/RootTutorial-Histograms-intro.html
# ----------------------------------------------
h_sliceY = []
c_ch_d_MP_intL = TCanvas('c_ch_d_MP_intL', 'c_ch_d_MP_intL', 700, 800)
c_ch_d_MP_intL.SetGrid()

for h in range(0, 3):#len(h_2D_ch)
    n =  h_2D_ch[h].GetName()
    if 'ch' in n:
        aSlices = TObjArray()
        h_fit[h].SetRange(10, 60) 
        fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 0, -1, 0, "QNR", aSlices)
        #fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 7, 100, 0, "QNR", aSlices)
        aSlices[1].GetYaxis().SetRangeUser(12., 22.)
        aSlices[1].SetAxisRange(0., 70., "X")
        h_sliceY.append(aSlices[1])
        
hSliceYdColorMap = zip(h_sliceY[0:3], lsColor[0:3], lsMarker[0:3])
ymax = 0; ymin = 9999;
for h, c, m in hSliceYdColorMap:
    ymax   = h.GetMaximum()
    ymin   = h.GetMinimum()
    setColor(h, c, m)
    if   lumiType == 'int': setHisto(h, "Integrated Luminosity (fb^{-1})", "MPV On-track cluster charge (ke)", 1)
    elif lumiType == 'ins': setHisto(h, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "MPV On-track cluster charge (ke)", 1)
    elif lumiType == 'PU': setHisto(h, "Pileup", "MPV On-track cluster charge (ke)", 1)
    h.Draw("same")
    if 'D1' in h.GetName(): setHistLeg (h, "#scale[0.96]{#color[633]{Disk 1}}")
    if 'D2' in h.GetName(): setHistLeg (h, "#scale[0.96]{#color[618]{Disk 2}}")
    if 'D3' in h.GetName(): setHistLeg (h, "#scale[0.96]{#color[601]{Disk 3}}")
    
# Draw the condition lines
drawConditionLines(leg=legCond, barrel=0, yMin=ymin, yMax=ymax)

# display integ. lumi.
boxc.Draw()
drawLabels(lumiType)

# display histo legend
legD.Draw()
gPadSet()
c_ch_d_MP_intL.RedrawAxis()

if   lumiType == 'int': c_ch_d_MP_intL.SaveAs(plotdir+"ch2D_disk_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_ch_d_MP_intL.SaveAs(plotdir+"ch2D_disk_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_ch_d_MP_intL.SaveAs(plotdir+"ch2D_disk_Ins_Run_all.pdf")
elif lumiType == 'PU' and fill == '': c_ch_d_MP_intL.SaveAs(plotdir+"ch2D_disk_PU_Run_all.pdf")

raw_input('wait a bit ...')


ymax=0
for h in range(3, len(h_2D_ch)):
    n =  h_2D_ch[h].GetName()
    if 'ch' in n:
        aSlices = TObjArray()           
        h_fit[h].SetRange(12, 60)
        
        if lumiType == 'int':
            if h==3: fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 0, -1, 20, "QNR", aSlices) #QNR
            else: fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 0, -1, 20, "QNR", aSlices) #24, 20 or 30, 20
            #print aSlices[0], aSlices[1], aSlices[2], aSlices[3]
        else:  h_2D_ch[h].FitSlicesY(h_fit[h], 0, -1, 0, "QNR", aSlices)
        
        aSlices[1].GetYaxis().SetRangeUser(8., 28.)
        aSlices[1].SetAxisRange(0., 70., "X")
        h_sliceY.append(aSlices[1])
        '''
        if lumiType == 'int':
            if h==3:
                print 'fitS', fitS
                hL1bins=[]
                hL1_par0=[]
                hL1_par1=[]
                hL1_par2=[]
                hL1_par3=[]
                #hs = THStack("projY", "")
                fitUptoBin = 1000
                if   rebinSizeX == '1': fitUptoBin = 68
                if   rebinSizeX == '2': fitUptoBin = 34
                elif rebinSizeX == '3': fitUptoBin = 21
                for i in range(2, fitUptoBin):
                    h_temp = h_2D_ch[h].ProjectionY("bin"+str(i+1), i+1, i+2)
                    if h_temp.GetMaximum() > ymax: ymax = h_temp.GetMaximum() 
                    hL1bins.append(h_temp)
                    hL1_par0.append(aSlices[0])
                    hL1_par1.append(aSlices[1])
                    hL1_par2.append(aSlices[2])
                    hL1_par3.append(aSlices[3])
                    #hs.Add(h_2D_ch[h].ProjectionY("bin"+str(i+1), i+1, i+2))
                #hs.Draw("Hist")
        '''
'''            
if lumiType == 'int':              
    print  hL1bins, hL1_par0
    print  'ymax', ymax
    offset = 0.5
    ch_L1_Leg = TLegend(0.65,0.65-offset,0.85,0.88) #580.70,0.88,0.82,0.70)
    ch_L1_Leg.SetTextSize(0.035)
    ch_L1_Leg.SetBorderSize(0)
    ch_L1_Leg.SetFillColor(10)
    ch_L1_Leg.SetLineColor(10)
    ch_L1_Leg.SetLineWidth(0)

    c_L1_a = TCanvas('c_L1_a', 'c_L1_a', 1000, 500)
    c_L1_a.Divide(2,1)
    c_L1_a.cd(1)
    h_2D_ch[3].Draw("colz")

    c_L1_a.cd(2)
    c_j=0
    for h_j in reversed(hL1bins):    
        print h_j.GetName(), 'area:', h_j.Integral()
        if c_j <= 4:
            h_j.SetLineColor(kRed+c_j)
        elif c_j > 4 and c_j <= 8:
            h_j.SetLineColor(kGreen-c_j)
        elif  c_j > 8:
            h_j.SetLineColor(kBlue+c_j)
        ch_L1_Leg.AddEntry(h_j, h_j.GetName(), "L")
        #h_j.SetMaximum(ymax*(1.10))
        #h_j.SetMaximum(1.20)
        #print 'hello, lets print all histogram area : ', h_j.GetEntries()
        if h_j.GetEntries() != 0 :
            h_j.DrawNormalized("hist,same")
        c_j+=1
    
    ch_L1_Leg.Draw()
    c_L1_a.RedrawAxis()
    gPadSet()


    c_L1_b = TCanvas('c_L1', 'c_L1', 1000, 1000)
    c_L1_b.Divide(2,2)
    c_L1_b.cd(1)

    for h_p0 in reversed(hL1_par0):
        h_p0.SetMarkerColor(kRed)
        h_p0.SetMarkerStyle(20)
        h_p0.SetMarkerSize(0.6)
        h_p0.SetMinimum(1.2)
        h_p0.Draw()
    
    c_L1_b.cd(2)    
    for h_p1 in reversed(hL1_par1):
        h_p1.SetMarkerColor(kRed)
        h_p1.SetMarkerStyle(20)
        h_p1.SetMarkerSize(0.6)
        h_p1.Draw()
    
    c_L1_b.cd(3)    
    for h_p2 in reversed(hL1_par2):
        h_p2.SetMarkerColor(kRed)
        h_p2.SetMarkerStyle(20)
        h_p2.SetMarkerSize(0.6)
        h_p2.Draw()

    c_L1_b.cd(4)    
    for h_p3 in reversed(hL1_par3):
        h_p3.SetMarkerColor(kRed)
        h_p3.SetMarkerStyle(20)
        h_p3.SetMarkerSize(0.6)
        h_p3.SetMinimum(4)
        h_p3.Draw()    

    #ch_L1_Leg.Draw()
    c_L1_b.RedrawAxis()
    gPadSet()

if  lumiType == 'int':
    c_L1_a.SaveAs(plotdir+"chL1_Int_"+InsSlice+"_Run_all.pdf")
    c_L1_b.SaveAs(plotdir+"chL1_Parm_Int_"+InsSlice+"_Run_all.pdf")
raw_input('freez ...')
'''

c_ch_b_MP_intL = TCanvas('c_ch_b_MP_intL', 'c_ch_b_MP_intL', 700, 800)
c_ch_b_MP_intL.SetGrid()

hSliceYbColorMap = zip(h_sliceY[3:7], lsColor[3:7], lsMarker[3:7])
    
for h, c, m in hSliceYbColorMap:
    ymax   = h.GetMaximum()
    ymin   = h.GetMinimum()
    setColor(h, c, m)
    if   lumiType == 'int': setHisto(h, "Integrated Luminosity (fb^{-1})", "MPV On-track cluster charge (ke)", 1)
    elif lumiType == 'ins': setHisto(h, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "MPV On-track cluster charge (ke)", 1)
    elif lumiType == 'PU': setHisto(h, "Pileup", "MPV On-track cluster charge (ke)", 1)
    h.Draw("same")

    if 'L1' in h.GetName(): setHistLeg (h, "#scale[0.96]{#color[633]{Layer 1}}")
    if 'L2' in h.GetName(): setHistLeg (h, "#scale[0.96]{#color[618]{Layer 2}}")
    if 'L3' in h.GetName(): setHistLeg (h, "#scale[0.96]{#color[601]{Layer 3}}")
    if 'L4' in h.GetName(): setHistLeg (h, "#scale[0.96]{#color[433]{Layer 4}}")

# Draw the condition lines
drawConditionLines(leg=legCond, barrel=1, yMin=ymin, yMax=ymax)

# display integ. lumi.
boxc.Draw()
drawLabels(lumiType)

# display histo legend
legL.Draw()
gPadSet()
c_ch_b_MP_intL.RedrawAxis()

if   lumiType == 'int': c_ch_b_MP_intL.SaveAs(plotdir+"ch2D_barrel_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_ch_b_MP_intL.SaveAs(plotdir+"ch2D_barrel_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_ch_b_MP_intL.SaveAs(plotdir+"ch2D_barrel_Ins_Run_all.pdf")
elif lumiType == 'PU' and fill == '': c_ch_b_MP_intL.SaveAs(plotdir+"ch2D_barrel_PU_Run_all.pdf")

raw_input('wait a bit ...')

# ----------------------------------------------
# Plot Ave value of clustSizeX vs intergrated Lumi.
# ----------------------------------------------
c_sX_d_intL = TCanvas('c_sX_d_intL', 'c_sX_d_intL', 700, 800)
c_sX_d_intL.SetGrid()

for h in range(0,3):#len(h_2D_sX)):    
    h1 =  h_2D_sX[h].ProfileX()    
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size x (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size x (pixel)", 1)
    elif lumiType == 'PU': setHisto(h1, "Pileup", "Ave On-track cluster size x (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 5.)
    ymax   = h1.GetMaximum(); ymin   = h1.GetMinimum()
    if ymax < 5.: ymax = 5.       
    h1.SetAxisRange(0., 70., "X")
    h1.Draw("same")
    
# Draw the condition lines
drawConditionLines(leg=legCond, barrel=0, yMin=ymin, yMax=ymax)

# display integ. lumi.
boxc.Draw()    
drawLabels(lumiType)

# display histo legend
legD.Draw()
c_sX_d_intL.RedrawAxis()
gPadSet()

if   lumiType == 'int': c_sX_d_intL.SaveAs(plotdir+"sX2D_disk_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sX_d_intL.SaveAs(plotdir+"sX2D_disk_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sX_d_intL.SaveAs(plotdir+"sX2D_disk_Ins_Run_all.pdf")
elif lumiType == 'PU' and fill == '': c_sX_d_intL.SaveAs(plotdir+"sX2D_disk_PU_Run_all.pdf")

raw_input('wait a bit ...')

c_sX_b_intL = TCanvas('c_sX_b_intL', 'c_sX_b_intL', 700, 800)
c_sX_b_intL.SetGrid()

for h in range(3, len(h_2D_sX)):
    h1 =  h_2D_sX[h].ProfileX()
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size x (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size x (pixel)", 1)
    elif lumiType == 'PU': setHisto(h1, "Pileup", "Ave On-track cluster size x (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 5.)
    h1.SetAxisRange(0., 70., "X")
    h1.Draw("same")

# Draw the condition lines
drawConditionLines(leg=legCond, barrel=1, yMin=ymin, yMax=ymax)

# display integ. lumi.
boxc.Draw()    
drawLabels(lumiType)

legL.Draw()
gPadSet()
c_sX_b_intL.RedrawAxis()

if   lumiType == 'int': c_sX_b_intL.SaveAs(plotdir+"sX2D_barrel_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sX_b_intL.SaveAs(plotdir+"sX2D_barrel_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sX_b_intL.SaveAs(plotdir+"sX2D_barrel_Ins_Run_all.pdf")
elif lumiType == 'PU' and fill == '': c_sX_b_intL.SaveAs(plotdir+"sX2D_barrel_PU_Run_all.pdf")

raw_input('wait a bit ...')

# ----------------------------------------------
# Plot Ave value of clustSizeY vs intergrated Lumi.
# ----------------------------------------------

c_sY_d_intL = TCanvas('c_sY_d_intL', 'c_sY_d_intL', 700, 800)
c_sY_d_intL.SetGrid()

for h in range(0,3):#len(h_2D_sY)):
    h1 =  h_2D_sY[h].ProfileX()
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size y (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size y (pixel)", 1)
    elif lumiType == 'PU': setHisto(h1, "Pileup", "Ave On-track cluster size y (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 5.)
    ymax   = h1.GetMaximum(); ymin   = h1.GetMinimum()
    if ymax < 5.: ymax = 5.       
    h1.SetAxisRange(0., 70., "X")
    h1.Draw("same")

# Draw the condition lines
drawConditionLines(leg=legCond, barrel=0, yMin=ymin, yMax=ymax)

# display integ. lumi.
boxc.Draw()        
drawLabels(lumiType)

# display histo legend
legD.Draw()
gPadSet()
c_sY_d_intL.RedrawAxis()

if   lumiType == 'int': c_sY_d_intL.SaveAs(plotdir+"sXYD_disk_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sY_d_intL.SaveAs(plotdir+"sY2D_disk_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sY_d_intL.SaveAs(plotdir+"sY2D_disk_Ins_Run_all.pdf")
elif lumiType == 'PU' and fill == '': c_sY_d_intL.SaveAs(plotdir+"sY2D_disk_PU_Run_all.pdf")

raw_input('wait a bit ...')

c_sY_b_intL = TCanvas('c_sY_b_intL', 'c_sY_b_intL', 700, 800)
c_sY_b_intL.SetGrid()

for h in range(3, len(h_2D_sY)):
    h1 =  h_2D_sY[h].ProfileX()
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size y (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size y (pixel)", 1)
    elif lumiType == 'PU': setHisto(h1, "Pileup", "Ave On-track cluster size y (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 10.)
    ymax   = h1.GetMaximum(); ymin   = h1.GetMinimum()
    if ymax < 10.: ymax = 10.    
    h1.SetAxisRange(0., 70., "X")
    h1.Draw("same")

# Draw the condition lines
drawConditionLines(leg=legCond, barrel=1, yMin=ymin, yMax=ymax)

# display integ. lumi.
boxc.Draw()    
drawLabels(lumiType)

# display histo legend
legL.Draw()
gPadSet()
c_sY_b_intL.RedrawAxis()

if   lumiType == 'int': c_sY_b_intL.SaveAs(plotdir+"sY2D_barrel_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sY_b_intL.SaveAs(plotdir+"sY2D_barrel_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sY_b_intL.SaveAs(plotdir+"sY2D_barrel_Ins_Run_all.pdf")
elif lumiType == 'PU' and fill == '': c_sY_b_intL.SaveAs(plotdir+"sY2D_barrel_PU_Run_all.pdf")

raw_input('wait a bit ...')

