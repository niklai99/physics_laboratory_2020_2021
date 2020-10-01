#include <fstream>
#include <vector>
#include <cmath>

namespace NSP {
/*---COSTANTI---*/ 

    //nome file 
    string FILE_NAME = "test.txt";  

    //plot range del fit
    double XMIN = 0;
    double XMAX = 6;
    double YMIN = 2;
    double YMAX = 7;

    //plot range dei residui
    double RESXMIN = XMIN;
    double RESXMAX = XMAX;
    double RESYMIN = -1;
    double RESYMAX = 1;

/*---OGGETTINI CARINI---*/ 

    //vector dei dati + errori
    vector<double> x, y, errX, errY;

    //i due canvas
    TCanvas *c1, *c2;

    //il grafico del fit
    TGraph *plot;
    TGraphErrors *plot_err;

    //il grafico dei residui
    TGraph *residuals;
    TGraphErrors *residuals_err;
    

/*---FUNZIONI---*/ 

    //la funzione matematica del fit
    double myfit(double*, double*);
    //numero di parametri del fit
    double NPAR = 2;

    //funzione per il calcolo dei residui
    TGraph * res(TGraph*);
    TGraphErrors * res(TGraphErrors*);

    //funzione per il fit
    TFitResultPtr fit_fun(TGraphErrors*);
    TFitResultPtr fit_fun(TGraph*);
    
    //funzione per la personalizzazione del grafico fit
    void settings_fit(TGraphErrors*);
    void settings_fit(TGraph*);

    //funzione per la personalizzazione del grafico residui
    void settings_res(TGraphErrors*);
    void settings_res(TGraph*);

    //funzione per l'aggiunta di linee e cose varie nel grafico dei residui
    void linee_res();

    //funzione per la personalizzazione globale dei grafici
    void settings_global();

    //funzione per leggere i dati senza errori da un file
    void read_data(vector<double>&, vector<double>&);

    //funzione per leggere i dati con errori da un file
    void read_data(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

    //funzione per creare il grafico del fit senza errori
    TGraph *plot_fit(vector<double>&, vector<double>&);

    //funzione per creare il grafico del fit con errori
    TGraphErrors *plot_fit(vector<double>&, vector<double>&, vector<double>&, vector<double>&);
}

/*---MAIN---*/

void plot_fit_and_res(){
/*---caso dati senza errori---*/

    //leggo i dati senza errori dal file
    NSP::read_data(NSP::x, NSP::y);

    //creo il grafico del fit senza errori  
    NSP::plot = NSP::plot_fit(NSP::x, NSP::y); 

    //faccio il fit
    TFitResultPtr fit = NSP::fit_fun(NSP::plot);

    //calcolo i residui
	NSP::residuals = NSP::res(NSP::plot);
    
    //personalizzo il grafico fit
    NSP::settings_fit(NSP::plot);

    //personalizzo il grafico residui
    NSP::linee_res();
    NSP::settings_res(NSP::residuals); 

/*---caso dati con errori---*/
/*
    //leggo i dati con errori dal file
    NSP::read_data(NSP::x, NSP::y, NSP::errX, NSP::errY);

    //creo il grafico del fit con errori
    NSP::plot_err = NSP::plot_fit(NSP::x, NSP::y, NSP::errX, NSP::errY); 
   
    //faccio il fit
    TFitResultPtr fit = NSP::fit_fun(NSP::plot_err);

    //calcolo i residui
	NSP::residuals_err = NSP::res(NSP::plot);
    
    //personalizzo il grafico fit
    NSP::settings_fit(NSP::plot_err);

    //personalizzo il grafico residui
    NSP::linee_res();
    NSP::settings_res(NSP::residuals_err); 
*/

    //personalizzo in modo globale i grafici
    NSP::settings_global();
}

/*---FUNZIONI---*/ 

//funzione matematica per il fit
double NSP::myfit(double* x, double* par){   
    Double_t a = par[0];
    Double_t b = par[1];

    Double_t fit_function = 0;

    fit_function = (a * x[0] + b);

    return fit_function;
}

//fit
TFitResultPtr NSP::fit_fun(TGraphErrors* graph) {
    //il fit viene disegnato nel primo canvas
    NSP::c1 = new TCanvas("canvas1", "Fit", 700, 500);

    //creo la funzione di root
    TF1* f1 = new TF1("myfit", myfit, NSP::XMIN, NSP::XMAX, NSP::NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("myfit", "S");

    //disegno il grafico
    graph->Draw("AP");

    return fit_result;
}

//fit
TFitResultPtr NSP::fit_fun(TGraph* graph) {
    //il fit viene disegnato nel primo canvas
    NSP::c1 = new TCanvas("canvas1", "Fit", 700, 500);

    //creo la funzione di root
    TF1* f1 = new TF1("myfit", myfit, NSP::XMIN, NSP::XMAX, NSP::NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("myfit", "S");

    //disegno il grafico
    graph->Draw("AP");

    return fit_result;
}

//residui
TGraphErrors* NSP::res(TGraphErrors* graph) {
    //i residui vengono disegnati nel secondo canvas
    NSP::c2 = new TCanvas("canvas2", "Residui", 700, 500);

    //creo vector per i residui
    vector<double> res;

    //calcolo i residui
    for (int i = 0; i < NSP::x.size(); i++) {
		res.push_back(NSP::y[i] - graph->GetFunction("myfit")->Eval(NSP::x[i]));
    }

    //creo il grafico dei residui
    TGraphErrors* res_plot = new TGraphErrors(NSP::x.size(), &NSP::x[0], &res[0], &NSP::errX[0], &NSP::errY[0]);

    //plot grafico residui
    res_plot->Draw("AP"); 

    return res_plot;
}

//residui
TGraph* NSP::res(TGraph* graph) {
    //i residui vengono disegnati nel secondo canvas
    NSP::c2 = new TCanvas("canvas2", "Residui", 700, 500);

    //creo vector per i residui
    vector<double> res;

    //calcolo i residui
    for (int i = 0; i < NSP::x.size(); i++) {
		res.push_back(NSP::y[i] - graph->GetFunction("myfit")->Eval(NSP::x[i]));
    }

    //creo il grafico dei residui
    TGraph* res_plot = new TGraph(NSP::x.size(), &NSP::x[0], &res[0]);

    //plot grafico residui
    res_plot->Draw("AP"); 

    return res_plot;  
}

//personalizzazione grafico fit
void NSP::settings_fit(TGraph* graph) {
    //entro nel primo canvas
    NSP::c1->cd();

    //titolo e assi
    graph-> SetTitle("Fit; x; y");

    //stile e colore
    graph-> SetLineColor(kBlack);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(NSP::XMIN, NSP::XMAX);
    graph->SetMinimum(NSP::YMIN);
    graph->SetMaximum(NSP::YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
}

//personalizzazione grafico fit
void NSP::settings_fit(TGraphErrors* graph) {
    //entro nel primo canvas
    NSP::c1->cd();

    //titolo e assi
    graph-> SetTitle("Fit; x; y");

    //stile e colore
    graph-> SetLineColor(kBlack);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(NSP::XMIN, NSP::XMAX);
    graph->SetMinimum(NSP::YMIN);
    graph->SetMaximum(NSP::YMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
}

//personalizzazione grafico residui 
void NSP::settings_res(TGraph* graph) {
    //entro nel primo canvas
    NSP::c2->cd();

    //titolo e assi 
    graph-> SetTitle("Residui; x; res");

    //colori e cose 
    graph-> SetLineColor(kBlack);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(NSP::RESXMIN, NSP::RESXMAX);
    graph->SetMinimum(NSP::RESYMIN);
    graph->SetMaximum(NSP::RESYMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
}

//personalizzazione grafico residui 
void NSP::settings_res(TGraphErrors* graph) {
    //entro nel primo canvas
    NSP::c2->cd();

    //titolo e assi 
    graph-> SetTitle("Residui; x; res");

    //colori e cose 
    graph-> SetLineColor(kBlack);
    graph-> SetMarkerStyle(20);
    graph-> SetMarkerColor(kBlack);
    graph-> SetMarkerSize(1);

    gPad->Modified();
    
    //plot range
    graph->GetXaxis()->SetLimits(NSP::RESXMIN, NSP::RESXMAX);
    graph->SetMinimum(NSP::RESYMIN);
    graph->SetMaximum(NSP::RESYMAX);

    //tick più guardabili
    graph->GetXaxis()->SetTickLength(0.02);
    graph->GetYaxis()->SetTickLength(0.02);
}

//linea di zero nel grafico dei residui
void NSP::linee_res() {    
    NSP::c2->cd(); 

    //creo la linea
    TLine *line = new TLine (NSP::RESXMIN, 0, NSP::RESXMAX, 0); //linea orizzontale sullo zero 

    //personalizzazione
    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();
}

//personalizzazione globale dei grafici
void NSP::settings_global() {
    //imposto massimo tre cifre prima di usare la notazione scientifica
    TGaxis::SetMaxDigits(3);
    //le tick labels hanno lo stesso numero di cifre significative
    gStyle->SetStripDecimals(kFALSE);
}

//funzione per leggere i dati senza errori da un file
void NSP::read_data(vector<double>& x, vector<double>& y) {
    //leggo il file e carico i dati nei vector
    /*---NB: sarebbe meglio usare dei vector ausiliari così si possono fare operazioni e/o propagazioni di errori prima di inserirli nei vector ufficiali---*/
    ifstream f;
    f.open(NSP::FILE_NAME);
    double i = 0;
    while(f >> i) {

        NSP::x.push_back(i);    //prima colonna
        f >> i;
        NSP::y.push_back(i);    //seconda colonna

    }
    f.close();
}

//funzione per leggere i dati con errori da un file
void NSP::read_data(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    //leggo il file e carico i dati nei vector
    /*---NB: sarebbe meglio usare dei vector ausiliari così si possono fare operazioni e/o propagazioni di errori prima di inserirli nei vector ufficiali---*/
    ifstream f;
    f.open(NSP::FILE_NAME);
    double i = 0;
    while(f >> i) {

        NSP::x.push_back(i);    //prima colonna
        f >> i;
        NSP::y.push_back(i);    //seconda colonna
        f >> i;
        NSP::errX.push_back(i);     //push_back(0) se non ho errori sull'asse x
        f >> i;
        NSP::errY.push_back(i);

    }
    f.close();
}

//creo il grafico senza errori
TGraph *NSP::plot_fit(vector<double>& x, vector<double>& y) {

    TGraph* graph = new TGraph(NSP::x.size(), &NSP::x[0], &NSP::y[0]);

    return graph;
}

//creo il grafico con errori
TGraphErrors *NSP::plot_fit(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(NSP::x.size(), &NSP::x[0], &NSP::y[0], &NSP::errX[0], &NSP::errY[0]);

    return graph;
}