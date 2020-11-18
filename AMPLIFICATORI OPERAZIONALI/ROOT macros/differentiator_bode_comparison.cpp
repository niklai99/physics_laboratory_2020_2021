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

double XMIN = 1.8;
double XMAX = 6.2;
double YMIN = -30;
double YMAX = 25;

double RESXMIN = XMIN;
double RESXMAX = XMAX;
double RESYMIN = -0.55;
double RESYMAX = 0.55;

const double NPAR = 2;

TCanvas* c1;

vector<double> x, y, errX, errY;
vector<double> log10x, T;

TGraphErrors *plot;
TGraphErrors *residuals_lin;
TGraphErrors *residuals_par;
TGraph *sim;
TMultiGraph* mg;
TMultiGraph* residuals;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);
void readData(vector<double>&, vector<double>&, const string);

TGraphErrors *make_plot(vector<double>&, vector<double>&, vector<double>&, vector<double>&);
TGraph *make_plot(vector<double>&, vector<double>&);

TGraphErrors *make_lin_res(TGraphErrors*, vector<double>&, vector<double>&, vector<double>&, vector<double>&);
TGraphErrors *make_par_res(TGraphErrors*, vector<double>&, vector<double>&, vector<double>&, vector<double>&);

void settings_res(TMultiGraph*, const double, const double, const double, const double);
void settings_lin_res(TGraphErrors*, const double, const double, const double, const double);
void settings_par_res(TGraphErrors*, const double, const double, const double, const double);

void linee_res(const double, const double);

void settings_fit(TGraphErrors*, const double, const double, const double, const double);
void settings_fit(TGraph*, const double, const double, const double, const double);
void settings_fit(TMultiGraph*, const double, const double, const double, const double);

TFitResultPtr lin_fit(TGraphErrors*, const double, const double);
double lin_model(double*, double*);

TFitResultPtr par_fit(TGraphErrors*, const double, const double);
double par_model(double*, double*);

TMultiGraph *make_mg(TGraphErrors*, TGraph*);

void settings_global();

void make_legend(TF1*, TF1*);

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---------- MAIN ----------*/

void differentiator_bode_comparison() {

    c1 = new TCanvas("canvas1", "Fit", 1080, 720);
    c1->Divide(2, 0);
    c1->cd(1);
    gPad->SetPad( 0.01, 0.30, 0.99, 0.99);

    readData(x, y, errX, errY, FILE_NAME);
    readData(log10x, T, OUT_FILE);

    plot = make_plot(x, y, errX, errY);
    sim = make_plot(log10x, T);

    TFitResultPtr fit_lineare = lin_fit(plot, XMIN, XMAX);
    TFitResultPtr fit_parabolico = par_fit(plot, XMIN, XMAX);


    settings_fit(plot, XMIN, XMAX, YMIN, YMAX);
    settings_fit(sim, XMIN, XMAX, YMIN, YMAX);

    mg = make_mg(plot, sim); 
    mg->SetTitle("Differentiator - Bode Plot;; H (dB)");
    mg->Draw("AP");

    settings_fit(mg, XMIN, XMAX, YMIN, YMAX);
    settings_global();

    make_legend(plot->GetFunction("lin_model"), plot->GetFunction("par_model"));

    c1->cd(2);
    gPad->SetPad( 0.01, 0.01, 0.99, 0.30);

    residuals_lin = make_lin_res(plot, x, y, errX, errY);
    residuals_par = make_par_res(plot, x, y, errX, errY);
    settings_lin_res(residuals_lin, RESXMIN, RESXMAX, RESYMIN, RESYMAX);
    settings_par_res(residuals_par, RESXMIN, RESXMAX, RESYMIN, RESYMAX);

    residuals = make_mg(residuals_lin, residuals_par);
    residuals->Draw("AP");
    linee_res(RESXMIN, RESXMAX); 

    settings_res(residuals, RESXMIN, RESXMAX, RESYMIN, RESYMAX);

    

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
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1.5);

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
    graph-> SetLineColor(kMagenta + 2);
    graph-> SetMarkerStyle(25);
    graph-> SetMarkerColor(kMagenta + 2);
    graph-> SetMarkerSize(1.5);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    
}

void settings_fit(TMultiGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);

    graph->GetYaxis()->SetTitleOffset(0.50);
    graph->GetYaxis()->SetTitleSize(0.05);
    graph->GetXaxis()->SetLabelSize(0.05);
    graph->GetYaxis()->SetLabelSize(0.05);
    
}

TMultiGraph *make_mg(TGraphErrors* plot, TGraph* sim) {

    TMultiGraph* multi = new TMultiGraph();

    multi -> Add(sim);
    multi -> Add(plot);
  
    return multi;
}

void make_legend(TF1* f1, TF1* f2) {

    TLegend *leg = new TLegend(0.15, 0.6, 0.35, 0.85);

    leg->AddEntry(plot, "Acquired Measures   ", "pe");
    leg->AddEntry(sim, "Simulated Points   ", "p");
    leg->AddEntry(f1, "Linear Fit   ", "l");
    leg->AddEntry(f2, "Parabolic Fit   ", "l");

    leg->Draw();

    return;
}

TGraphErrors* make_lin_res(TGraphErrors* graph, vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {

    //creo vector per i residui
    vector<double> res;

    //calcolo i residui
    for (int i = 0; i < x.size(); i++) {
		res.push_back(y[i] - graph->GetFunction("lin_model")->Eval(x[i]));
    }

    //creo il grafico dei residui
    TGraphErrors* res_plot = new TGraphErrors(x.size(), &x[0], &res[0], &errX[0], &errY[0]);

    //plot grafico residui
    //res_plot->Draw("AP"); 

    return res_plot;
}

TGraphErrors* make_par_res(TGraphErrors* graph, vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {

    //creo vector per i residui
    vector<double> res;

    //calcolo i residui
    for (int i = 0; i < x.size() - 2; i++) {
		res.push_back(y[i] - graph->GetFunction("par_model")->Eval(x[i]));
    }


    //creo il grafico dei residui
    TGraphErrors* res_plot = new TGraphErrors(x.size() - 2, &x[0], &res[0], &errX[0], &errY[0]);

    return res_plot;
}

double lin_model(double* x, double* par){   
    double a = par[0];
    double b = par[1];

    double fit_function = 0;

    fit_function = (a * x[0] + b);

    return fit_function;
}

double par_model(double* x, double* par){   
    double a = par[0];
    double b = par[1];
    double c = par[2];

    double fit_function = 0;

    fit_function = (a * pow(x[0], 2) + b * x[0] + c);

    return fit_function;
}

TFitResultPtr lin_fit(TGraphErrors* graph, const double XMIN, const double XMAX) {

    //creo la funzione di root
    TF1* f1 = new TF1("lin_model", lin_model, XMIN, 4.1, NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kOrange + 10);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("lin_model", "RS+");
    fit_result->Print("V");

    return fit_result;
}

TFitResultPtr par_fit(TGraphErrors* graph, const double XMIN, const double XMAX) {

    //creo la funzione di root
    TF1* f1 = new TF1("par_model", par_model, 3.9, 5.5, NPAR+1);
    f1->SetParNames("a", "b", "c");
    f1->SetLineColor(kAzure + 10 );

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("par_model", "RS+");
    fit_result->Print("V");

    return fit_result;
}

void settings_res(TMultiGraph* graph, const double RESXMIN, const double RESXMAX, const double RESYMIN, const double RESYMAX) {

    graph->SetTitle(";log_{10}[f (Hz)];");

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(RESXMIN, RESXMAX);
    graph->SetMinimum(RESYMIN);
    graph->SetMaximum(RESYMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    graph->GetXaxis()->SetLabelSize(0.11);
    graph->GetYaxis()->SetLabelSize(0.11);
    graph->GetXaxis()->SetTitleSize(0.11);

    graph->GetYaxis()->SetNdivisions(505);
}

void settings_lin_res(TGraphErrors* graph, const double RESXMIN, const double RESXMAX, const double RESYMIN, const double RESYMAX) {

    //colori e cose 
    graph-> SetLineColor(kOrange + 10);
    graph-> SetLineWidth(2);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1.5);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(RESXMIN, RESXMAX);
    graph->SetMinimum(RESYMIN);
    graph->SetMaximum(RESYMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
}

void settings_par_res(TGraphErrors* graph, const double RESXMIN, const double RESXMAX, const double RESYMIN, const double RESYMAX) {

    //colori e cose 
    graph-> SetLineColor(kAzure + 10 );
    graph-> SetLineWidth(2);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1.5);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(RESXMIN, RESXMAX);
    graph->SetMinimum(RESYMIN);
    graph->SetMaximum(RESYMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
}

void linee_res(const double RESXMIN, const double RESXMAX) {    

    TLine *line = new TLine (RESXMIN, 0, RESXMAX, 0); 

    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();
}
/*-----------------------------------------------------------------------------EOF------------------------------------------------------------------------*/