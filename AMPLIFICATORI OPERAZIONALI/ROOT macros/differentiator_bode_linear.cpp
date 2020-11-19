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

const string FILE_NAME = "../Data/data_diff_lin.txt";

double XMIN = 15000;
double XMAX = 27000;
double YMIN = 6;
double YMAX = 8.2;

double RESXMIN = XMIN;
double RESXMAX = XMAX;
double RESYMIN = -0.4;
double RESYMAX = 0.4;

const double NPAR = 2;

TCanvas* c1;

vector<double> x, y, errX, errY;

TGraphErrors *plot;
TGraphErrors *residuals_lin;

TLatex* text;
/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);

TGraphErrors *make_plot(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

TGraphErrors *make_lin_res(TGraphErrors*, vector<double>&, vector<double>&, vector<double>&, vector<double>&);

void settings_lin_res(TGraphErrors*, const double, const double, const double, const double);

void linee_res(const double, const double);

void settings_fit(TGraphErrors*, const double, const double, const double, const double);

TFitResultPtr lin_fit(TGraphErrors*, const double, const double);

double lin_model(double*, double*);

void settings_global();

void latex(TLatex*);

double err_posteriori(TFitResultPtr, vector<double>&, vector<double>& );

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---------- MAIN ----------*/

void differentiator_bode_linear() {

    c1 = new TCanvas("canvas1", "Fit", 1080, 720);
    c1->Divide(2, 0);
    c1->cd(1);

    readData(x, y, errX, errY, FILE_NAME);

    plot = make_plot(x, y, errX, errY);

    TFitResultPtr fit_lineare = lin_fit(plot, XMIN, XMAX);

    settings_fit(plot, XMIN, XMAX, YMIN, YMAX);

    plot->SetTitle("Differentiator - Linear Plot; f (Hz); H = V_{out} / V_{in}");

    plot->Draw("AP");

    settings_global();

    //make_legend(plot->GetFunction("lin_model"), plot->GetFunction("par_model"));

    c1->cd(2);

    residuals_lin = make_lin_res(plot, x, y, errX, errY);

    settings_lin_res(residuals_lin, RESXMIN, RESXMAX, RESYMIN, RESYMAX);

    residuals_lin->SetTitle("Residui; f (Hz); H = V_{out} / V_{in} - fit");

    residuals_lin->Draw("AP");

    linee_res(RESXMIN, RESXMAX); 

/*
    latex(text);

    double err_post = err_posteriori(fit_parabolico, x, y);
    cout << err_post << endl;
*/
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


TGraphErrors* make_plot(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(x.size(), &x[0], &y[0], &errX[0], &errY[0]);

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

double lin_model(double* x, double* par){   
    double a = par[0];
    double b = par[1];

    double fit_function = 0;

    fit_function = (a * x[0] + b);

    return fit_function;
}

TFitResultPtr lin_fit(TGraphErrors* graph, const double XMIN, const double XMAX) {

    //creo la funzione di root
    TF1* f1 = new TF1("lin_model", lin_model, XMIN, XMAX, NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("lin_model", "RS");
    fit_result->Print("V");

    return fit_result;
}


void settings_lin_res(TGraphErrors* graph, const double RESXMIN, const double RESXMAX, const double RESYMIN, const double RESYMAX) {

    //colori e cose 
    graph-> SetLineColor(kBlack);
    graph-> SetLineWidth(1);
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
    graph->GetYaxis()->SetTitleOffset(1.35);
}


void linee_res(const double RESXMIN, const double RESXMAX) {    

    TLine *line = new TLine (RESXMIN, 0, RESXMAX, 0); 

    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();
}

void latex (TLatex* text) {
    c1->cd(1);

    text = new TLatex(4, 0, "Fit Parameters");
    text->SetTextSize(0.07);
    text->Draw();

    text = new TLatex(3.3, -10, "#color[810]{a = -63.4 #pm 0.5 dB}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(3.3, -14, "#color[810]{b = 19.03 #pm 0.16 dB/dec}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(3.3, -18, "#color[810]{#chi^{2}/ndf = 2.4 / 1}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(3.3, -22, "#color[810]{#sigma_{post} = 0.3 dB}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(4.8, -7, "#color[870]{c = -9.93 #pm 0.02 dB/dec^{2}}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(4.8, -11, "#color[870]{d = 96.25 #pm 0.14 dB/dec}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(4.8, -15, "#color[870]{e = -213.3 #pm 0.4 dB}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(4.8, -19, "#color[870]{#chi^{2}/ndf = 0.9 / 22}");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(4.8, -23, "#color[870]{#sigma_{post} = 0.04 dB}");
    text->SetTextSize(0.05);
    text->Draw();



    return;
}

double err_posteriori(TFitResultPtr fit, vector<double>& x, vector<double>& y) {

    double err_post_squared = 0;

   
    const double a = fit->Parameter(0);
    const double b = fit->Parameter(1);
    const double c = fit->Parameter(2);
 
    for(unsigned int j = 4; j < x.size() - 2; j++) {
        err_post_squared += pow( (a * pow(x[j], 2) + b * x[j] + c) - y[j] , 2 ) / ( 22 );
    }

/*
    for(unsigned int j = 0; j < x.size(); j++) {
        err_post_squared += pow( cost - y[j] , 2 ) / ( x.size() - 2 );
    }
*/
    return sqrt(err_post_squared);
}
/*-----------------------------------------------------------------------------EOF------------------------------------------------------------------------*/