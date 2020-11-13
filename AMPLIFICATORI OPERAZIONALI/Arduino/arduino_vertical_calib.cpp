/*-------------------------------------- CODE BY NICOLO LAI --------------------------------------*/
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
void read_data(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);

TGraphErrors *make_plot(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

TMultiGraph *make_mg(TGraph*, TGraph*, TGraph*, TGraph*, TGraph*, TGraph*, TGraph*,
                    TGraph*, TGraph*, TGraph*, TGraph*);

void settings_plot(TGraphErrors*, const double, const double, const double, const double);

void settings_global();

void compute_derivative(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

void seek_values(vector<double>&, vector<double>&, vector<double>&, vector<double>&,
                 vector<double>&, vector<double>&, const double, const double);

void print_results(vector<double>&, vector<double>&);

double sampling_rate(vector<double>&, vector<double>&, vector<double>&, const double);

double max_value(vector<double>&);

void arrange_data(vector<double>&, double);

double myfit(double*, double*);

TFitResultPtr fit_fun(TGraphErrors*, const double, const double);


/*-------- MAIN -------*/

void arduino_vertical_calib()
{   
    /*--- COSTANTI ---*/
    const double NPAR = 2;
    const string FILE_NAME  = "./Data/arduino_linear_fit.txt";
    const string FILE_NAME1  = "./Data/0_2V_ROOT.dat";
    const string FILE_NAME2  = "./Data/0_5V_ROOT.dat";
    const string FILE_NAME3  = "./Data/1_0V_ROOT.dat";
    const string FILE_NAME4  = "./Data/1_5V_ROOT.dat";
    const string FILE_NAME5  = "./Data/1_8V_ROOT.dat";
    const string FILE_NAME6  = "./Data/2_0V_ROOT.dat";
    const string FILE_NAME7  = "./Data/2_1V_ROOT.dat";
    const string FILE_NAME8  = "./Data/2_2V_ROOT.dat";
    const string FILE_NAME9  = "./Data/2_3V_ROOT.dat";
    const string FILE_NAME10 = "./Data/2_4V_ROOT.dat";
    const string FILE_NAME11 = "./Data/2_5V_ROOT.dat";
    const double XMIN = 0;
    const double XMAX = 2000;
    const double YMIN = 500;
    const double YMAX = 4300;
    const double THRESHOLD_MAX1 = 90;
    const double THRESHOLD_MIN1 = -90;
    const double THRESHOLD_MAX2 = 200;
    const double THRESHOLD_MIN2 = -200;
    const double THRESHOLD_MAX3 = 400;
    const double THRESHOLD_MIN3 = -400;
    const double THRESHOLD_MAX4 = 700;
    const double THRESHOLD_MIN4 = -700;
    const double THRESHOLD_MAX5 = 800;
    const double THRESHOLD_MIN5 = -800;
    const double THRESHOLD_MAX6 = 900;
    const double THRESHOLD_MIN6 = -900;
    const double THRESHOLD_MAX7 = 900;
    const double THRESHOLD_MIN7 = -900;
    const double THRESHOLD_MAX8 = 1000;
    const double THRESHOLD_MIN8 = -1000;
    const double THRESHOLD_MAX9 = 1000;
    const double THRESHOLD_MIN9 = -1000;
    const double THRESHOLD_MAX10 = 1100;
    const double THRESHOLD_MIN10 = -1100;
    const double THRESHOLD_MAX11 = 1200;
    const double THRESHOLD_MIN11 = -1200;

    /* --- ROOT CANVASES ---*/
    TCanvas* c1 = nullptr;
    TCanvas* c2 = nullptr;
    TCanvas* c3 = nullptr;
    TCanvas* c4 = nullptr;
    TCanvas* c5 = nullptr;
    TCanvas* c6 = nullptr;
    TCanvas* c7 = nullptr;
    TCanvas* c8 = nullptr;
    TCanvas* c9 = nullptr;
    TCanvas* c10 = nullptr;
    TCanvas* c11 = nullptr;

    /* --- ROOT PLOTS ---*/
    TGraph *plot1 = nullptr;
    TGraph *plot2 = nullptr;
    TGraph *plot3 = nullptr;
    TGraph *plot4 = nullptr;
    TGraph *plot5 = nullptr;
    TGraph *plot6 = nullptr;
    TGraph *plot7 = nullptr;
    TGraph *plot8 = nullptr;
    TGraph *plot9 = nullptr;
    TGraph *plot10 = nullptr;
    TGraph *plot11 = nullptr;
    TMultiGraph *mg = nullptr;

    /*--- DATA VECTORS ---*/
    vector<double> x1, y1;
    vector<double> x2, y2;
    vector<double> x3, y3;
    vector<double> x4, y4;
    vector<double> x5, y5;
    vector<double> x6, y6;
    vector<double> x7, y7;
    vector<double> x8, y8;
    vector<double> x9, y9;
    vector<double> x10, y10;
    vector<double> x11, y11;
    vector<double> derx1, dery1;
    vector<double> derx2, dery2;
    vector<double> derx3, dery3;
    vector<double> derx4, dery4;
    vector<double> derx5, dery5;
    vector<double> derx6, dery6;
    vector<double> derx7, dery7;
    vector<double> derx8, dery8;
    vector<double> derx9, dery9;
    vector<double> derx10, dery10;
    vector<double> derx11, dery11;
    vector<double> x_results_max1, y_results_max1;
    vector<double> x_results_min1, y_results_min1;
    vector<double> x_results_max2, y_results_max2;
    vector<double> x_results_min2, y_results_min2;
    vector<double> x_results_max3, y_results_max3;
    vector<double> x_results_min3, y_results_min3;
    vector<double> x_results_max4, y_results_max4;
    vector<double> x_results_min4, y_results_min4;
    vector<double> x_results_max5, y_results_max5;
    vector<double> x_results_min5, y_results_min5;
    vector<double> x_results_max6, y_results_max6;
    vector<double> x_results_min6, y_results_min6;
    vector<double> x_results_max7, y_results_max7;
    vector<double> x_results_min7, y_results_min7;
    vector<double> x_results_max8, y_results_max8;
    vector<double> x_results_min8, y_results_min8;
    vector<double> x_results_max9, y_results_max9;
    vector<double> x_results_min9, y_results_min9;
    vector<double> x_results_max10, y_results_max10;
    vector<double> x_results_min10, y_results_min10;
    vector<double> x_results_max11, y_results_max11;
    vector<double> x_results_min11, y_results_min11;


    double max1;
    double max2;
    double max3;
    double max4;
    double max5;
    double max6;
    double max7;
    double max8;
    double max9;
    double max10;
    double max11;

    vector<double> max_vec;


    /*--- CANVAS ---*/
    //c1 = new TCanvas("canvas1", "ARDUINO PLOT", 1080, 720);
    //c1->Divide(3, 4);
/*
    c2 = new TCanvas("canvas2", "ARDUINO PLOT", 1080, 720);
    c3 = new TCanvas("canvas3", "ARDUINO PLOT", 1080, 720);
    c4 = new TCanvas("canvas4", "ARDUINO PLOT", 1080, 720);
    c5 = new TCanvas("canvas5", "ARDUINO PLOT", 1080, 720);
    c6 = new TCanvas("canvas6", "ARDUINO PLOT", 1080, 720);
    c7 = new TCanvas("canvas7", "ARDUINO PLOT", 1080, 720);
    c8 = new TCanvas("canvas8", "ARDUINO PLOT", 1080, 720);
    c9 = new TCanvas("canvas9", "ARDUINO PLOT", 1080, 720);
    c10 = new TCanvas("canvas10", "ARDUINO PLOT", 1080, 720);
    c11 = new TCanvas("canvas11", "ARDUINO PLOT", 1080, 720);
*/

    /*--- READING DATA FROM FILE ---*/

    read_data(x1, y1, FILE_NAME1);
    read_data(x2, y2, FILE_NAME2);
    read_data(x3, y3, FILE_NAME3);
    read_data(x4, y4, FILE_NAME4);
    read_data(x5, y5, FILE_NAME5);
    read_data(x6, y6, FILE_NAME6);
    read_data(x7, y7, FILE_NAME7);
    read_data(x8, y8, FILE_NAME8);
    read_data(x9, y9, FILE_NAME9);
    read_data(x10, y10, FILE_NAME10);
    read_data(x11, y11, FILE_NAME11);

/*

    compute_derivative(x1, y1, derx1, dery1);
    compute_derivative(x2, y2, derx2, dery2);
    compute_derivative(x3, y3, derx3, dery3);
    compute_derivative(x4, y4, derx4, dery4);
    compute_derivative(x5, y5, derx5, dery5);
    compute_derivative(x6, y6, derx6, dery6);
    compute_derivative(x7, y7, derx7, dery7);
    compute_derivative(x8, y8, derx8, dery8);
    compute_derivative(x9, y9, derx9, dery9);
    compute_derivative(x10, y10, derx10, dery10);
    compute_derivative(x11, y11, derx11, dery11);

    seek_values(derx1, dery1, x_results_max1, y_results_max1, x_results_min1, y_results_min1, THRESHOLD_MAX1, THRESHOLD_MIN1);
    seek_values(derx2, dery2, x_results_max2, y_results_max2, x_results_min2, y_results_min2, THRESHOLD_MAX2, THRESHOLD_MIN2);
    seek_values(derx3, dery3, x_results_max3, y_results_max3, x_results_min3, y_results_min3, THRESHOLD_MAX3, THRESHOLD_MIN3);
    seek_values(derx4, dery4, x_results_max4, y_results_max4, x_results_min4, y_results_min4, THRESHOLD_MAX4, THRESHOLD_MIN4);
    seek_values(derx5, dery5, x_results_max5, y_results_max5, x_results_min5, y_results_min5, THRESHOLD_MAX5, THRESHOLD_MIN5);
    seek_values(derx6, dery6, x_results_max6, y_results_max6, x_results_min6, y_results_min6, THRESHOLD_MAX6, THRESHOLD_MIN6);
    seek_values(derx7, dery7, x_results_max7, y_results_max7, x_results_min7, y_results_min7, THRESHOLD_MAX7, THRESHOLD_MIN7);
    seek_values(derx8, dery8, x_results_max8, y_results_max8, x_results_min8, y_results_min8, THRESHOLD_MAX8, THRESHOLD_MIN8);
    seek_values(derx9, dery9, x_results_max9, y_results_max9, x_results_min9, y_results_min9, THRESHOLD_MAX9, THRESHOLD_MIN9);
    seek_values(derx10, dery10, x_results_max10, y_results_max10, x_results_min10, y_results_min10, THRESHOLD_MAX10, THRESHOLD_MIN10);
    seek_values(derx11, dery11, x_results_max11, y_results_max11, x_results_min11, y_results_min11, THRESHOLD_MAX11, THRESHOLD_MIN11);
    
    
*/  


    /*--- MAKING PLOTS ---*/  
/*
    plot1 = make_plot(x1, y1);
    
    plot1-> SetLineColor(kBlue+2);
    plot1-> SetMarkerStyle(20);
    plot1-> SetMarkerColor(kBlue+2);
    plot1-> SetMarkerSize(0.75);
    plot1-> SetLineWidth(2);
    plot1-> SetTitle("Vgen 0.2 V; time (a.u.); ADC (a.u.)");

    //c1->cd();
    c1->cd(1);
    plot1->Draw("AL");
    settings_plot(plot1, XMIN, XMAX, YMIN, YMAX);

    plot2 = make_plot(x2, y2);

    plot2-> SetLineColor(kOrange+10);
    plot2-> SetMarkerStyle(20);
    plot2-> SetMarkerColor(kOrange+10);
    plot2-> SetMarkerSize(0.75);
    plot2-> SetLineWidth(2);
    plot2-> SetTitle("Vgen 0.5 V; time (a.u.); ADC (a.u.)");

    //c2->cd();
    c1->cd(2);
    plot2->Draw("AL");
    settings_plot(plot2, XMIN, XMAX, YMIN, YMAX);

    plot3 = make_plot(x3, y3);

    plot3-> SetLineColor(kGreen);
    plot3-> SetMarkerStyle(20);
    plot3-> SetMarkerColor(kGreen);
    plot3-> SetMarkerSize(0.75);
    plot3-> SetLineWidth(2);
    plot3-> SetTitle("Vgen 1.0 V; time (a.u.); ADC (a.u.)");

    //c3->cd();
    c1->cd(3);
    plot3->Draw("AL");
    settings_plot(plot3, XMIN, XMAX, YMIN, YMAX);

    plot4 = make_plot(x4, y4);

    plot4-> SetLineColor(kMagenta);
    plot4-> SetMarkerStyle(20);
    plot4-> SetMarkerColor(kMagenta);
    plot4-> SetMarkerSize(0.75);
    plot4-> SetLineWidth(2);
    plot4-> SetTitle("Vgen 1.5 V; time (a.u.); ADC (a.u.)");

    //c4->cd();
    c1->cd(4);
    plot4->Draw("AL");
    settings_plot(plot4, XMIN, XMAX, YMIN, YMAX);

    plot5 = make_plot(x5, y5);

    plot5-> SetLineColor(kTeal);
    plot5-> SetMarkerStyle(20);
    plot5-> SetMarkerColor(kTeal);
    plot5-> SetMarkerSize(0.75);
    plot5-> SetLineWidth(2);
    plot5-> SetTitle("Vgen 1.8 V; time (a.u.); ADC (a.u.)");

    //c5->cd();
    c1->cd(5);
    plot5->Draw("AL");
    settings_plot(plot5, XMIN, XMAX, YMIN, YMAX);

    plot6 = make_plot(x6, y6);

    plot6-> SetLineColor(kViolet+7);
    plot6-> SetMarkerStyle(20);
    plot6-> SetMarkerColor(kViolet+7);
    plot6-> SetMarkerSize(0.75);
    plot6-> SetLineWidth(2);
    plot6-> SetTitle("Vgen 2.0 V; time (a.u.); ADC (a.u.)");

    //c6->cd();
    c1->cd(6);
    plot6->Draw("AL");
    settings_plot(plot6, XMIN, XMAX, YMIN, YMAX);

    plot7 = make_plot(x7, y7);

    plot7-> SetLineColor(kAzure+7);
    plot7-> SetMarkerStyle(20);
    plot7-> SetMarkerColor(kAzure+7);
    plot7-> SetMarkerSize(0.75);
    plot7-> SetLineWidth(2);
    plot7-> SetTitle("Vgen 2.1 V; time (a.u.); ADC (a.u.)");

    //c7->cd();
    c1->cd(7);
    plot7->Draw("AL");
    settings_plot(plot7, XMIN, XMAX, YMIN, YMAX);

    plot8 = make_plot(x8, y8);

    plot8-> SetLineColor(kPink+5);
    plot8-> SetMarkerStyle(20);
    plot8-> SetMarkerColor(kPink+5);
    plot8-> SetMarkerSize(0.75);
    plot8-> SetLineWidth(2);
    plot8-> SetTitle("Vgen 2.2 V; time (a.u.); ADC (a.u.)");

    //c8->cd();
    c1->cd(8);
    plot8->Draw("AL");
    settings_plot(plot8, XMIN, XMAX, YMIN, YMAX);

    plot9 = make_plot(x9, y9);

    plot9-> SetLineColor(kGreen+3);
    plot9-> SetMarkerStyle(20);
    plot9-> SetMarkerColor(kGreen+3);
    plot9-> SetMarkerSize(0.75);
    plot9-> SetLineWidth(2);
    plot9-> SetTitle("Vgen 2.3 V; time (a.u.); ADC (a.u.)");

    //c9->cd();
    c1->cd(9);
    plot9->Draw("AL");
    settings_plot(plot9, XMIN, XMAX, YMIN, YMAX);

    plot10 = make_plot(x10, y10);

    plot10-> SetLineColor(kOrange);
    plot10-> SetMarkerStyle(20);
    plot10-> SetMarkerColor(kOrange);
    plot10-> SetMarkerSize(0.75);
    plot10-> SetLineWidth(2);
    plot10-> SetTitle("Vgen 2.4 V; time (a.u.); ADC (a.u.)");

    //c10->cd();
    c1->cd(10);
    plot10->Draw("AL");
    settings_plot(plot10, XMIN, XMAX, YMIN, YMAX);

    plot11 = make_plot(x11, y11);

    plot11-> SetLineColor(kPink);
    plot11-> SetMarkerStyle(20);
    plot11-> SetMarkerColor(kPink);
    plot11-> SetMarkerSize(0.75);
    plot11-> SetLineWidth(2);
    plot11-> SetTitle("Vgen 2.5 V; time (a.u.); ADC (a.u.)");

    //c11->cd();
    c1->cd(11);
    plot11->Draw("AL");
    settings_plot(plot11, XMIN, XMAX, YMIN, YMAX);
*/
    /*--- SAVING PLOTS ---*/
/*
    c1->SaveAs("./Plots/0_2V.png");
    c2->SaveAs("./Plots/0_5V.png");
    c3->SaveAs("./Plots/1_0V.png");
    c4->SaveAs("./Plots/1_5V.png");
    c5->SaveAs("./Plots/1_8V.png");
    c6->SaveAs("./Plots/2_0V.png");
    c7->SaveAs("./Plots/2_1V.png");
    c8->SaveAs("./Plots/2_2V.png");
    c9->SaveAs("./Plots/2_3V.png");
    c10->SaveAs("./Plots/2_4V.png");
    c11->SaveAs("./Plots/2_5V.png");
*/


/*
    max1 = max_value(y1);
    max2 = max_value(y2);
    max3 = max_value(y3);
    max4 = max_value(y4);
    max5 = max_value(y5);
    max6 = max_value(y6);
    max7 = max_value(y7);
    max8 = max_value(y8);
    max9 = max_value(y9);
    max10 = max_value(y10);
    max11 = max_value(y11);

    arrange_data(max_vec, max1);
    arrange_data(max_vec, max2);
    arrange_data(max_vec, max3);
    arrange_data(max_vec, max4);
    arrange_data(max_vec, max5);
    arrange_data(max_vec, max6);
    arrange_data(max_vec, max7);
    arrange_data(max_vec, max8);
    arrange_data(max_vec, max9);
    arrange_data(max_vec, max10);
    arrange_data(max_vec, max11);

    for (unsigned int i = 0; i < max_vec.size(); i++)
    {
        cout << "\nDataset:\t" << i+1 << '\n' << "Massimo:\t" << max_vec[i] << endl;
    }
 */
    

    /*--- MAKING PLOTS ---*/
/*
    plot1 = make_plot(x1, y1);
    
    plot1-> SetLineColor(kBlue+2);
    plot1-> SetMarkerStyle(20);
    plot1-> SetMarkerColor(kBlue+2);
    plot1-> SetMarkerSize(0.75);

    plot2 = make_plot(x2, y2);

    plot2-> SetLineColor(kOrange+10);
    plot2-> SetMarkerStyle(20);
    plot2-> SetMarkerColor(kOrange+10);
    plot2-> SetMarkerSize(0.75);

    plot3 = make_plot(x3, y3);

    plot3-> SetLineColor(kGreen);
    plot3-> SetMarkerStyle(20);
    plot3-> SetMarkerColor(kGreen);
    plot3-> SetMarkerSize(0.75);

    plot4 = make_plot(x4, y4);

    plot4-> SetLineColor(kMagenta);
    plot4-> SetMarkerStyle(20);
    plot4-> SetMarkerColor(kMagenta);
    plot4-> SetMarkerSize(0.75);

    plot5 = make_plot(x5, y5);

    plot5-> SetLineColor(kTeal);
    plot5-> SetMarkerStyle(20);
    plot5-> SetMarkerColor(kTeal);
    plot5-> SetMarkerSize(0.75);

    plot6 = make_plot(x6, y6);

    plot6-> SetLineColor(kViolet+7);
    plot6-> SetMarkerStyle(20);
    plot6-> SetMarkerColor(kViolet+7);
    plot6-> SetMarkerSize(0.75);

    plot7 = make_plot(x7, y7);

    plot7-> SetLineColor(kAzure+7);
    plot7-> SetMarkerStyle(20);
    plot7-> SetMarkerColor(kAzure+7);
    plot7-> SetMarkerSize(0.75);

    plot8 = make_plot(x8, y8);

    plot8-> SetLineColor(kPink+5);
    plot8-> SetMarkerStyle(20);
    plot8-> SetMarkerColor(kPink+5);
    plot8-> SetMarkerSize(0.75);

    plot9 = make_plot(x9, y9);

    plot9-> SetLineColor(kGreen+3);
    plot9-> SetMarkerStyle(20);
    plot9-> SetMarkerColor(kGreen+3);
    plot9-> SetMarkerSize(0.75);

    plot10 = make_plot(x10, y10);

    plot10-> SetLineColor(kOrange);
    plot10-> SetMarkerStyle(20);
    plot10-> SetMarkerColor(kOrange);
    plot10-> SetMarkerSize(0.75);

    plot11 = make_plot(x11, y11);

    plot11-> SetLineColor(kPink);
    plot11-> SetMarkerStyle(20);
    plot11-> SetMarkerColor(kPink);
    plot11-> SetMarkerSize(0.75);

    
    mg = make_mg(plot1, plot2, plot3, plot4, plot5, plot6, plot7, plot8, plot9, plot10, plot11);
    mg->Draw("AL");

    settings_plot(mg, XMIN, XMAX, YMIN, YMAX);
*/

    vector<double> x, y, errx, erry;
    read_data(x, y, errx, erry, FILE_NAME);

    TGraphErrors *plot = make_plot(x, y, errx, erry);
    plot->SetTitle("Arduino Calibration Fit; ADC (a.u.); V (V)");
    plot-> SetLineColor(kBlack);
    plot-> SetMarkerStyle(20);
    plot-> SetMarkerColor(kBlack);
    plot-> SetMarkerSize(1);
    TFitResultPtr fit = fit_fun(plot, 1000, 4050);

    settings_plot(plot, 700, 4300, 0, 2.7);

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

void read_data(vector<double>& x, vector<double>& y, vector<double>& errx, vector<double>& erry, const string FILE_NAME) {

    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {

        x.push_back(i);   
        f >> i;
        y.push_back(i);    
        f >> i;
        errx.push_back(i);   
        f >> i;
        erry.push_back(i); 
    }

    f.close();

    return;
}

TGraphErrors* make_plot(vector<double>& x, vector<double>& y, vector<double>& errx, vector<double>& erry) {
    
    TGraphErrors* graph = new TGraphErrors(x.size(), &x[0], &y[0], &errx[0], &erry[0]);

    return graph;
}

TMultiGraph* make_mg(TGraph* plot1, TGraph* plot2, TGraph* plot3, TGraph* plot4, TGraph* plot5, TGraph* plot6, TGraph* plot7,
                    TGraph* plot8, TGraph* plot9, TGraph* plot10, TGraph* plot11) {

    TMultiGraph* multi = new TMultiGraph();

    multi->Add(plot1);
    multi->Add(plot2);
    multi->Add(plot3);
    multi->Add(plot4);
    multi->Add(plot5);
    multi->Add(plot6);
    multi->Add(plot7);
    multi->Add(plot8);
    multi->Add(plot9);
    multi->Add(plot10);
    multi->Add(plot11);

    return multi;
}

void settings_global() {

    TGaxis::SetMaxDigits(4);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);

    return;
}

void settings_plot(TGraphErrors* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

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

void seek_values(vector<double>& x_deriv, vector<double>& y_deriv, vector<double>& x_results_max, vector<double>& y_results_max,
                 vector<double>& x_results_min, vector<double>& y_results_min, const double THRESHOLD_MAX, const double THRESHOLD_MIN) {

    for (unsigned int i = 0; i < y_deriv.size(); i++)
    {
        if ( y_deriv[i] > THRESHOLD_MAX )
        {
            x_results_max.push_back(x_deriv[i]);
            y_results_max.push_back(y_deriv[i]);
        }

        else if (  y_deriv[i] < THRESHOLD_MIN )
        {
            x_results_min.push_back(x_deriv[i]);
            y_results_min.push_back(y_deriv[i]);
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

double sampling_rate(vector<double>& x_results, vector<double>& n_points, vector<double>& sampling_rates, const double PERIODO) {

    double temp = 0;
    double mean = 0;

    for (unsigned int i = 0; i < x_results.size()-1; i++)
    {

        temp = x_results[i+1] - x_results[i];
        n_points.push_back(temp);
        sampling_rates.push_back(n_points[i] / PERIODO);
        cout << '\n' << "Sampling Rate:\t" << sampling_rates[i] << '\n';
        mean += sampling_rates[i];
    }

    mean = mean/sampling_rates.size();

    return mean;
}

double max_value(vector<double>& ADC) {

    double maxx = 0;

    for (unsigned int i = 0; i < ADC.size(); i++)
        if (ADC[i] > maxx)
            maxx = ADC[i];

    return maxx;
}

void arrange_data(vector<double>& max_vec, double maxx) {

    max_vec.push_back(maxx);

    return;
}

double myfit(double* x, double* par){   
    double a = par[0];
    double b = par[1];

    double fit_function = 0;

    fit_function = (a * x[0] + b);

    return fit_function;
}

TFitResultPtr fit_fun(TGraphErrors* graph, const double XMIN, const double XMAX) {

    //creo la funzione di root
    TF1* f1 = new TF1("myfit", myfit, XMIN, XMAX, 2);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("myfit", "S");
    fit_result->Print("V");

    std::cout << f1->GetProb() << std::endl;
    //disegno il grafico
    graph->Draw("AP");

    return fit_result;
}