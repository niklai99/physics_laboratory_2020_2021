using namespace std;

//C++ LIBRARIES
#include <fstream>
#include <cmath>
#include <vector>
#include <string>
#include <iostream>

//ROOT LIBRARIES
#include "TROOT.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TGraphErrors.h"


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void read_data(vector<double>&, vector<double>&, const string);

TGraph *make_plot(vector<double>&, vector<double>&);

void settings_plot(TGraph*, const double, const double, const double, const double);

void settings_global();

void compute_derivative(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

void seek_values(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const double);

void print_results(vector<double>&, vector<double>&);

double sampling_rate(vector<double>&, vector<double>&, const double);


/*-------- MAIN -------*/

void arduino_plot()
{   
    /*--- COSTANTI ---*/
    const string FILE_NAME = "./Data/calib_time_ROOT.dat";
    const double XMIN = 0;
    const double XMAX = 2050;
    const double YMIN = 700;
    const double YMAX = 2100;
    const double FREQ = 5000; //Hertz
    const double PERIODO = pow(FREQ, -1); //Secondi
    const double THRESHOLD = 450;

    /* --- ROOT OBJECTS ---*/
    TCanvas* c1 = nullptr;
    TGraph *plot = nullptr;
    TGraph *der = nullptr;

    /*--- DATA VECTORS ---*/
    vector<double> x, y;
    vector<double> x_deriv, y_deriv;
    vector<double> x_result, y_result;

    c1 = new TCanvas("canvas1", "ARDUINO PLOT", 1080, 720);
    c1->Divide(2, 0);

    read_data(x, y, FILE_NAME);

    plot = make_plot(x, y);
    c1->cd(1);
    plot->Draw("AP");

    settings_plot(plot, XMIN, XMAX, YMIN, YMAX);

    compute_derivative(x, y, x_deriv, y_deriv);

    der = make_plot(x_deriv, y_deriv);
    c1->cd(2);
    der->Draw("AP");

    settings_plot(der, XMIN, XMAX, 0, 600);

    seek_values(x_deriv, y_deriv, x_result, y_result, THRESHOLD);

    print_results(x_result, y_result);

    settings_global();

    //cout << "\nSampling Rate:\t" << sampling_rate(x, y, FREQ) << endl;

   return;
}

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void read_data(vector<double>& x, vector<double>& y, const string FILE_NAME) {

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

void settings_plot(TGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

    graph-> SetTitle("Arduino Waveform Plot; time (a.u.); ADC (a.u.)");

    graph-> SetLineColor(kBlue+2);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlue+2);
    graph-> SetMarkerSize(0.75);

    gPad->Modified();
    
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);

    return;
}

void compute_derivative(vector<double>& x, vector<double>& y, vector<double>& x_deriv, vector<double>& y_deriv) {

    double temp = 0;

    for (unsigned int i = 1; i < x.size()-1; i++)
    {
        temp = ( y[i+1] - y[i-1] ) / 2.;
        x_deriv.push_back(x[i-1]);
        y_deriv.push_back(temp);
    }
    
    return;
}

void seek_values(vector<double>& x_deriv, vector<double>& y_deriv, vector<double>& x_result, vector<double>& y_result, const double THRESHOLD) {

    for (unsigned int i = 0; i < y_deriv.size(); i++)
    {
        if ( y_deriv[i] > THRESHOLD )
        {
            x_result.push_back(x_deriv[i]);
            y_result.push_back(y_deriv[i]);
        }
        
    }
    
    return;
}

void print_results(vector<double>& x_results, vector<double>& y_results) {

    for (unsigned int i = 0; i < x_results.size(); i++)
    {
        cout << '\n' <<
        "Time:\t" << x_results[i] << '\n' <<
        "Deriv:\t" << y_results[i] << '\n';
    }

    return;
}

/*
double sampling_rate(vector<double>& x, vector<double>& y, const double FREQ) {

    double sampling = 0;

    double counter = 0;



    return sampling;
}
*/