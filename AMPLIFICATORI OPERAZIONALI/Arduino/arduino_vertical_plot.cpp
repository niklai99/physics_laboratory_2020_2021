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

void read_data(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);

TGraphErrors *make_plot(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

void settings_plot(TGraphErrors*, const double, const double, const double, const double);

void settings_global();

double myfit(double*, double*);

TFitResultPtr fit_fun(TGraphErrors*, const double, const double, const double);

TGraphErrors *make_res(TGraphErrors*, vector<double>&, vector<double>&, vector<double>&, vector<double>&);

void settings_res(TGraphErrors*, const double, const double, const double, const double);

void linee_res(const double, const double);

void latex(TLatex*);

/*-------- MAIN -------*/

void arduino_vertical_plot()
{   

    /*--- COSTANTI ---*/
    const double NPAR = 2;
    const string FILE_NAME  = "./Data/arduino_linear_fit.txt";
    const double XMIN = 700;
    const double XMAX = 4300;
    const double YMIN = 0.;
    const double YMAX = 2.7;
    const double RESXMIN = XMIN;
    const double RESXMAX = XMAX;
    const double RESYMIN = -.1;
    const double RESYMAX = .1;

    vector<double> x, y, errx, erry;

    TCanvas* c1;
    TLatex* text;
    TGraphErrors* plot;
    TGraphErrors* residuals;


    c1 = new TCanvas("canvas1", "Fit", 1080, 720);
    c1->Divide(2, 0);

    read_data(x, y, errx, erry, FILE_NAME);

    c1->cd(1);
    plot = make_plot(x, y, errx, erry);
    plot -> Draw("AP");

    TFitResultPtr fit = fit_fun(plot, XMIN, XMAX, NPAR);
    settings_plot(plot, XMIN, XMAX, YMIN, YMAX);

    c1->cd(2);
    residuals = make_res(plot, x, y, errx, erry);
    residuals -> Draw("AP");

    settings_res(residuals, RESXMIN, RESXMAX, RESYMIN, RESYMAX);
    linee_res(RESXMIN, RESXMAX); 

    settings_global();
/*
    for (unsigned int i = 0; i < 8; i++)
    {
        x.pop_back();
        y.pop_back();
        errx.pop_back();
        erry.pop_back();

        c1->cd(1);
        plot = make_plot(x, y, errx, erry);
        plot -> Draw("same p");

        TFitResultPtr fit = fit_fun(plot, XMIN, XMAX, NPAR);
        settings_plot(plot, XMIN, XMAX, YMIN, YMAX);

        c1->cd(2);
        residuals = make_res(plot, x, y, errx, erry);
        residuals -> Draw("same p");

        settings_res(residuals, RESXMIN, RESXMAX, RESYMIN, RESYMAX);


    }
    */
    c1->cd(1);
    latex(text);
    return;
}

/*-------- FUNCTIONS -------*/
void read_data(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY, const string FILE_NAME) {

    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {

        x.push_back(i);   
        f >> i;
        y.push_back(i);    
        f >> i;
        errX.push_back(i);     
        f >> i;
        errY.push_back(i);

    }

/*
    x.erase(x.begin());
    y.erase(y.begin());
    errX.erase(errX.begin());
    errY.erase(errY.begin());
*/
/*
    for (unsigned int i = 0; i < 7; i++)
    {
        x.pop_back();
        y.pop_back();
        errX.pop_back();
        errY.pop_back();
    }
*/   

    f.close();
}

TGraphErrors* make_plot(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(x.size(), &x[0], &y[0], &errX[0], &errY[0]);

    return graph;
}

TGraphErrors* make_res(TGraphErrors* graph, vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {

    //creo vector per i residui
    vector<double> res;

    //calcolo i residui
    for (int i = 0; i < x.size(); i++) {
		res.push_back(y[i] - graph->GetFunction("myfit")->Eval(x[i]));
    }

    //creo il grafico dei residui
    TGraphErrors* res_plot = new TGraphErrors(x.size(), &x[0], &res[0], &errX[0], &errY[0]);

    return res_plot;
}

void settings_plot(TGraphErrors* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

    //titolo e assi
    graph-> SetTitle("Arduino Calibration Fit; ADC (a.u.); V (V)");

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

    return;
}

void settings_res(TGraphErrors* graph, const double RESXMIN, const double RESXMAX, const double RESYMIN, const double RESYMAX) {

    //titolo e assi 
    graph-> SetTitle("Arduino Calibration Residuals; ADC (a.u.); V - fit (V)");

    //colori e cose 
    graph-> SetLineColor(kBlack);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(RESXMIN, RESXMAX);
    graph->SetMinimum(RESYMIN);
    graph->SetMaximum(RESYMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTitleOffset(1.5);

    return;
}

void linee_res(const double RESXMIN, const double RESXMAX) {    

    TLine *line = new TLine (RESXMIN, 0, RESXMAX, 0); 

    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();

    return;
}

TFitResultPtr fit_fun(TGraphErrors* graph, const double XMIN, const double XMAX, const double NPAR) {

    //creo la funzione di root
    TF1* f1 = new TF1("myfit", myfit, XMIN, XMAX, NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("myfit", "S");
    fit_result->Print("V");

    return fit_result;
}

double myfit(double* x, double* par){   
    double a = par[0];
    double b = par[1];

    double fit_function = 0;

    fit_function = (a * x[0] + b);
    //fit_function = a;

    return fit_function;
}

void settings_global() {

    TGaxis::SetMaxDigits(4);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
}

void latex(TLatex* text) {

    text = new TLatex(1200, 2.4, "Fit Function");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(1250, 2.2, "V = a + b ADC");
    text->SetTextSize(0.04);
    text->Draw();

    text = new TLatex(2500, 0.9, "Fit Parameters");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(2550, 0.7, "a = - 602 #pm 7 mV");
    text->SetTextSize(0.04);
    text->Draw();

    text = new TLatex(2550, 0.55, "b = 0.776 #pm 0.005 mV");
    text->SetTextSize(0.04);
    text->Draw();

    text = new TLatex(2550, 0.40, "#chi^{2} = 8.0   NDF = 9");
    text->SetTextSize(0.04);
    text->Draw();
   
    return;
}