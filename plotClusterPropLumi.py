#!/usr/bin/env python
import os, sys, math, array, operator
from ROOT import gROOT, TFile, TF1, gPad, gStyle, gDirectory, TTree, TCanvas, TH1F, TH2F, TH1D, TProfile, TObjArray, TStopwatch, TGaxis, TLegend, TLatex, THStack
from ROOT import kBlack, kYellow, kGreen, kOrange, kGreen, kMagenta, kRed, kBlue, kTeal, kPink, kViolet, kCyan, kTRUE
#from readLumi import readLumiInfo
gROOT.ProcessLine('.L ./fitting.C')
#gROOT.SetBatch(True)
from ROOT import fitting
gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetLineWidth(2)
TGaxis.SetMaxDigits(3)

def setLeg(histo, legText):
    if 'D' in histo.GetName():
        legD.AddEntry(histo, legText, "pl")
    if 'L' in histo.GetName():
        legL.AddEntry(histo, legText, "pl")
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
    if lumiType == 'ins': lf.DrawLatex(0.36, 0.80, 'Fill: '+ fill)
    
    lw.DrawLatex(0.12, 0.91, 'CMS')
    le.DrawLatex(0.66, 0.91, '#bf{#sqrt{s} = 13 TeV}')
    lp.DrawLatex(0.24, 0.91, 'Preliminary 2018')#Preliminary 2018')

def gPadSet():
    gPad.SetTickx(1)
    gPad.SetTicky(1)
    gPad.SetLeftMargin(0.12)
    gPad.SetRightMargin(1.4)
    gPad.SetBottomMargin(0.10)
    gPad.SetFrameLineWidth(2)
    gPad.RedrawAxis()
    #gPad.Update()    
# ==========
# options
# ===============
def runs(option, opt, value, parser):
    setattr(parser.values, option.dest, value.splt(','))
            
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='PlotsDec/', 
                  dest='plotDir',
                  help='output directory of plots')
parser.add_option('--slicePerInstLumi', metavar='S', action='store_true',
                  default=True, 
                  dest='slicePerInstLumi',
                  help='output directory of plots')
parser.add_option('--sliceDir', metavar='F', type='string', action='store',
                  default='inslumi13to15', 
                  dest='sliceDir',
                  help='ins lumi subdir 6to8,  8to10, 11to13, 13to15')
#parser.add_option('--lumiRange', metavar='I', type='string', action='store',
#                  default='', 
#                  dest='lumiRange',
#                  help='inst. lumi. range')                                            
parser.add_option('--runList', metavar='l', type='string', action='callback', callback = runs,
                  default= '317648, 317649, 317650',
                  dest='runList',
                  help='run list')
parser.add_option('--lumiType', metavar='L', type='string', action='store',
                  default='int', #int #ins 
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
#lumiRange   = options.lumiRange
lumiType    = options.lumiType
sliceDir    = options.sliceDir
runList     = options.runList.split(',')
fill        = options.fill

#RUN         = inFile.split('_')[1].replace('.root', '')
#print RUN
f = TFile.Open(inFile)

group_ch1D     = ['chL1', 'chL2', 'chL3', 'chL4', 'chD1', 'chD2', 'chD3']
group_sizeX1D  = ['sXL1', 'sXL2', 'sXL3', 'sXL4', 'sXD1', 'sXD2', 'sXD3']
group_sizeY1D  = ['sYL1', 'sYL2', 'sYL3', 'sYL4', 'sYD1', 'sYD2', 'sYD3']
group_all1D    =  group_ch1D + group_sizeX1D + group_sizeY1D  

if sliceL==True :
    if '13to15' in sliceDir:
        InsSlice='13to15lumi'
        lumiRange='13-15'
    elif '11to13' in sliceDir:
        InsSlice='11to13lumi'
        lumiRange='11-13'
    elif '8to10' in sliceDir:
        InsSlice='8to10lumi'
        lumiRange='8-10'
    elif '6to8' in sliceDir:
        InsSlice='6to8lumi'
        lumiRange='6-8'      
    else:
        InsSlice = 'lumi'
        lumiRange=''
group_ch2D_int    = ['chL1VsInt'+InsSlice, 'chL2VsInt'+InsSlice, 'chL3VsInt'+InsSlice, 'chL4VsInt'+InsSlice, 'chD1VsInt'+InsSlice, 'chD2VsInt'+InsSlice, 'chD3VsInt'+InsSlice]               
group_sizeX2D_int = ['sXL1VsInt'+InsSlice, 'sXL2VsInt'+InsSlice, 'sXL3VsInt'+InsSlice, 'sXL4VsInt'+InsSlice, 'sXD1VsInt'+InsSlice, 'sXD2VsInt'+InsSlice, 'sXD3VsInt'+InsSlice]
group_sizeY2D_int = ['sYL1VsInt'+InsSlice, 'sYL2VsInt'+InsSlice, 'sYL3VsInt'+InsSlice, 'sYL4VsInt'+InsSlice, 'sYD1VsInt'+InsSlice, 'sYD2VsInt'+InsSlice, 'sYD3VsInt'+InsSlice]
group_all2D_int   = group_ch2D_int + group_sizeX2D_int + group_sizeY2D_int

group_ch2D_ins    = ['chL1VsInslumi', 'chL2VsInslumi', 'chL3VsInslumi', 'chL4VsInslumi', 'chD1VsInslumi', 'chD2VsInslumi', 'chD3VsInslumi']               
group_sizeX2D_ins = ['sXL1VsInslumi', 'sXL2VsInslumi', 'sXL3VsInslumi', 'sXL4VsInslumi', 'sXD1VsInslumi', 'sXD2VsInslumi', 'sXD3VsInslumi']
group_sizeY2D_ins = ['sYL1VsInslumi', 'sYL2VsInslumi', 'sYL3VsInslumi', 'sYL4VsInslumi', 'sYD1VsInslumi', 'sYD2VsInslumi', 'sYD3VsInslumi']
group_all2D_ins   = group_ch2D_ins + group_sizeX2D_ins + group_sizeY2D_ins

histo2D = {}

if lumiType == 'int':
    for subdet in group_all2D_int:
        histo2D[subdet] = f.Get(sliceDir+"/"+subdet)
elif lumiType == 'ins':
    for subdet in group_all2D_ins:
        histo2D[subdet] = f.Get(subdet)    

#print histo2D

histo1D = {}

#sort the histogram lists accoring to cluster property
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


for h in sorted(histo2D):
    if lumiType == 'int':
        #print histo2D[h].GetName()
        newN =  histo2D[h].GetName().replace('VsIntlumi', '')
    elif lumiType == 'ins': newN =  histo2D[h].GetName().replace('VsInslumi', '')   
    hist2D = histo2D[h].Clone()
    hist2D.RebinX(2)
    histY = hist2D.ProjectionY()
    histY.SetName(newN)
    # charge
    if 'ch' in newN:
        if   lumiType == 'int': setHisto(hist2D, "Integrated Luminosity (fb^{-1})", "Norm. on-trk. charge (ke)", 1)
        elif lumiType == 'ins': setHisto(hist2D, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Norm. on-trk. charge (ke)", 1)
        setHisto(histY, "Norm. on-trk. charge (ke)", "events", 0)
        h_fit.append(fitting(histY))
        h_1D_ch.append(histY)
        if 'L1' in newN:
            histY.Draw("hist")
            h_fit[3].Draw("same")
            raw_input('freez ...')
        h_2D_ch.append(hist2D)
        if histY.GetMaximum() > chMaxYRange: chMaxYRange = histY.GetMaximum()
    # sizeX     
    if 'X' in newN:
        if   lumiType == 'int': setHisto(hist2D, "Integrated Luminosity (fb^{-1})", "On-Track cluster size in x-direction (pixel)", 1)
        elif lumiType == 'ins': setHisto(hist2D, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "On-Track cluster size in x-direction (pixel)", 1)
        setHisto(histY, "On-Track cluster size in x-direction (pixel)", "clusters", 0)
        h_1D_sX.append(histY)
        h_2D_sX.append(hist2D)
        if histY.GetMaximum() > sXMaxYRange: sXMaxYRange = histY.GetMaximum()

    # sizeY     
    if 'Y' in newN:
        if   lumiType == 'int': setHisto(hist2D, "Integrated Luminosity (fb^{-1})", "On-Track cluster size in y-direction (pixel)", 1)
        elif lumiType == 'ins': setHisto(hist2D, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "On-Track cluster size in y-direction (pixel)", 1)
        setHisto(histY, "On-Track cluster size in y-direction (pixel)", "clusters", 0)
        h_1D_sY.append(histY)
        h_2D_sY.append(hist2D)
        if histY.GetMaximum() > sYMaxYRange: sYMaxYRange = histY.GetMaximum()    

#print histo1D

legD = TLegend(0.36,0.78,0.50,0.60) #58
legD.SetTextSize(0.035)
legD.SetBorderSize(0)
legD.SetFillColor(10)
legD.SetLineColor(10)
legD.SetLineWidth(0)


legL = TLegend(0.36,0.78,0.50,0.62) #58
legL.SetTextSize(0.035)
legL.SetBorderSize(0)
legL.SetFillColor(10)
legL.SetLineColor(10)
legL.SetLineWidth(0)

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


print h_1D_ch

lsColor   = [633, 618, 601, 633, 618, 601, 433]
lsMarker  = [20, 21, 22, 20, 21, 22, 24 ]

h1DChColorMap = zip(h_1D_ch, lsColor, lsMarker)
h2DChColorMap = zip(h_2D_ch, lsColor, lsMarker)
h1DSXColorMap = zip(h_1D_sX, lsColor, lsMarker)
h2DSXColorMap = zip(h_2D_sX, lsColor, lsMarker)
h1DSYColorMap = zip(h_1D_sY, lsColor, lsMarker)
h2DSYColorMap = zip(h_2D_sY, lsColor, lsMarker)
fitChColorMap = zip(h_fit,   lsColor, lsMarker)

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
    
for h, c, m in fitChColorMap:
    setColor(h,c,m)

# ----------------------------------------------
# Plot MP of charge vs intergrated Lumi.
# https://www.slac.stanford.edu/BFROOT/www/doc/tutorials/PhysicsWeekApril2000/RootTutorial-Histograms-intro.html
# ----------------------------------------------
h_sliceY = []
c_ch_d_MP_intL = TCanvas('c_ch_d_MP_intL', 'c_ch_d_MP_intL', 700, 800)
#c_ch_d_MP_intL.SetGrid()
for h in range(0, 3):#len(h_2D_ch)
    n =  h_2D_ch[h].GetName()
    if 'ch' in n:
        aSlices = TObjArray()
        h_fit[h].SetRange(10, 50)
        fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 0, 100, 0, "QNR", aSlices)
        aSlices[1].GetYaxis().SetRangeUser(12., 22.)
        h_sliceY.append(aSlices[1])
        
hSliceYdColorMap = zip(h_sliceY[0:3], lsColor[0:3], lsMarker[0:3])

for h, c, m in hSliceYdColorMap:
    setColor(h, c, m)
    if   lumiType == 'int': setHisto(h, "Integrated Luminosity (fb^{-1})", "MPV On-track cluster charge (ke)", 1)
    elif lumiType == 'ins': setHisto(h, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "MPV On-track cluster charge (ke)", 1)
    h.Draw("same")
    if 'D1' in h.GetName(): setLeg (h, "#scale[0.96]{#color[633]{Disk 1}}")
    if 'D2' in h.GetName(): setLeg (h, "#scale[0.96]{#color[618]{Disk 2}}")
    if 'D3' in h.GetName(): setLeg (h, "#scale[0.96]{#color[601]{Disk 3}}")

drawLabels(lumiType) 
legD.Draw()
c_ch_d_MP_intL.RedrawAxis()
gPadSet()

if   lumiType == 'int': c_ch_d_MP_intL.SaveAs(plotdir+"ch2D_disk_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_ch_d_MP_intL.SaveAs(plotdir+"ch2D_disk_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_ch_d_MP_intL.SaveAs(plotdir+"ch2D_disk_Ins_Run_all.pdf")

raw_input('wait a bit ...')


#c_ch_b_MP_intL.SetGrid()
ymax=0
for h in range(3, len(h_2D_ch)):
    n =  h_2D_ch[h].GetName()
    if 'ch' in n:
        aSlices = TObjArray()
           
        h_fit[h].SetRange(11, 50)
        if h==3:
            fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 0, 24, 20, "R", aSlices) #QNR
        else:
            fitS = h_2D_ch[h].FitSlicesY(h_fit[h], 0, 24, 20, "QNR", aSlices) 
        print aSlices[0], aSlices[1], aSlices[2], aSlices[3]
        aSlices[1].GetYaxis().SetRangeUser(12., 28.)
        h_sliceY.append(aSlices[1])
        
        if h==3:
            print 'fitS', fitS
            hL1bins=[]
            hL1_par0=[]
            hL1_par1=[]
            hL1_par2=[]
            hL1_par3=[]
            #hs = THStack("projY", "")
            for i in range(2, 12):
                h_temp = h_2D_ch[h].ProjectionY("bin"+str(i+1), i+1, i+2)
                if h_temp.GetMaximum() > ymax: ymax = h_temp.GetMaximum() 
                hL1bins.append(h_temp)
                hL1_par0.append(aSlices[0])
                hL1_par1.append(aSlices[1])
                hL1_par2.append(aSlices[2])
                hL1_par3.append(aSlices[3])
                #hs.Add(h_2D_ch[h].ProjectionY("bin"+str(i+1), i+1, i+2))
            #hs.Draw("Hist")
            
              
print  hL1bins, hL1_par0
print  ymax
ch_L1_Leg = TLegend(0.70,0.88,0.82,0.60) #580.70,0.88,0.82,0.70)
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
    elif c_j > 4:
        h_j.SetLineColor(kGreen-c_j)
    ch_L1_Leg.AddEntry(h_j, h_j.GetName(), "L")
    #h_j.SetMaximum(ymax*(1.10))
    #h_j.SetMaximum(1.20)
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
    h_p0.SetMinimum(1.8)
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

if   lumiType == 'int':
    c_L1_a.SaveAs(plotdir+"chL1_Int_"+InsSlice+"_Run_all.pdf")
    c_L1_b.SaveAs(plotdir+"chL1_Parm_Int_"+InsSlice+"_Run_all.pdf")
raw_input('freez ...')

c_ch_b_MP_intL = TCanvas('c_ch_b_MP_intL', 'c_ch_b_MP_intL', 700, 800)

hSliceYbColorMap = zip(h_sliceY[3:7], lsColor[3:7], lsMarker[3:7])

for h, c, m in hSliceYbColorMap:
    setColor(h, c, m)
    if   lumiType == 'int': setHisto(h, "Integrated Luminosity (fb^{-1})", "MPV On-track cluster charge (ke)", 1)
    elif lumiType == 'ins': setHisto(h, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "MPV On-track cluster charge (ke)", 1)
    h.Draw("same")
    if 'L1' in h.GetName(): setLeg (h, "#scale[0.96]{#color[633]{Layer 1}}")
    if 'L2' in h.GetName(): setLeg (h, "#scale[0.96]{#color[618]{Layer 2}}")
    if 'L3' in h.GetName(): setLeg (h, "#scale[0.96]{#color[601]{Layer 3}}")
    if 'L4' in h.GetName(): setLeg (h, "#scale[0.96]{#color[433]{Layer 4}}")
    
drawLabels(lumiType) 
legL.Draw()
c_ch_b_MP_intL.RedrawAxis()
gPadSet()

if   lumiType == 'int': c_ch_b_MP_intL.SaveAs(plotdir+"ch2D_barrel_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_ch_b_MP_intL.SaveAs(plotdir+"ch2D_barrel_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_ch_b_MP_intL.SaveAs(plotdir+"ch2D_barrel_Ins_Run_all.pdf")

raw_input('wait a bit ...')

# ----------------------------------------------
# Plot Ave value of clustSizeX vs intergrated Lumi.
# ----------------------------------------------
c_sX_d_intL = TCanvas('c_sX_d_intL', 'c_sX_d_intL', 700, 800)
#c_sX_d_intL.SetGrid()
for h in range(0,3):#len(h_2D_sX)):
    h1 =  h_2D_sX[h].ProfileX()
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size x (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size x (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 5.)
    h1.Draw("same")

drawLabels(lumiType)
legD.Draw()
gPadSet()

c_sX_d_intL.RedrawAxis()
if   lumiType == 'int': c_sX_d_intL.SaveAs(plotdir+"sX2D_disk_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sX_d_intL.SaveAs(plotdir+"sX2D_disk_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sX_d_intL.SaveAs(plotdir+"sX2D_disk_Ins_Run_all.pdf")

raw_input('wait a bit ...')

c_sX_b_intL = TCanvas('c_sX_b_intL', 'c_sX_b_intL', 700, 800)
#c_sX_b_intL.SetGrid()
for h in range(3, len(h_2D_sX)):
    h1 =  h_2D_sX[h].ProfileX()
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size x (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size x (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 5.)
    h1.Draw("same")

drawLabels(lumiType)
legL.Draw()
gPadSet()

c_sX_b_intL.RedrawAxis()
if   lumiType == 'int': c_sX_b_intL.SaveAs(plotdir+"sX2D_barrel_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sX_b_intL.SaveAs(plotdir+"sX2D_barrel_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sX_b_intL.SaveAs(plotdir+"sX2D_barrel_Ins_Run_all.pdf")

raw_input('wait a bit ...')

# ----------------------------------------------
# Plot Ave value of clustSizeY vs intergrated Lumi.
# ----------------------------------------------

c_sY_d_intL = TCanvas('c_sY_d_intL', 'c_sY_d_intL', 700, 800)
#c_sY_d_intL.SetGrid()
for h in range(0,3):#len(h_2D_sY)):
    h1 =  h_2D_sY[h].ProfileX()
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size y (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size y (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 5.)
    h1.Draw("same")

drawLabels(lumiType)
legD.Draw()
gPadSet()

c_sY_d_intL.RedrawAxis()
if   lumiType == 'int': c_sY_d_intL.SaveAs(plotdir+"sXYD_disk_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sY_d_intL.SaveAs(plotdir+"sY2D_disk_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sY_d_intL.SaveAs(plotdir+"sY2D_disk_Ins_Run_all.pdf")

raw_input('wait a bit ...')

c_sY_b_intL = TCanvas('c_sY_b_intL', 'c_sY_b_intL', 700, 800)
#c_sY_b_intL.SetGrid()
for h in range(3, len(h_2D_sY)):
    h1 =  h_2D_sY[h].ProfileX()
    if   lumiType == 'int': setHisto(h1, "Integrated Luminosity (fb^{-1})", "Ave On-track cluster size y (pixel)", 1)
    elif lumiType == 'ins': setHisto(h1, "Instantaneous Luminosity (#times10^{33}cm^{-2}s^{-1})", "Ave On-track cluster size y (pixel)", 1)
    h1.GetYaxis().SetRangeUser(0., 10.)
    h1.Draw("same")

drawLabels(lumiType)
legL.Draw()
gPadSet()

c_sY_b_intL.RedrawAxis()
if   lumiType == 'int': c_sY_b_intL.SaveAs(plotdir+"sY2D_barrel_Int_"+InsSlice+"_Run_all.pdf")
elif lumiType == 'ins' and fill != '': c_sY_b_intL.SaveAs(plotdir+"sY2D_barrel_Ins_Fill_"+fill+".pdf")
elif lumiType == 'ins' and fill == '': c_sY_b_intL.SaveAs(plotdir+"sY2D_barrel_Ins_Run_all.pdf")

raw_input('wait a bit ...')

