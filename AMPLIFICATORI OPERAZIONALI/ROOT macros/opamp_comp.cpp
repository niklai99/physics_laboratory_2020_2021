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

const unsigned int NPAR = 1;

const string FILE_NAME = "../Data/data_opamp_comp.txt";

TCanvas* c1;
TLatex* text;

//plot range del fit
const double XMIN = 0;
const double XMAX = 6;
const double YMIN = 9.8;
const double YMAX = 10.35;


//vector dei dati + errori
vector<double> x, y, errX, errY;

vector<double> G1, G2, G3, G4, G5;
vector<double> errG1, errG2, errG3, errG4, errG5;

vector<double> x1, x2, x3, x4, x5;
vector<double> errx1, errx2, errx3, errx4, errx5;

//il grafico del fit
TGraphErrors *plot;
TGraphErrors *plot1;
TGraphErrors *plot2;
TGraphErrors *plot3;
TGraphErrors *plot4;
TGraphErrors *plot5;
TMultiGraph *mg;
TF1 *f;


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-------- FUNCTIONS -------*/

void readData(vector<double>&, vector<double>&, vector<double>&, vector<double>&, const string);

void arrange_data(vector<double>&, vector<double>&, vector<double>&, vector<double>&,
                    vector<double>&, vector<double>&, vector<double>&, vector<double>&,
                    vector<double>&, vector<double>&, vector<double>&, vector<double>&,
                    vector<double>&, vector<double>&, vector<double>&, vector<double>&,
                    vector<double>&, vector<double>&, vector<double>&, vector<double>&,
                    vector<double>&, vector<double>&, vector<double>&, vector<double>&);

double myfit(double*, double*);

TGraphErrors *make_graph(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

TMultiGraph* make_mg(TGraphErrors*, TGraphErrors*, TGraphErrors*, TGraphErrors*, TGraphErrors*);

void settings_fit(TMultiGraph*, const double, const double, const double, const double);

void settings_global();

void latex(TLatex*);

double myfit(double*, double*);

TF1* make_fit(TGraphErrors*, const double, const double, const unsigned int);


/*--------------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---------- MAIN ----------*/
void opamp_comp() {

    c1 = new TCanvas("canvas1", "Comp", 1080, 720);

    readData(x, y, errX, errY, FILE_NAME);

    vector<double> v(x.size(), 0);

    plot = make_graph(x, y, v, v);

    f = make_fit(plot, XMIN, XMAX, NPAR);

    arrange_data(x, y, errX, errY, x1, G1, errx1, errG1, x2, G2, errx2, errG2, 
                x3, G3, errx3, errG3, x4, G4, errx4, errG4, x5, G5, errx5, errG5);
 
    plot1 = make_graph(x1, G1, errx1, errG1);
    //stile e colore
    plot1-> SetLineColor(kMagenta+1);
    plot1-> SetMarkerStyle(20);
    plot1-> SetMarkerColor(kMagenta+1);
    plot1-> SetMarkerSize(1);

    plot2 = make_graph(x2, G2, errx2, errG2);
    //stile e colore
    plot2-> SetLineColor(kRed);
    plot2-> SetMarkerStyle(22);
    plot2-> SetMarkerColor(kRed);
    plot2-> SetMarkerSize(1);

    plot3 = make_graph(x3, G3, errx3, errG3);
    //stile e colore
    plot3-> SetLineColor(kBlue);
    plot3-> SetMarkerStyle(23);
    plot3-> SetMarkerColor(kBlue);
    plot3-> SetMarkerSize(1);

    plot4 = make_graph(x4, G4, errx4, errG4);
    //stile e colore
    plot4-> SetLineColor(kGreen+2);
    plot4-> SetMarkerStyle(21);
    plot4-> SetMarkerColor(kGreen+2);
    plot4-> SetMarkerSize(1);

    plot5 = make_graph(x5, G5, errx5, errG5);
    //stile e colore
    plot5-> SetLineColor(kOrange+10);
    plot5-> SetMarkerStyle(29);
    plot5-> SetMarkerColor(kOrange+10);
    plot5-> SetMarkerSize(1.5);


    mg = make_mg(plot1, plot2, plot3, plot4, plot5);

    mg->Draw("AP");

    f->Draw("SAME");

    settings_fit(mg, XMIN, XMAX, YMIN, YMAX);

    settings_global();

    latex(text);

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

    return;
}

void arrange_data(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY,
                    vector<double>& x1, vector<double>& G1, vector<double>& errx1, vector<double>& errG1,
                    vector<double>& x2, vector<double>& G2, vector<double>& errx2, vector<double>& errG2,
                    vector<double>& x3, vector<double>& G3, vector<double>& errx3, vector<double>& errG3,
                    vector<double>& x4, vector<double>& G4, vector<double>& errx4, vector<double>& errG4,
                    vector<double>& x5, vector<double>& G5, vector<double>& errx5, vector<double>& errG5){

    x1.push_back(x[0]);
    x2.push_back(x[1]);
    x3.push_back(x[2]);
    x4.push_back(x[3]);
    x5.push_back(x[4]);

    errx1.push_back(0);
    errx2.push_back(0);
    errx3.push_back(0);
    errx4.push_back(0);
    errx5.push_back(0);

    G1.push_back(y[0]);
    G2.push_back(y[1]);
    G3.push_back(y[2]);
    G4.push_back(y[3]);
    G5.push_back(y[4]);

    errG1.push_back(errY[0]);
    errG2.push_back(errY[1]);
    errG3.push_back(errY[2]);
    errG4.push_back(errY[3]);
    errG5.push_back(errY[4]);

    return;
}

TGraphErrors* make_graph(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(x.size(), &x[0], &y[0], &errX[0], &errY[0]);
    
    return graph;
}

TMultiGraph* make_mg(TGraphErrors* plot1, TGraphErrors* plot2, TGraphErrors* plot3, TGraphErrors* plot4, TGraphErrors* plot5) {
    
    TMultiGraph* multi = new TMultiGraph();

    multi->Add(plot1);
    multi->Add(plot2);
    multi->Add(plot3);
    multi->Add(plot4);
    multi->Add(plot5);
    
    return multi;
}

void settings_global() {

    TGaxis::SetMaxDigits(3);
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
}


void settings_fit(TMultiGraph* graph, const double XMIN, const double XMAX, const double YMIN, const double YMAX) {
    //entro nel primo canvas

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(XMIN, XMAX);
    graph->SetMinimum(YMIN);
    graph->SetMaximum(YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
    
}


void latex(TLatex* text) {

    text = new TLatex(0.75, 10.14, "#color[617]{G #equiv R_{f}/R_{1}}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(0.55, 10.115, "#color[617]{10.194 #pm 0.006}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(1.7, 10.22, "#color[632]{G #equiv slope^{MAX}}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(1.65, 10.195, "#color[632]{10.02 #pm 0.14}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(2.7, 9.97, "#color[600]{G #equiv slope^{MIN}}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(2.65, 9.945, "#color[600]{10.16 #pm 0.14}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(3.7, 10.06, "#color[418]{G #equiv slope^{ALL}}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(3.7, 10.035, "#color[418]{9.93 #pm 0.07}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(4.7, 9.93, "#color[810]{G #equiv slope^{PP}}");
    text->SetTextSize(0.03);
    text->Draw();

    text = new TLatex(4.7, 9.905, "#color[810]{10.09 #pm 0.11}");
    text->SetTextSize(0.03);
    text->Draw();
  
}

double myfit(double* x, double* par){ 

    double a = par[0];

    double fit_function = 0;

    fit_function = a;
  
    return fit_function;
}

TF1* make_fit(TGraphErrors* graph, const double XMIN, const double XMAX, const unsigned int NPAR) {

    TF1* f1 = new TF1("myfit", myfit, XMIN, XMAX, NPAR);
    f1->SetParName(0, "Media Pesata");
    f1->SetLineColor(kBlack);
    f1->SetLineStyle(2);
    f1->SetLineWidth(1);

    TFitResultPtr fit_result = graph->Fit("myfit", "S");
    fit_result->Print("V");

    return f1;
}



/*-----------------------------------------------------------------------------EOF------------------------------------------------------------------------*/