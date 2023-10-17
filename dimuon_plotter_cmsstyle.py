import ROOT
from cms_style import CMS_lumi

photon = "true" #include photon corrections

if photon:
    f1 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/ttbar_v3.root","read") #ttbar
    f2 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/dytautau.root","read") #DY tau tau
    f3 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/dytomumu_high.root","read") #DY mu mu high
    f4 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/dytomumu_low.root","read") #DY mumu low
    f5 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/qcd_v1.root","read") #qcd
    # only available for photon correction
    f6 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/WW.root","read") #WW
    f7 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/ZZ.root","read") #ZZ
    f8 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/WZ.root","read") #WZ

#old :)
else:
    #load MC
    f1 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/peers/ttbar.root","read") #ttbar
    f2 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/peers/dytotautau.root","read") #DY tau tau
    f3 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/peers/dytomumu_high_new.root","read") #DY mu mu high
    f4 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/peers/dytomumu_low_new.root","read") #DY mumu low
    f5 = ROOT.TFile.Open(f"/nfs/dust/cms/group/cmsdas2023/pahwagne/work/{key}/input/peers/qcd.root","read") #qcd

#load data
if photon:
    fdata = ROOT.TFile.Open("/nfs/dust/cms/group/cmsdas2023/pahwagne/work/photon/data.root","read")

else:
    fdata = ROOT.TFile.Open("/nfs/dust/cms/group/cmsdas2023/pahwagne/work/corrected/input/data.root","read")

#old :)
#uncorrected data 
#fdata = ROOT.TFile.Open("/nfs/dust/cms/group/cmsdas2023/gparaske/0D_rawData/getDimuonSpectrum/Run2018.root","read")

files = [f1,f2,f3,f4,f5,f6,f7,f8]

def dimuon(files):
    hists = []
    for i,f in enumerate(files):
        h = f.dimuon
        h.SetFillColor(color[i])
        h.SetLineWidth(0)
        hists.append(h)


def drawing(name):

    leg = ROOT.TLegend(.6,.6,.88,0.88)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    leg.SetNColumns(1)
    leg.SetMargin(0.2)
    leg.AddEntry(h2,'DY #rightarrow #tau #tau','F')
    leg.AddEntry(h3,'DY #rightarrow #mu#mu','F')
    #leg.AddEntry(h4,'DY #rightarrow #mu#mu, m(#mu#mu) < 50 GeV ','F')
    leg.AddEntry(h1,'t#bar{t} #rightarrow 2l 2#nu','F')
    leg.AddEntry(h5,'QCD ','F')
    leg.AddEntry(h6,'WW ','F') #remark: very unlikely to have 4mu (as we require 2)  and very unlikely to have electrons (we filter: no electrons)
    leg.AddEntry(h7,'ZZ ','F')
    leg.AddEntry(h8,'WZ ','F')

    leg.AddEntry(h_data,'Data','EP')

    c1 = ROOT.TCanvas('', '', 700, 700)
    c1.Draw()
    c1.cd()
    main_pad = ROOT.TPad('main_pad', '', 0., 0., 1. , 1.  )

    main_pad.Draw()
    main_pad.cd()
    hframe = main_pad.DrawFrame(30,10,3000,h_data.GetMaximum()*1.5,";m_{#mu#mu} (GeV);Events")
    hframe.GetXaxis().SetMoreLogLabels()
    hframe.GetXaxis().SetNoExponent()

    ROOT.gPad.SetLogx()
    ROOT.gPad.SetLogy()

    hs.Draw("HIST SAME")
    h_data.Draw("SAME")
    leg.Draw("SAME")
    ROOT.gPad.RedrawAxis()

    #cms logo and style
    CMS_lumi(main_pad, 4,0, cmsText = 'CMS', extraText = '   Work in Progress', lumi_13TeV = '59.8 fb^{-1}')
    c1.SaveAs(f"{name}.pdf")
    
#ttbar
h1 = f1.dimuon
#h1.Scale(0.3) #only uncorrected
h1.SetFillColor(ROOT.kRed-2)
h1.SetLineWidth(0)
#DY->tautau pogdan
h2 = f2.dimuon
#h2.Scale(4/9) #only uncorrected
h2.SetFillColor(ROOT.kBlue-2)
h2.SetLineWidth(0)
#DY->MuMu (high)
h3 = f3.dimuon
h3.SetFillColor(ROOT.kCyan-1)
h3.SetLineWidth(0)
#DY->MuMu (low)
h4 = f4.dimuon
h4.SetFillColor(ROOT.kCyan-1)
h4.SetLineWidth(0)
#qcd
h5 = f5.dimuon
h5.SetFillColor(ROOT.kCyan)
h5.SetLineWidth(0)
#bosons
h6 = f6.dimuon
h6.SetFillColor(ROOT.kYellow)
h6.SetLineWidth(0)

h7 = f7.dimuon
h7.SetFillColor(ROOT.kPink)
h7.SetLineWidth(0)

h8 = f8.dimuon
h8.SetFillColor(ROOT.kGreen)
h8.SetLineWidth(0)

#data
h_data = fdata.dimuon
h_data.SetFillColor(ROOT.kBlack)
h_data.SetLineColor(ROOT.kBlack)
h_data.SetMarkerColor(ROOT.kBlack)
h_data.SetMarkerStyle(8)	
h_data.SetMarkerSize(0.7)

#create stacked histo
hs = ROOT.THStack("hs","");
hs.Add(h5)
hs.Add(h6)
hs.Add(h7)
hs.Add(h8)
hs.Add(h1)
hs.Add(h2)
hs.Add(h3)
hs.Add(h4)


if photon:
    drawing("dimuon_photon.pdf")
else:
    drawing("dimuon.pdf")

N_mumu = h_data.Integral() - h1.Integral() - h5.Integral() - h6.Integral() -h7.Integral() - h8.Integral()

#ttbar
h1 = f1.mumugamma
#h1.Scale(0.3) #only uncorrected
h1.SetFillColor(ROOT.kRed-2)
h1.SetLineWidth(0)

#DY->tautau pogdan
h2 = f2.mumugamma
#h2.Scale(4/9) #only uncorrected
h2.SetFillColor(ROOT.kBlue-2)
h2.SetLineWidth(0)
#DY->MuMu (high)
h3 = f3.mumugamma
h3.SetFillColor(ROOT.kCyan-1)
h3.SetLineWidth(0)
#DY->MuMu (low)
h4 = f4.mumugamma
h4.SetFillColor(ROOT.kCyan-1)
h4.SetLineWidth(0)
#DY->qcd
h5 = f5.mumugamma
h5.SetFillColor(ROOT.kCyan)
h5.SetLineWidth(0)
#boson
h6 = f6.mumugamma
h6.SetFillColor(ROOT.kYellow+2)
h6.SetLineWidth(0)

h7 = f7.mumugamma
h7.SetFillColor(ROOT.kPink)
h7.SetLineWidth(0)

h8 = f8.mumugamma
h8.SetFillColor(ROOT.kGreen)
h8.SetLineWidth(0)

#data
h_data = fdata.mumugamma
h_data.SetFillColor(ROOT.kBlack)
h_data.SetLineColor(ROOT.kBlack)
h_data.SetMarkerColor(ROOT.kBlack)
h_data.SetMarkerStyle(8)	
h_data.SetMarkerSize(0.7)

#create stacked histo
hs = ROOT.THStack("hs","");
hs.Add(h5)
hs.Add(h6)
hs.Add(h7)
hs.Add(h8)
hs.Add(h1)
hs.Add(h2)
hs.Add(h3)
hs.Add(h4)

drawing("mumugamma.pdf")
