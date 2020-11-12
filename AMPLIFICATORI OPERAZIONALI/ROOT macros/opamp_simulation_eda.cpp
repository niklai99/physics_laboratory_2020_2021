/*--------------------------------Code by Nicolò Lai--------------------------------*/

#include <fstream>
#include <cmath>
#include <vector>
#include <string>
#include <TGraph.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TH1D.h>
#include <TFitResult.h>
#include <TRandom.h>
#include <TStyle.h>

using namespace std;


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/


const string FILE_NAME = "../Data/Simulations/OPAMP.txt";
const string FILE_NAME_sat = "../Data/Simulations/OPAMP_sat.txt";

TCanvas* c1;
TLatex* text;

//plot range del fit
const double XMIN = 0.01;
const double XMAX = 0.013;
const double YMIN = -17;
const double YMAX = 17;

const int NPAR = 3;

//vector dei dati + errori
vector<double> t, Vin, Vout;
vector<double> t_sat, Vin_sat, Vout_sat;

//il grafico del fit
TGraph *plot_Vin;
TGraph *plot_Vout;
TGraph *plot_Vin_sat;
TGraph *plot_Vout_sat;

TMultiGraph *mg;

/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

void readData(vector<double>&, vector<double>&, vector<double>&, const string);

TGraph* make_graph(vector<double>&, vector<double>&);

TMultiGraph* make_mg(TGraph*, TGraph*, TGraph*, TGraph*);

void settings_plot(TGraph*, const double, const double, const double, const double);

void settings_mg(TMultiGraph*, const double, const double, const double, const double);

void settings_global();

void linee(const double, const double);

void legend();


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

void opamp_simulation_eda() {

    c1 = new TCanvas("c1", "Simulation", 1080, 720);

    readData(t, Vin, Vout, FILE_NAME);
    readData(t_sat, Vin_sat, Vout_sat, FILE_NAME_sat);

    plot_Vin = make_graph(t, Vin);
    plot_Vout = make_graph(t, Vout);
    plot_Vin_sat = make_graph(t_sat, Vin_sat);
    plot_Vout_sat = make_graph(t_sat, Vout_sat);

    mg = make_mg(plot_Vin, plot_Vout, plot_Vin_sat, plot_Vout_sat);

    plot_Vin-> SetLineColor(kBlue);
    plot_Vin-> SetLineWidth(2);
    plot_Vin-> SetMarkerStyle(20);
    plot_Vin-> SetMarkerColor(kBlue);
    plot_Vin-> SetMarkerSize(1);

    plot_Vout-> SetLineColor(kGreen+2);
    plot_Vout-> SetLineWidth(2);
    plot_Vout-> SetMarkerStyle(20);
    plot_Vout-> SetMarkerColor(kGreen+2);
    plot_Vout-> SetMarkerSize(1);

    plot_Vin_sat-> SetLineColor(kOrange+10);
    plot_Vin_sat-> SetLineWidth(2);
    plot_Vin_sat-> SetMarkerStyle(20);
    plot_Vin_sat-> SetMarkerColor(kOrange+10);
    plot_Vin_sat-> SetMarkerSize(1);

    plot_Vout_sat-> SetLineColor(kMagenta);
    plot_Vout_sat-> SetLineWidth(2);
    plot_Vout_sat-> SetMarkerStyle(20);
    plot_Vout_sat-> SetMarkerColor(kMagenta);
    plot_Vout_sat-> SetMarkerSize(1);

    mg->Draw("AL");

    mg->SetTitle("Spice Simulation; t (s); Voltage (V)");

    settings_plot(plot_Vin, XMIN, XMAX, YMIN, YMAX);
    settings_plot(plot_Vout, XMIN, XMAX, YMIN, YMAX);
    settings_plot(plot_Vin_sat, XMIN, XMAX, YMIN, YMAX);
    settings_plot(plot_Vout_sat, XMIN, XMAX, YMIN, YMAX);
    settings_mg(mg, XMIN, XMAX, YMIN, YMAX);

    settings_global();

    linee(XMIN, XMAX);
    legend();

    return;
}

void readData(vector<double>& t, vector<double>& Vin, vector<double>& Vout, const string FILE_NAME) {

    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {

        t.push_back(i);   
        f >> i;
        Vin.push_back(i);    
        f >> i;
        Vout.push_back(i);     

    }
    f.close();
}

TGraph* make_graph(vector<double>& x, vector<double>& y) {
    
    TGraph* graph = new TGraph(x.size(), &x[0], &y[0]);

    return graph;
}

TMultiGraph* make_mg(TGraph* gr1, TGraph* gr2, TGraph* gr3, TGraph* gr4) {

    TMultiGraph* multi = new TMultiGraph();
    multi->Add(gr1);
    multi->Add(gr2);
    multi->Add(gr3);
    multi->Add(gr4);

    return multi;
}

void settings_global() {

    TGaxis::SetMaxDigits(3);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
}

void settings_plot(TGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    
}

void settings_mg(TMultiGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX){

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    
}

void linee(const double RESXMIN, const double RESXMAX) {    

    TLine *line = new TLine (RESXMIN, 0, RESXMAX, 0); 

    line->SetLineStyle(1);
    line->SetLineColor(kBlack);

    line->Draw();

    line = new TLine (RESXMIN, 15, RESXMAX, 15); 

    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();

    line = new TLine (RESXMIN, -15, RESXMAX, -15); 

    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();

}

double myfit(double* x, double* par){   
    double A = par[0];
    double w = par[1];
    double p = par[2];

    double fit_function = 0;

    fit_function = A * sin(w * x[0] + p);

    return fit_function;
}

void legend() {
    TLegend *leg = new TLegend(0.7, 0.15, 0.85, 0.3);
    leg->AddEntry(plot_Vin, "V_{gen} = 1V : V_{in}  ", "pl");
    leg->AddEntry(plot_Vout, "V_{gen} = 1V : V_{out}  ", "pl");
    leg->AddEntry(plot_Vin_sat, "V_{gen} = 4V : V_{in}  ", "pl");
    leg->AddEntry(plot_Vout_sat, "V_{gen} = 4V : V_{out}  ", "pl");
    //leg->SetMargin(0.2);
    leg->Draw();
}














