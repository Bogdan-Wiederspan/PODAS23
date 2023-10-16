import ROOT
from cms_style import CMS_lumi

key = "corrected" #"uncorrected"

#load MC
f1 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/ttbar.root","read") #ttbar
f2 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/peers/dytotautau.root","read") #DY tau tau
f3 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/dytomumu_high.root","read") #DY mu mu high
f4 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/peers/dytomumu_low.root","read") #DY mumu low

#load data
if key == "uncorrected":
    fdata = ROOT.TFile.Open("/nfs/dust/cms/group/cmsdas2023/gparaske/0D_rawData/getDimuonSpectrum/Run2018.root","read")
else:
    fdata = ROOT.TFile.Open("/nfs/dust/cms/group/cmsdas2023/pahwagne/work/corrected/input/data.root","read")

#ttbar
h1 = f1.dimuon
#h1.Scale(0.3) #only uncorrected
h1.GetYaxis().SetTitle('Events')
h1.GetXaxis().SetTitle('m(#mu#mu) [GeV]')
h1.SetFillColor(ROOT.kRed-2)
h1.SetLineWidth(0)

#DY->tautau pogdan
h2 = f2.dimuon
#h2.Scale(4/9) #only uncorrected
h2.GetYaxis().SetTitle('Events')
h2.GetXaxis().SetTitle('m(#mu#mu) [GeV]')
h2.SetFillColor(ROOT.kBlue-2)
h2.SetLineWidth(0)
#DY->MuMu (high)
h3 = f3.dimuon
h3.SetFillColor(ROOT.kCyan-1)
h3.SetLineWidth(0)
#DY->MuMu (low)
h4 = f4.dimuon
h4.SetFillColor(ROOT.kOrange-1)
h4.SetLineWidth(0)

#data
h_data = fdata.dimuon
h_data.GetYaxis().SetTitle('Events')
h_data.GetXaxis().SetTitle('m(#mu#mu) [GeV]')
h_data.SetFillColor(ROOT.kBlack)
h_data.SetLineColor(ROOT.kBlack)
h_data.SetMarkerColor(ROOT.kBlack)
h_data.SetMarkerStyle(8)	
h_data.SetMarkerSize(0.7)

#create stacked histo
hs = ROOT.THStack("hs","");
hs.Add(h1)
hs.Add(h2)
hs.Add(h3)
hs.Add(h4)

#legend
leg = ROOT.TLegend(.35,.72,.88,0.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.SetNColumns(1)
leg.AddEntry(h1,'t#bar{t} #rightarrow 2l 2#nu','F')
leg.AddEntry(h2,'DY #rightarrow #tau #tau','F')
leg.AddEntry(h3,'DY #rightarrow #mu#mu, m(#mu#mu) > 50 GeV ','F')
leg.AddEntry(h4,'DY #rightarrow #mu#mu, m(#mu#mu) < 50 GeV ','F')
leg.AddEntry(h_data,'Data','LEP')

#drawing
c1 = ROOT.TCanvas('', '', 700, 700)
c1.Draw()
c1.cd()
main_pad = ROOT.TPad('main_pad', '', 0., 0., 1. , 1.  )

main_pad.Draw()
main_pad.cd()
main_pad.DrawFrame(30,10,3000,h_data.GetMaximum()*1.5,";m(#mu#mu) (GeV);Events")

"""
ratio_pad = ROOT.TPad('ratio_pad', '', 0., 0., 1., 0.25)
ratio_pad.Draw()
main_pad.SetTicks(True)
main_pad.SetBottomMargin(0.)
main_pad.SetLeftMargin(.16)
ratio_pad.SetTopMargin(0.)   
ratio_pad.SetLeftMargin(.16)
ratio_pad.SetGridy()
ratio_pad.SetBottomMargin(0.45)
"""

ROOT.gPad.SetLogx()
ROOT.gPad.SetLogy()

hs.Draw("HIST SAME")
h_data.Draw("SAME")
leg.Draw("SAME")
ROOT.gPad.RedrawAxis()

#cms logo and style
CMS_lumi(main_pad, 4,0, cmsText = 'CMS', extraText = '   Work in Progress', lumi_13TeV = '60 fb^{-1}')
c1.SaveAs("dimuon.pdf")
