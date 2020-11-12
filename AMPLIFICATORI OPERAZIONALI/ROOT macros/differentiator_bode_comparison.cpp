/*--------------------------------Code by Nicolò Lai--------------------------------*/

#include <fstream>
#include <cmath>
#include <vector>
#include <string>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TH1D.h>
#include <TFitResult.h>
#include <TRandom.h>
#include <TStyle.h>

using namespace std;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

const string FILE_NAME = "../Data/data_differentiator_bode.txt";
const string OUT_FILE = "../Data/Simulations/DIFF_OUT.txt";

double XMIN = 1;
double XMAX = 7;
double YMIN = -30;
double YMAX = 25;

TCanvas* c1;

vector<double> x, y, errX, errY;
vector<double> log10x, T;

TGraphErrors *plot;
TGraph *sim;
TMultiGraph* mg;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);
void readData(vector<double>&, vector<double>&, const string);

TGraphErrors *make_plot(vector<double>&, vector<double>&, vector<double>&, vector<double>&);
TGraph *make_plot(vector<double>&, vector<double>&);

void settings_fit(TGraphErrors*, const double, const double, const double, const double);
void settings_fit(TGraph*, const double, const double, const double, const double);

TMultiGraph *make_mg(TGraphErrors*, TGraph*);

void settings_global();

void make_legend();

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---------- MAIN ----------*/

void differentiator_bode_comparison() {

    c1 = new TCanvas("canvas1", "Fit", 1080, 720);

    readData(x, y, errX, errY, FILE_NAME);
    readData(log10x, T, OUT_FILE);

    plot = make_plot(x, y, errX, errY);
    sim = make_plot(log10x, T);

    settings_fit(plot, XMIN, XMAX, YMIN, YMAX);
    settings_fit(sim, XMIN, XMAX, YMIN, YMAX);

    mg = make_mg(plot, sim);
    mg->Draw("AP");

    settings_global();

    make_legend();

    return;
}

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/
void readData(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY, const string FILE_NAME) {

    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {

        x.push_back(i);   
        f >> i;
        y.push_back(i);    
        f >> i;
        errX.push_back(0);     
        f >> i;
        errY.push_back(i);

    }

    f.close();
}

void readData(vector<double>& log10x, vector<double>& T, const string OUT_FILE) {

    ifstream f;
    f.open(OUT_FILE);
    double i = 0;
    while(f >> i) {

        log10x.push_back(i);   
        f >> i;
        T.push_back(i);    

    }

    f.close();
}

TGraphErrors* make_plot(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(x.size(), &x[0], &y[0], &errX[0], &errY[0]);

    return graph;
}


TGraph* make_plot(vector<double>& log10x, vector<double>& T) {
    
    TGraph* graph = new TGraphErrors(log10x.size(), &log10x[0], &T[0]);

    return graph;
}

void settings_global() {

    TGaxis::SetMaxDigits(3);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
}

void settings_fit(TGraphErrors* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

    //stile e colore
    graph-> SetLineColor(kBlack);
    graph-> SetMarkerStyle(21);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    
}

void settings_fit(TGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

    //stile e colore
    graph-> SetLineColor(kRed);
    graph-> SetMarkerStyle(24);
    graph-> SetMarkerColor(kRed);
    graph-> SetMarkerSize(1);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    
}

TMultiGraph *make_mg(TGraphErrors* plot, TGraph* sim) {

    TMultiGraph* multi = new TMultiGraph();

    multi -> Add(sim);
    multi -> Add(plot);

    multi->SetTitle("Differentiator - Bode; log_{10}[f (Hz)]; T (dB)");
  
    return multi;
}

void make_legend() {

    TLegend *leg = new TLegend(0.7, 0.15, 0.85, 0.3);

    leg->AddEntry(plot, "Acquired Measures   ", "pl");
    leg->AddEntry(sim, "Simulated Points   ", "pl");

    leg->Draw();

    return;
}


/*-----------------------------------------------------------------------------EOF------------------------------------------------------------------------*/