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

const double NPAR = 2;

const string FILE_NAME = "../Data/data_differentiator_bode.txt";

double XMIN = 1;
double XMAX = 7;
double YMIN = -30;
double YMAX = 25;

double RESXMIN = XMIN;
double RESXMAX = XMAX;
double RESYMIN = -0.7;
double RESYMAX = 0.7;

TCanvas* c1;
TLatex* text;

double err_post;

vector<double> x, y, errX, errY;

TGraphErrors *plot;
TGraphErrors *residuals;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);

double myfit(double*, double*);

TGraphErrors *make_plot(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

TGraphErrors *make_res(TGraphErrors*, vector<double>&, vector<double>&, vector<double>&, vector<double>&);

TFitResultPtr fit_fun(TGraphErrors*, const double, const double);

void settings_fit(TGraphErrors*, const double, const double, const double, const double);

void settings_res(TGraphErrors*, const double, const double, const double, const double);

void linee_res(const double, const double);

void settings_global();

double err_posteriori(TFitResultPtr, vector<double>&, vector<double>&);

void latex(TLatex*);

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---------- MAIN ----------*/

void differentiator_bode() {

    c1 = new TCanvas("canvas1", "Fit", 1080, 720);
    c1->Divide(2, 0);

    readData(x, y, errX, errY, FILE_NAME);

    plot = make_plot(x, y, errX, errY);

    c1->cd(1);
    TFitResultPtr fit = fit_fun(plot, XMIN, XMAX);
    settings_fit(plot, XMIN, XMAX, YMIN, YMAX);

    c1->cd(2);
	residuals = make_res(plot, x, y, errX, errY);
    linee_res(RESXMIN, RESXMAX);    
    settings_res(residuals, RESXMIN, RESXMAX, RESYMIN, RESYMAX);

    settings_global();

    err_post = err_posteriori(fit, x, y);
    cout << err_post << endl;


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

    //x.erase(x.begin());
    //y.erase(y.begin());
    //errX.erase(errX.begin());
    //errY.erase(errY.begin());



    f.close();
}

TGraphErrors* make_plot(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(x.size(), &x[0], &y[0], &errX[0], &errY[0]);

    return graph;
}

double myfit(double* x, double* par){   
    double a = par[0];
    double b = par[1];

    double fit_function = 0;

    fit_function = (a * x[0] + b);
    //fit_function = a;

    return fit_function;
}

TFitResultPtr fit_fun(TGraphErrors* graph, const double XMIN, const double XMAX) {

    //creo la funzione di root
    TF1* f1 = new TF1("myfit", myfit, XMIN, 4.2, NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("myfit", "RS");
    fit_result->Print("V");

    //std::cout << f1->GetProb() << std::endl;
    //disegno il grafico
    graph->Draw("AP");

    return fit_result;
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

    //plot grafico residui
    res_plot->Draw("AP"); 

    return res_plot;
}

void settings_global() {

    TGaxis::SetMaxDigits(3);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
}

void linee_res(const double RESXMIN, const double RESXMAX) {    

    TLine *line = new TLine (RESXMIN, 0, RESXMAX, 0); 

    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();
}

void settings_res(TGraphErrors* graph, const double RESXMIN, const double RESXMAX, const double RESYMIN, const double RESYMAX) {

    //titolo e assi 
    //graph-> SetTitle("Residui; V_{in} (V); V_{out} - fit (V)");

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
    graph->GetYaxis()->SetTitleOffset(1.35);
}

void settings_fit(TGraphErrors* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {
    //entro nel primo canvas
    c1->cd(1);

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

double err_posteriori(TFitResultPtr fit, vector<double>& x, vector<double>& y) {

    double err_post_squared = 0;

   
    const double m = fit->Parameter(0);
    const double q = fit->Parameter(1);


    //const double cost = fit->Parameter(0);

    
    for(unsigned int j = 0; j < x.size(); j++) {
        err_post_squared += pow( q + ( m * x[j] ) - y[j] , 2 ) / ( x.size() - 2 );
    }

/*
    for(unsigned int j = 0; j < x.size(); j++) {
        err_post_squared += pow( cost - y[j] , 2 ) / ( x.size() - 2 );
    }
*/
    return sqrt(err_post_squared);
}

void latex_max(TLatex* text) {
    c1->cd(1);

    text = new TLatex(.4, 25, "Fit Function");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(.6, 23.5, "y = a + bx");
    text->SetTextSize(0.04);
    text->Draw();

    text = new TLatex(1.45, 11.5, "Fit Parameters");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(1.5, 9, "a = -0.13 #pm 0.06 V");
    text->SetTextSize(0.04);
    text->Draw();

    text = new TLatex(1.5, 7, "b = 10.09 #pm 0.11");
    text->SetTextSize(0.04);
    text->Draw();

    text = new TLatex(1.5, 5, "#chi^{2} = 0.12   NDF = 7");
    text->SetTextSize(0.04);
    text->Draw();

    text = new TLatex(1.5, 3, "#sigma_{post} = 0.06 V");
    text->SetTextSize(0.04);
    text->Draw();
    
}

void latex_min(TLatex* text) {
    c1->cd(3);

    text = new TLatex(-1.4, -2, "Fit Function");
    text->SetTextSize(0.06);
    text->Draw();

    text = new TLatex(-1.35, -3.5, "y = c + dx");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(-0.6, -8, "Fit Parameters");
    text->SetTextSize(0.06);
    text->Draw();

    text = new TLatex(-0.6, -9, "c = 0.07 #pm 0.04 V");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(-0.6, -10, "d = 10.16 #pm 0.14");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(-0.6, -11, "#chi^{2} = 0.67   NDF = 7");
    text->SetTextSize(0.05);
    text->Draw();

    text = new TLatex(-0.6, -12, "#sigma_{post} = 0.07");
    text->SetTextSize(0.05);
    text->Draw();
  
}

/*-----------------------------------------------------------------------------EOF------------------------------------------------------------------------*/