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



const double NPAR = 2;

const string FILE_NAME_max = "../Data/data_opamp_max_nooutliers.txt";
const string FILE_NAME_min = "../Data/data_opamp_min_err_nooutliers.txt";

TCanvas* c1;

//plot range del fit
const double XMIN_max = -0;
const double XMAX_max = 1.5;
const double YMIN_max = 0;
const double YMAX_max = 14;

//plot range dei residui
const double RESXMIN_max = XMIN_max;
const double RESXMAX_max = XMAX_max;
const double RESYMIN_max = -.55;
const double RESYMAX_max = .55;

//plot range del fit
const double XMIN_min = -1.5;
const double XMAX_min = 0;
const double YMIN_min = -14;
const double YMAX_min = 0;

//plot range dei residui
const double RESXMIN_min = XMIN_min;
const double RESXMAX_min = XMAX_min;
const double RESYMIN_min = -.55;
const double RESYMAX_min = .55;

//vector dei dati + errori
vector<double> x_max, y_max, errX_max, errY_max;
vector<double> x_min, y_min, errX_min, errY_min;

//il grafico del fit
TGraphErrors *plot_max;
TGraphErrors *plot_min;

//il grafico dei residui
TGraphErrors *residuals_max;
TGraphErrors *residuals_min;

void readData(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);

double myfit(double*, double*);

TGraphErrors *plot_fit(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

TGraphErrors *res(TGraphErrors*, vector<double>&, vector<double>&, vector<double>&, vector<double>&);

TFitResultPtr fit_fun(TGraphErrors*, const double, const double);

void settings_fit(TGraphErrors*, const double, const double, const double, const double);

void settings_res(TGraphErrors*, const double, const double, const double, const double);

void linee_res(const double, const double);

void settings_global();



void opamp_max_and_min_plot_res() {
    c1 = new TCanvas("canvas1", "Fit", 1080, 720);
    c1->Divide(2, 2);

    readData(x_max, y_max, errX_max, errY_max, FILE_NAME_max);
    readData(x_min, y_min, errX_min, errY_min, FILE_NAME_min);

 
    plot_max = plot_fit(x_max, y_max, errX_max, errY_max);
    plot_min = plot_fit(x_min, y_min, errX_min, errY_min);

    c1->cd(1);
    TFitResultPtr fit_max = fit_fun(plot_max, XMIN_max, XMAX_max);
    c1->cd(3);
    TFitResultPtr fit_min = fit_fun(plot_min, XMIN_min, XMAX_min);

    c1->cd(2);
	residuals_max = res(plot_max, x_max, y_max, errX_max, errY_max);
    c1->cd(4);
    residuals_min = res(plot_min, x_min, y_min, errX_min, errY_min);

    c1->cd(1);
    settings_fit(plot_max, XMIN_max, XMAX_max, YMIN_max, YMAX_max);
    c1->cd(3);
    settings_fit(plot_min, XMIN_min, XMAX_min, YMIN_min, YMAX_min);

    //personalizzo il grafico residui
    c1->cd(2);
    linee_res(RESXMIN_max, RESXMAX_max);    
    settings_res(residuals_max, RESXMIN_max, RESXMAX_max, RESYMIN_max, RESYMAX_max);

    c1->cd(4);
    settings_res(residuals_min, RESXMIN_min, RESXMAX_min, RESYMIN_min, RESYMAX_min);
    linee_res(RESXMIN_min, RESXMAX_min);

    //personalizzo in modo globale i grafici
    settings_global();


    return;
}

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

//creo il grafico con errori
TGraphErrors* plot_fit(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(x.size(), &x[0], &y[0], &errX[0], &errY[0]);

    return graph;
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
    TF1* f1 = new TF1("myfit", myfit, XMIN, XMAX, NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("myfit", "S");
    fit_result->Print("V");
    //disegno il grafico
    graph->Draw("AP");

    return fit_result;
}

TGraphErrors* res(TGraphErrors* graph, vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {

    //creo vector per i residui
    vector<double> res;

    //calcolo i residui
    for (int i = 0; i < x.size(); i++) {
		res.push_back(y[i] - graph->GetFunction("myfit")->Eval(x[i]));
    }

    //creo il grafico dei residui
    TGraphErrors* res_plot = new TGraphErrors(x.size(), &x[0], &res[0], &errX[0], &errY[0]);

    //plot grafico residui
    res_plot->Draw("AP"); 

    return res_plot;
}

//personalizzazione globale dei grafici
void settings_global() {
    //imposto massimo tre cifre prima di usare la notazione scientifica
    TGaxis::SetMaxDigits(3);
    //le tick labels hanno lo stesso numero di cifre significative
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
}

void linee_res(const double RESXMIN, const double RESXMAX) {    

    //creo la linea
    TLine *line = new TLine (RESXMIN, 0, RESXMAX, 0); //linea orizzontale sullo zero 

    //personalizzazione
    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();
}

void settings_res(TGraphErrors* graph, const double RESXMIN, const double RESXMAX, const double RESYMIN, const double RESYMAX) {

    //titolo e assi 
    graph-> SetTitle("Residui; V_{in} (V); V_{out} - fit (V)");

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
}

void settings_fit(TGraphErrors* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {
    //entro nel primo canvas
    c1->cd(1);

    //titolo e assi
    graph-> SetTitle("OpAmp; V_{in} (V); V_{out} (V)");

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