//
#if !defined(__CINT__) || defined(__MAKECINT__)
#include <Riostream.h>
#include <stdlib.h>
#include <TROOT.h>
#include <TSystem.h>
#include "TNtuple.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TF1.h"
#endif

#ifndef LABNUC
#define LABNUC
struct bragg_signal {
  short int s[128];
};
#endif

int plotSignal(bragg_signal sig, int same) {

  float x[128]; for (int i=0; i<128; i++) x[i]=i*0.1;
  float y[128]; for (int i=0; i<128; i++) y[i]=sig.s[i];
  TGraph *g = new TGraph(128,x,y); // crea il grafico
  g->SetMarkerStyle(7); // imposta alcuni attributi
  g->SetLineColor(4);
  g->SetLineWidth(2);

  TCanvas *csig = (TCanvas*)gROOT->FindObject("csig"); // cerca l'oggetto "csig" (canvas)
  if (!csig) { 
    csig=new TCanvas("csig"); // se non c'e' la crea nuova
    csig->SetGridy();
    g->Draw("apl"); // disegna il grafico e anche il frame con gli assi
  }
  else { 
    csig->cd(); // se c'e' si posiziona sulla canvas "csig"
    if (same)
      g->Draw("pl"); // disegna nel frame esistente
    else {
      csig->Clear();
      g->Draw("apl"); // disegna in un nuovo frame
      gSystem->Sleep(200); // aspetta 200 ms
    }      
  }
  csig->Modified(); // aggiorna la canvas
  csig->Update();
  gSystem->ProcessEvents(); // aggiorna la grafica

  return 0;
}

int PlotSignals(char *filename, int plfrom=0, int plto=100, int same=1) {

  bragg_signal signal;

  TFile *fin=new TFile(filename);
  if (!fin->IsOpen()) {
    std::cout << "file not found! " << std::endl;
    return -1;
  }

  TTree *tree = (TTree*)fin->Get("bragg");
  if (!tree) {
    std::cout << "Bragg tree not found! " << std::endl;
    return -2;
  }

  TBranch *br = tree->GetBranch("signals");
  if (!br) {
    std::cout << "Signal branch not found! " << std::endl;
    return -3;
  }

  br->SetAddress(&signal);
  int nev = br->GetEntries();
  std::cout << "Number of events in file : " << nev << std::endl;

  for (int i=plfrom; i<plto; i++) {
    br->GetEntry(i);
    plotSignal(signal,same);  
  }
  
  return 0;
}
