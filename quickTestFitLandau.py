#! /usr/bin/env python
import sys
from ROOT import gROOT, gStyle, gPad, TFile, TTree, TCanvas, TH1F, TLegend, TLatex, TGaxis, kTRUE, kBlack, kGreen, kOrange, kGreen, kRed, kBlue
gROOT.ProcessLine('.L ./fitting.C')
from ROOT import fitting

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
TGaxis.SetMaxDigits(3)

def setHisto(histo, xTitle, yTitle, color, legText, ymax, v):
    histo.GetXaxis().SetTitle( xTitle )
    histo.GetYaxis().SetTitle( yTitle )
    histo.SetLineWidth(2)
    #histo.SetMarkerStyle(31)
    #histo.SetMarkerSize(2)
    #histo.SetMarkerColor(color)
    histo.SetLineColor(color)
    if  v == 0:
        leg.AddEntry(histo, legText, "pl")
    elif v == 1:
        leg2.AddEntry(histo, legText, "pl")
    histo.SetMaximum(ymax)
    histo.SetMinimum(0.)
    
# =============== 
# options
# ===============
from optparse import OptionParser
parser = OptionParser()	  	

parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Plots/', 
                  dest='plotDir',
                  help='output directory of plots')

parser.add_option('--var', metavar='P', type='string', action='store',
                  default='sizeY', #sizeX, norm_charge
                  dest='var',
                  help='variable to plot')

parser.add_option('--fill', metavar='P', type='string', action='store',
                  default='6573', 
                  dest='fill',
                  help='data fill number to identify the output .pdf files')

(options,args) = parser.parse_args()
# ==========end: options =============

plotdir = options.plotDir
var     = options.var
fill    = option.fill

barrel = "mod_on.det == 0"
endcap = "mod_on.det == 1"

layer1 = "mod_on.layer == 1"+" && "+ barrel
layer2 = "mod_on.layer == 2"+" && "+ barrel
layer3 = "mod_on.layer == 3"+" && "+ barrel
layer4 = "mod_on.layer == 4"+" && "+ barrel

disk1  = "mod_on.disk == 1"+" &&  "+ endcap
disk2  = "mod_on.disk == 2"+" &&  "+ endcap
disk3  = "mod_on.disk == 3"+" &&  "+ endcap

#provide title and histogram properties for each variable
hset = ['', 100, 0., 1000.]
if var == 'norm_charge':
    hset = ['charge', 70, 0, 140]
    varRange = "traj.norm_charge > 0. && traj.norm_charge < 120."
    leaf = "traj.norm_charge"
    xTitle = "Normalized On-Track cluster charge (ke)"
if var == 'size':
    hset = ['size', 20, 0, 20.5]
    varRange = "clust.size > 0."
    leaf = "clust.size"
    xTitle = "On-Track cluster size (pixel)"
if var == 'sizeX':
    hset = ['size in x-direction', 20, 0.5, 20.5]
    varRange = "clust.sizeX > 0."
    leaf = "clust.sizeX"
    xTitle = "On-Track cluster size in x-direction (pixel)"
if var == 'sizeY':
    hset = ['size in y-direction',  20, 0.5, 20.5]
    varRange = "clust.sizeY > 0."
    leaf = "clust.sizeY"
    xTitle = "On-Track cluster size in y-direction (pixel)"
    
f = TFile.Open('../Ntuples/v0406_default_1012p2_101X_dataRun2_Express_v7_Fill6573_Ntuple.root')
t = f.Get("trajTree")
#h = TH1F("h","cluster charge", 70, 0, 140)

h_l1 = TH1F("hcluster_"+var+"_l1", hset[0]+" layer 1", hset[1], hset[2], hset[3])
h_l2 = TH1F("hcluster_"+var+"_l2", hset[0]+" layer 2", hset[1], hset[2], hset[3])
h_l3 = TH1F("hcluster_"+var+"_l3", hset[0]+" layer 3", hset[1], hset[2], hset[3])
h_l4 = TH1F("hcluster_"+var+"_l4", hset[0]+" layer 4", hset[1], hset[2], hset[3])


h_d1 = TH1F("hcluster_"+var+"_d1", hset[0]+" disk 1", hset[1], hset[2], hset[3])
h_d2 = TH1F("hcluster_"+var+"_d2", hset[0]+" disk 2", hset[1], hset[2], hset[3])
h_d3 = TH1F("hcluster_"+var+"_d3", hset[0]+" disk 3", hset[1], hset[2], hset[3])


t.Draw(leaf+ " >> hcluster_"+var+"_l1", varRange+" && "+layer1)
t.Draw(leaf+ " >> hcluster_"+var+"_l2", varRange+" && "+layer2)
t.Draw(leaf+ " >> hcluster_"+var+"_l3", varRange+" && "+layer3)
t.Draw(leaf+ " >> hcluster_"+var+"_l4", varRange+" && "+layer4)

t.Draw(leaf+ " >> hcluster_"+var+"_d1", varRange+" && "+disk1)
t.Draw(leaf+ " >> hcluster_"+var+"_d2", varRange+" && "+disk2)
t.Draw(leaf+ " >> hcluster_"+var+"_d3", varRange+" && "+disk3)

c = TCanvas('c', 'c', 800, 640)
leg = TLegend(0.60,0.89,0.90, 0.69)
leg.SetBorderSize(0)
leg.SetFillColor(10)
leg.SetLineColor(10)
leg.SetLineWidth(0)


if var == "norm_charge":
    f_l1 = fitting(h_l1)
    f_l2 = fitting(h_l2)
    f_l3 = fitting(h_l3)
    f_l4 = fitting(h_l4)
    MP_l1 = round(f_l1.GetParameter('MP'),3)
    MPe_l1 = round(f_l1.GetParError(1),3)
    MP_l2 = round(f_l2.GetParameter('MP'),3)
    MPe_l2 = round(f_l2.GetParError(1),3)
    MP_l3 = round(f_l3.GetParameter('MP'),3)
    MPe_l3 = round(f_l3.GetParError(1),3)
    MP_l4 = round(f_l4.GetParameter('MP'),3)
    MPe_l4 = round(f_l4.GetParError(1),3)
   
max_y = max(h_l1.GetMaximum(), h_l2.GetMaximum(), h_l3.GetMaximum(), h_l4.GetMaximum())

setHisto(h_l1, xTitle, "Clusters", kBlack,  'Layer 1', max_y+max_y*0.1, 0)
setHisto(h_l2, xTitle, "Clusters", kBlue,   'Layer 2', max_y+max_y*0.1, 0)
setHisto(h_l3, xTitle, "Clusters", kGreen,  'Layer 3', max_y+max_y*0.1, 0)
setHisto(h_l4, xTitle, "Clusters", kOrange, 'Layer 4', max_y+max_y*0.1, 0)

h_l1.Draw("hist")
h_l2.Draw("hist, same")
h_l3.Draw("hist, same")
h_l4.Draw("hist, same")

lb = TLatex()

if var == "norm_charge":
    f_l1.SetMaximum(max_y+a)
    f_l2.SetMaximum(max_y+a)
    f_l3.SetMaximum(max_y+a)
    f_l4.SetMaximum(max_y+a)
    f_l1.Draw("lsame")
    f_l2.Draw("lsame")
    f_l3.Draw("lsame")
    f_l4.Draw("lsame")
    lb.SetNDC(kTRUE)
    lb.SetTextSize(0.025)
    lb.SetTextAlign(13)
    lb.DrawLatex(0.5, 0.55, "MP L1 = "+str(MP_l1)+"#pm"+str(MPe_l1))
    lb.DrawLatex(0.5, 0.50, "MP L2 = "+str(MP_l2)+"#pm"+str(MPe_l2))
    lb.DrawLatex(0.5, 0.45, "MP L3 = "+str(MP_l3)+"#pm"+str(MPe_l3))
    lb.DrawLatex(0.5, 0.40, "MP L4 = "+str(MP_l4)+"#pm"+str(MPe_l4))

leg.Draw()
gPad.RedrawAxis()
c.SaveAs(plotdir+"barrel_summary_"+var+"_"+fill"_.pdf"))
#c.Update()
#c.Clear()


c2 = TCanvas('c2', 'c2', 800, 640)
leg2 = TLegend(0.60,0.90,0.90, 0.70)
leg2.SetBorderSize(0)
leg2.SetFillColor(10)
leg2.SetLineColor(10)
leg2.SetLineWidth(0)

if var == "norm_charge":
    f_d1 = fitting(h_d1)
    f_d2 = fitting(h_d2)
    f_d3 = fitting(h_d3)
    
    MP_d1 = round(f_d1.GetParameter('MP'),3)
    MPe_d1 = round(f_d1.GetParError(1),3)
    MP_d2 = round(f_d2.GetParameter('MP'),3)
    MPe_d2 = round(f_d2.GetParError(1),3)
    MP_d3 = round(f_d3.GetParameter('MP'),3)
    MPe_d3 = round(f_d3.GetParError(1),3)
    
max_ye = max(h_d1.GetMaximum(), h_d2.GetMaximum(), h_d3.GetMaximum())

setHisto(h_d1, xTitle, "Clusters", kBlack,  'Disk 1', max_ye+max_ye*0.1, 1)
setHisto(h_d2, xTitle, "Clusters", kBlue,   'Disk 2', max_ye+max_ye*0.1, 1)
setHisto(h_d3, xTitle, "Clusters", kGreen,  'Disk 3', max_ye+max_ye*0.1, 1)

h_d1.Draw("hist")
h_d2.Draw("hist, same")
h_d3.Draw("hist, same")

le = TLatex()

if var == "norm_charge":
    f_d1.SetMaximum(max_ye+a)
    f_d2.SetMaximum(max_ye+a)
    f_d3.SetMaximum(max_ye+a)
    f_d1.Draw("lsame")
    f_d2.Draw("lsame")
    f_d3.Draw("lsame")
    le.SetNDC(kTRUE)
    le.SetTextSize(0.025)
    le.SetTextAlign(13)
    le.DrawLatex(0.5, 0.55, "MP D1 = "+str(MP_d1)+"#pm"+str(MPe_d1))
    le.DrawLatex(0.5, 0.50, "MP D2 = "+str(MP_d2)+"#pm"+str(MPe_d2))
    le.DrawLatex(0.5, 0.45, "MP D3 = "+str(MP_d3)+"#pm"+str(MPe_d3))
    

leg2.Draw()
gPad.RedrawAxis()
c2.SaveAs(plotdir+"endcap_summary_"+var+"_"+fill"_.pdf")


raw_input("hold")
