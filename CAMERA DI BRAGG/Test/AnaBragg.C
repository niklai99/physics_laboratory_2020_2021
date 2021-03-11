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

#ifndef LABNUC
#define LABNUC
struct bragg_signal {
  short int s[128];
};
#endif

int AnaBragg(const char *filename, int intto=128, float blfix=13, int nsig=0) {

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

  // ANALIZZA EVENTO x EVENTO

  // altri parametri iniziali DA VERIFICARE ED EVENTUALMENTE MODIFICARE
  float thr_frac = 0.4; // soglia rispetto al vmax per il calcolo della larghezza
  int intfrom = 0;// regione di integrazione da 0 a intto
  if (intto>128) intto=128;
  int blfrom = 108, blto = 128; // regione per il calcolo della baseline


  float bl; // baseline evento x evento
  float integral; // integrale di carica
  float vmax; // massimo relativo alla bl
  float width; // larghezza temporale dei segnali


  char outfilename[200];
  strcpy(outfilename,"anabragg_");
  const char *cc=strrchr(filename,'/');
  if (cc) {cc++; strcat(outfilename,cc);}
  else strcat(outfilename,filename);

  TFile *fout=new TFile(outfilename,"RECREATE"); // output file

  TNtuple *nt=new TNtuple("nt","","ev:vmax:integral:width:baseline");

  int maxev=nev;
  if (nsig && nsig<nev) maxev=nsig;
  
  // LOOP SUGLI EVENTI
  for (int i=0; i<maxev; i++) {

    // recupera l'evento
    br->GetEntry(i);

    // inizializza a zero
    bl=0; 
    integral=0;
    vmax=0;				     
    width=0;

    // CALCOLO DELLA BASELINE
    for (int k=blfrom; k<blto; k++) 
      bl += signal.s[k]; bl /= (blto-blfrom);    

    
    // CALCOLO INTEGRALE E VMAX
    /*
      NOTA: se invece della baseline evento per evento tolgo la baseline fissa blfix viene molto meglio
            il grafico dell'integrale (=picchi molto meglio definiti)
            Why?
    */
    for (int j=intfrom; j<intto; j++) {

      if ( (signal.s[j] - bl) < 0 ) integral += 0;

      else if ( (signal.s[j] - bl) >= 0 )  integral += (signal.s[j] - bl);

      // integral += (signal.s[j] - blfix); 
 
      if ( (signal.s[j] - bl) > vmax ) vmax = (signal.s[j] - bl);

    }
    // PERCHE GARFA AGGIUNGE ROBA RANDOM ALL'INTEGRALE????
    // integral += gRandom->Rndm();

  
    // CALCOLO DELLA LARGHEZZA DEL SEGNALE A UNA CERTA PERCENTUALE DEL VMAX
    float hpc = 0.5; 
    float left, right;
    float height = vmax * hpc;

    int l = 0;

    while (signal.s[l] <= height)
    {
      left = l;
      l++;
    }

    while (signal.s[l] >= height)
    {
      right = l;
      l++;
    }
  
    width = (right - left) * 0.1;



    // Riempie la NTupla con i parametri calcolati per il dato evento
    nt->Fill(i,vmax,integral,width,bl);
  }
  std::cout << maxev << " events analyzed..." << std::endl;

  fout->Write();
  fout->Close();

  fin->Close();

  new TFile(outfilename); // riapre il file dei risultati

  return 0;
}
