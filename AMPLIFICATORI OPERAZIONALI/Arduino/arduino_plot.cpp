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

void sampling_rate(vector<double>&, vector<double>&, vector<double>&, const double);


/*-------- MAIN -------*/

void arduino_plot()
{   
    /*--- COSTANTI ---*/
    const string FILE_NAME = "./Data/calib_time_ROOT.dat";
    const double XMIN = 0;
    const double XMAX = 2000;
    const double YMIN = 700;
    const double YMAX = 2100;
    const double DER_YMIN = -600;
    const double DER_YMAX = 600;
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
    vector<double> x_results, y_results;
    vector<double> n_points, sampling_rates;

    /*--- CANVAS ---*/
    c1 = new TCanvas("canvas1", "ARDUINO PLOT", 1080, 720);
    c1->Divide(0, 2);

    /*--- READING DATA FROM FILE ---*/
    read_data(x, y, FILE_NAME);

    /*--- UPPER PLOT - WAVEFORM ---*/
    plot = make_plot(x, y);
    plot-> SetTitle("Arduino Waveform Plot; time (a.u.); ADC (a.u.)");
    c1->cd(1);
    plot->Draw("AP");

    settings_plot(plot, XMIN, XMAX, YMIN, YMAX);

    /*--- NUMERIC DERIVATIVE OF THE WAVEFORM ---*/
    compute_derivative(x, y, x_deriv, y_deriv);

    /*--- LOWER PLOT - DERIVATIVE ---*/
    der = make_plot(x_deriv, y_deriv);
    der-> SetTitle("Arduino Derivative Plot; time (a.u.); Derivative (a.u.)");
    c1->cd(2);
    der->Draw("AP");

    settings_plot(der, XMIN, XMAX, DER_YMIN, DER_YMAX);

    /*--- SEEKING DERIVATIVE PEEKS ---*/
    seek_values(x_deriv, y_deriv, x_results, y_results, THRESHOLD);

    /*--- PRINT RELEVANT PEEKS ---*/
    print_results(x_results, y_results);

    /*--- COMPUTE SAMPLING RATE ---*/
    sampling_rate(x_results, n_points, sampling_rates, PERIODO);

    /*--- GLOBAL PLOT SETTINGS ---*/
    settings_global();

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

void seek_values(vector<double>& x_deriv, vector<double>& y_deriv, vector<double>& x_results, vector<double>& y_results, const double THRESHOLD) {

    for (unsigned int i = 0; i < y_deriv.size(); i++)
    {
        if ( y_deriv[i] > THRESHOLD )
        {
            x_results.push_back(x_deriv[i]);
            y_results.push_back(y_deriv[i]);
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

void sampling_rate(vector<double>& x_results, vector<double>& n_points, vector<double>& sampling_rates, const double PERIODO) {

    double temp = 0;

    for (unsigned int i = 0; i < x_results.size()-1; i++)
    {
        temp = x_results[i+1] - x_results[i];
        n_points.push_back(temp);
        sampling_rates.push_back(n_points[i] / PERIODO);
        cout << '\n' << "Sampling Rate:\t" << sampling_rates[i] << '\n';
    }
    
    return;
}
