import ROOT
from ROOT import TFile, RDataFrame, TH1D, TCanvas, TGraph
from ROOT import gROOT
from array import array
import numpy as np

# this is to supress ROOT garbage collector for histograms
ROOT.TH1.AddDirectory(False)

def frame():

    ROOT.EnableImplicitMT(128)

    frame = RDataFrame("inclusive_jets", "/nfs/dust/cms/group/cmsdas2023/calexe/vectorPAG/DYJetsToMuMu_M-10to50_applyMClumi.root")

    histo = frame.Histo1D(ROOT.RDF.TH1DModel("event_weights", "event_weights", 100, 0, 100),"event.genWgts.v")

    outfile = ROOT.TFile.Open("histos.root","RECREATE")
    outfile.cd()

    histo.Write()
    outfile.Close()

frame ()
