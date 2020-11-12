using namespace std;

#include <fstream>
#include <cmath>
#include <vector>
#include <string>
#include <iostream>

#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TGraphErrors.h"


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>&, vector<double>&, const string);

TGraph *make_plot(vector<double>&, vector<double>&);

void settings_fit(TGraph*, const double, const double, const double, const double);

void settings_global();


/*-------- MAIN -------*/

void arduino_plot()
{   
    /*--- COSTANTI ---*/
    const string FILE_NAME = "./Data/calib_time_ROOT.dat";
    const double XMIN = 0;
    const double XMAX = 500;
    const double YMIN = 700;
    const double YMAX = 2100;

    /* --- ROOT OBJECTS ---*/
    TCanvas* c1 = nullptr;
    TGraph *plot = nullptr;

    /*--- DATA VECTORS ---*/
    vector<double> x, y;

    c1 = new TCanvas("canvas1", "ARDUINO PLOT", 1080, 720);

    readData(x, y, FILE_NAME);

    plot = make_plot(x, y);
    plot->Draw("AP");

    settings_fit(plot, XMIN, XMAX, YMIN, YMAX);

    settings_global();

   return;
}

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>& x, vector<double>& y, const string FILE_NAME) {

    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {

        x.push_back(i);   
        f >> i;
        y.push_back(i);    

    }

    f.close();

    return;
}

TGraph* make_plot(vector<double>& x, vector<double>& y) {
    
    TGraph* graph = new TGraph(x.size(), &x[0], &y[0]);

    return graph;
}

void settings_global() {

    TGaxis::SetMaxDigits(4);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);

    return;
}

void settings_fit(TGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

    //titolo e assi
    graph-> SetTitle("Arduino Waveform Plot; ADC (a.u.); Signal (a.u.)");

    //stile e colore
    graph-> SetLineColor(kBlue+2);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlue+2);
    graph-> SetMarkerSize(0.75);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);

    return;
}