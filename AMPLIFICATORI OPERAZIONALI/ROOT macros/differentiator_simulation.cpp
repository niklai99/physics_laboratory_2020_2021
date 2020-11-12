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

const string FILE_NAME = "../Data/Simulations/DIFF2.txt";
const string OUT_FILE = "../Data/Simulations/DIFF_OUT.txt";

double XMIN = 1;
double XMAX = 7;
double YMIN = -30;
double YMAX = 25;

double RESXMIN = XMIN;
double RESXMAX = XMAX;
double RESYMIN = -0.7;
double RESYMAX = 0.7;

TCanvas* c1;

vector<double> x, log10x;
vector<double> T;


TGraph *plot;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>&, vector<double>&, const string);

void arrangeData(vector<double>&, vector<double>&);

void writeData(vector<double>&, vector<double>&, const string);

TGraph *make_plot(vector<double>&, vector<double>&);

void settings_fit(TGraph*, const double, const double, const double, const double);

void settings_global();


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---------- MAIN ----------*/

void differentiator_simulation() {

    c1 = new TCanvas("canvas1", "Fit", 1080, 720);
    //c1->Divide(2, 0);

    readData(x, T, FILE_NAME);

    arrangeData(x, log10x);

    writeData(log10x, T, OUT_FILE);

    for (unsigned int i = 0; i < x.size(); i++)
    {
        cout << log10x[i] << '\t' << T[i] << '\n';
    }
    

    plot = make_plot(log10x, T);
    plot->Draw("AP");

    settings_fit(plot, XMIN, XMAX, YMIN, YMAX);

    settings_global();

    return;
}

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/
void readData(vector<double>& x, vector<double>& T, const string FILE_NAME) {

    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {

        x.push_back(i);   
        f >> i;
        T.push_back(i);    

    }

    f.close();
}

void arrangeData(vector<double>& x, vector<double>& log10x) {

    double tempx = 0;
    for(unsigned int j = 0; j < x.size(); j++) {

        tempx = log10(x[j]);
        log10x.push_back(tempx);

    }

    return;
}

void writeData(vector<double>& log10x, vector<double>& T, const string OUT_FILE) {

    ofstream myfile;
    myfile.open (OUT_FILE);
    
    for (unsigned int i = 0; i < log10x.size(); i++)
    {
        myfile << log10x[i] << '\t' << T[i] << '\n';
    }
    
    myfile.close();
    
    return;
}

TGraph* make_plot(vector<double>& x, vector<double>& y) {
    
    TGraph* graph = new TGraphErrors(x.size(), &x[0], &y[0]);

    return graph;
}


void settings_global() {

    TGaxis::SetMaxDigits(3);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
}

void settings_fit(TGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {
    //entro nel primo canvas


    //titolo e assi
    //graph-> SetTitle("OpAmp; V_{in} (V); V_{out} (V)");

    //stile e colore
    graph-> SetLineColor(kBlack);
    graph-> SetMarkerStyle(20);
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

/*-----------------------------------------------------------------------------EOF------------------------------------------------------------------------*/