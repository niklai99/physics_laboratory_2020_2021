//*
// File: plot_osc.C
//
// Description: plot signal data acquired with Arduino Due internal ADC
//
// Author: Alberto Garfagnini
//
// Date: 20-Nov-2019
//*
#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TH2F.h"

#include <iostream>

using namespace std;

void plot_osc()
{
  // Setup graphics
  gROOT->SetStyle( "Plain" );
  gStyle->SetOptTitle(kFALSE);
  gStyle->SetOptStat(0);
  gStyle->SetTitleSize(0.0425, "y");
  gStyle->SetTitleSize(0.0425, "x");
  gStyle->SetLabelOffset(0.01,"x");
  gStyle->SetLabelOffset(0.005,"y");
  gStyle->SetTitleOffset(0.95,"y");
  gStyle->SetTitleOffset(1.3,"x");
}

void plot_spectrum(const string file_name="data_0_root.dat")
{
   TGraph *g = nullptr;
   TH2F * frame_1 = nullptr;

   g = new TGraph(file_name.c_str());
   g->SetMarkerColor(4);
   g->SetMarkerStyle(21);
   g->SetMarkerSize(0.75);

   TCanvas * c1 = new TCanvas("c1","Arduino waveform plot");
   gPad->SetTopMargin(0.01);
   gPad->SetBottomMargin(0.12);
   gPad->SetRightMargin(0.01);
   gPad->SetLeftMargin(0.12);

   frame_1  = new TH2F("frame_1", "", 10, -5., 2050, 10, 0., 4096.);
   frame_1->Draw();
   frame_1->GetXaxis()->SetTitle("ADC [a.u.]");
   frame_1->GetXaxis()->SetLabelSize(0.05);
   frame_1->GetYaxis()->SetTitle("time [a.u.]");
   g->Draw("psame");

}
