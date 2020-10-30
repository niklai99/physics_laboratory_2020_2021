#include <fstream>
#include <vector>
#include <cmath>

namespace NSP {
/*---COSTANTI---*/ 

    //nome file 
    string FILE_NAME = "../Data/data_differentiator_bode_err_db.txt";  

    //plot range del fit
    double XMIN = 1;
    double XMAX = 7;
    double YMIN = -30;
    double YMAX = 25;

    //plot range dei residui
    double RESXMIN = XMIN;
    double RESXMAX = XMAX;
    double RESYMIN = -0.7;
    double RESYMAX = 0.7;

/*---OGGETTINI CARINI---*/ 

    //vector dei dati + errori
    vector<double> x, y, errX, errY;

    //i due canvas
    TCanvas *c1, *c2;

    //il grafico del fit
    TGraphErrors *plot_err;

    //il grafico dei residui
    TGraphErrors *residuals_err;
    

/*---FUNZIONI---*/ 

    //la funzione matematica del fit
    double myfit(double*, double*);
    //numero di parametri del fit
    double NPAR = 2;

    double myfit1(double*, double*);

    //funzione per il calcolo dei residui
    TGraphErrors * res(TGraphErrors*);

    //funzione per il fit
    TFitResultPtr fit_fun(TGraphErrors*);
    TFitResultPtr fit_fun1(TGraphErrors*);
    
    //funzione per la personalizzazione del grafico fit
    void settings_fit(TGraphErrors*);

    //funzione per la personalizzazione del grafico residui
    void settings_res(TGraphErrors*);

    //funzione per l'aggiunta di linee e cose varie nel grafico dei residui
    void linee_res();

    //funzione per la personalizzazione globale dei grafici
    void settings_global();

    //funzione per leggere i dati con errori da un file
    void read_data(vector<double>&, vector<double>&, vector<double>&, vector<double>&);

    //funzione per creare il grafico del fit con errori
    TGraphErrors *plot_fit(vector<double>&, vector<double>&, vector<double>&, vector<double>&);
}

/*---MAIN---*/

void differentiator_bode_plot_err(){
 //leggo i dati con errori dal file
    NSP::read_data(NSP::x, NSP::y, NSP::errX, NSP::errY);

    //creo il grafico del fit con errori
    NSP::plot_err = NSP::plot_fit(NSP::x, NSP::y, NSP::errX, NSP::errY); 
   
    //faccio il fit
    TFitResultPtr fit = NSP::fit_fun(NSP::plot_err);
    fit->Print("V");

    //calcolo i residui
	NSP::residuals_err = NSP::res(NSP::plot_err);

    //personalizzo il grafico residui
    NSP::linee_res();
    NSP::settings_res(NSP::residuals_err); 

    TF1* f2 = new TF1("myfit1", NSP::myfit1, 4.2, 5.4, NSP::NPAR+1);
    f2->SetParNames("a", "b", "c");
    f2->SetLineColor(kGreen);

    NSP::plot_err->Fit("myfit1", "SR");

    f2->Draw("same");

    double y_max;
    y_max = f2->GetMaximum(4.3, 5.7);
    //std::cout << y_max << endl;

    double x_max;

    x_max = f2->GetMaximumX(4.3, 5.7);

    double y_taglio;

    //y_taglio = log10( pow(10, y_max) * 0.70710678118 );
    //std::cout << y_taglio << endl;
    y_taglio = y_max - 3;

    double x_taglio;

    x_taglio = f2->GetX(y_taglio, 3.8, 4.8);
    //std::cout << x_taglio << endl;

    std::cout << "Frequenza di Taglio: \n\n" << pow(10, x_taglio) << " Hz\n\n" << endl;

    
    //personalizzo il grafico fit
    NSP::settings_fit(NSP::plot_err);

/*
    TLine *line_xmax = new TLine (x_max, NSP::YMIN, x_max, NSP::YMAX);

    line_xmax->SetLineStyle(2);
    line_xmax->SetLineColor(kBlack);
    line_xmax->Draw();

    TLine *line_ymax = new TLine (NSP::XMIN, y_max, NSP::XMAX, y_max);

    line_ymax->SetLineStyle(2);
    line_ymax->SetLineColor(kBlack);
    line_ymax->Draw();
*/

    TLine *line_xtaglio = new TLine (x_taglio, NSP::YMIN, x_taglio, NSP::YMAX);

    line_xtaglio->SetLineStyle(2);
    line_xtaglio->SetLineColor(kBlack);
    line_xtaglio->Draw();

    TLine *line_ytaglio = new TLine (NSP::XMIN, y_taglio, NSP::XMAX, y_taglio);

    line_ytaglio->SetLineStyle(2);
    line_ytaglio->SetLineColor(kBlack);
    line_ytaglio->Draw();


    //personalizzo in modo globale i grafici
    NSP::settings_global();
    
    //NSP::c1->SaveAs("../Plots/opamp_max_plot.png");
    //NSP::c2->SaveAs("../Plots/opamp_max_res.png");
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

double NSP::myfit1(double* x, double* par){   
    Double_t a = par[0];
    Double_t b = par[1];
    Double_t c = par[2];

    Double_t fit_function = 0;

    fit_function = (a * pow(x[0], 2) + b * x[0] + c);

    return fit_function;
}

//fit
TFitResultPtr NSP::fit_fun(TGraphErrors* graph) {
    //il fit viene disegnato nel primo canvas
    NSP::c1 = new TCanvas("canvas1", "Fit", 1080, 720);

    //creo la funzione di root
    TF1* f1 = new TF1("myfit", myfit, 0, 4.2, NSP::NPAR);
    f1->SetParNames("a", "b");
    f1->SetLineColor(kRed);

    //faccio il fit
    TFitResultPtr fit_result = graph->Fit("myfit", "SR");

    //disegno il grafico
    graph->Draw("ap");
    f1->Draw("same");

    return fit_result;
}



//personalizzazione grafico fit
void NSP::settings_fit(TGraphErrors* graph) {
    //entro nel primo canvas
    NSP::c1->cd();

    //titolo e assi
    graph-> SetTitle("Differentiator - Bode; log_{10}[f (Hz)]; A (dB)");

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


//personalizzazione globale dei grafici
void NSP::settings_global() {
    //imposto massimo tre cifre prima di usare la notazione scientifica
    TGaxis::SetMaxDigits(3);
    //le tick labels hanno lo stesso numero di cifre significative
    gStyle->SetStripDecimals(kFALSE);
    gStyle->SetImageScaling(3.);
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


//creo il grafico con errori
TGraphErrors *NSP::plot_fit(vector<double>& x, vector<double>& y, vector<double>& errX, vector<double>& errY) {
    
    TGraphErrors* graph = new TGraphErrors(NSP::x.size(), &NSP::x[0], &NSP::y[0], &NSP::errX[0], &NSP::errY[0]);

    return graph;
}

TGraphErrors* NSP::res(TGraphErrors* graph) {
    //i residui vengono disegnati nel secondo canvas
    NSP::c2 = new TCanvas("canvas2", "Residui", 1080, 720);

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

void NSP::settings_res(TGraphErrors* graph) {
    //entro nel primo canvas
    NSP::c2->cd();

    //titolo e assi 
    graph-> SetTitle("Residui; log_{10}[f (Hz)]; A - fit (dB)");

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

void NSP::linee_res() {    
    NSP::c2->cd(); 

    //creo la linea
    TLine *line = new TLine (NSP::RESXMIN, 0, NSP::RESXMAX, 0); //linea orizzontale sullo zero 

    //personalizzazione
    line->SetLineStyle(2);
    line->SetLineColor(kBlack);

    line->Draw();
}