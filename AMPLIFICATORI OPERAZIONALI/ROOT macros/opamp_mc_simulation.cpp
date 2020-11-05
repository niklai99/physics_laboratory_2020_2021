/*
 * Creato da Cigagna Simone e Nicolò Lai
 * 03/11/2020
 *
 *
 * Macro Root per verificare tramite una simulazione di montecarlo
 * l'eventuale presenza di errori sistematici nell'analisi dati di
 * un fit lineare.
 *
 */

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


void readData(const string FILE_NAME, vector<double> &x, vector<double> &y, vector<double> &errX, vector<double> &err0, vector<double> &errY);

TFitResultPtr linearFit(vector<double> &x, vector<double> &y, vector<double> &errX, vector<double> &errY,
                        const double XMIN, const  double XMAX);

void monteCarlo(const int n, TFitResultPtr r, vector<double> &x, vector<double> &errX, vector<double> &err0,
                 vector<double> &errY, const double XMIN, const double XMAX,  TCanvas *c1 );



void opamp_mc_simulation(){

    //numero simulazioni di montecarlo
    const int numMonti = 5000;

    //plot range
    const double XMIN = -2;
    const double XMAX = 2;
    const double YMIN = -18;
    const double YMAX = 18;

    //nome file
    const string FILE_NAME = "../Data/data_opamp_peak_peak_projected.txt";

    //vectors dove mettere i dati
    vector<double> x, y, errX, errY;
    vector<double> err0; //vector da riempire con tutti zeri per non avere errori su x

    //riempio vectors
    readData(FILE_NAME, x, y, errX, err0, errY);

    //creo canvas
    TCanvas *c1 = new TCanvas ("c1", "MC Simulation", 1080, 720);
    c1->Divide(2,0);
    c1->cd(1);

    //faccio il fit
    TFitResultPtr r = linearFit(x, y , err0, errY, XMIN, XMAX);

    //montecarlo
    monteCarlo(numMonti, r, x, errX, err0, errY, XMIN, XMAX, c1);

    //std::cout << "Programma terminato con successo"<< std::endl;
}


//leggo i dati da file
void readData(const string FILE_NAME, vector<double> &x, vector<double> &y, vector<double> &errX, vector<double> &err0, vector<double> &errY){
    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {
        x.push_back(i);    
        f >> i;
        y.push_back(i);    
        f >> i;
        errX.push_back(i);
        err0.push_back(0);     
        f >> i;
        errY.push_back(i);
    }
    f.close();
}

//faccio fit lineare preliminare
TFitResultPtr linearFit(vector<double> &x, vector<double> &y, vector<double> &errX, vector<double> &errY,
                        const double XMIN, const double XMAX){

    TGraphErrors *gr1 = new TGraphErrors (x.size(), &x[0], &y[0], &errX[0], &errY[0]);
    TF1 *f1 = new TF1("f1", "[0] + [1]*x", XMIN, XMAX);
    f1->SetParNames("offset","slope");
    TFitResultPtr r1 = gr1-> Fit("f1", "SQ");
    return r1;
}

//montecarlo
void monteCarlo(const int n, TFitResultPtr r, vector<double> &x, vector<double> &errX, vector<double> &err0, vector<double> &errY,
                 const double XMIN, const double XMAX,  TCanvas *c1 ){

    //prendo i parametri del fit preliminare                     
    const double q = r->Parameter(0);
    const double m = r->Parameter(1);
    const double errq = r->ParError(0);
    const double errm = r->ParError(1);

    //ricostruisco tale funzione
    TF1 *func = new TF1("func", "[0]+ [1]*x", XMIN, XMAX);
    func->SetParameter(0, q);
    func->SetParameter(1, m);

    // valori y teorici basati sulla funzione di fit
    vector<double> vOut;
    for(double i: x)
        vOut.push_back(func->Eval(i));

    // valori (x, y) con rumore gaussiano
    TRandom *g1 = new TRandom();
    TRandom *g2 = new TRandom();

    vector<vector<double>> toyVout(n);
    vector<vector<double>> toyVin(n);

    for(unsigned int j = 0; j < x.size(); j++){
        for(int i = 0; i < n; i++){
            double randNumb1 = g1->Gaus(vOut[j], errY[j]);
            double randNumb2 = g2->Gaus(x[j], errX[j]);
            toyVout[i].push_back(randNumb1);
            toyVin[i].push_back(randNumb2);
        }
    }

    // calcolo gli n fit
    vector<double> pend, inter, errPend, errInter, relPend;

    //faccio i fit e salvo i parametri
    for(int i = 0; i < n; i++){

        TFitResultPtr rFit = linearFit(toyVin[i], toyVout[i], err0, errY, XMIN, XMAX);

        pend.push_back(rFit->Parameter(1));
        inter.push_back(rFit->Parameter(0));
        errPend.push_back(rFit->ParError(1));
        errInter.push_back(rFit->ParError(0));
        relPend.push_back( rFit->ParError(1) / abs( rFit->Parameter(1) ) );
    }

    //istogramma pendenze
    TH1D *hist = new TH1D("slope distr", "Distribuzione di slope; slope; counts", 70, m-.9*errm, m+.9*errm);

    //filling
    for(double i: pend)
        hist->Fill(i);

    hist->Draw();
    hist->Fit("gaus");

    //modifiche
    gPad->Modified();
    hist->GetXaxis()->SetTickLength(0.02);
    hist->GetYaxis()->SetTickLength(0.02);
    gStyle->SetStripDecimals(kFALSE);
    c1->cd(2);

    //istogramma errori relativi pendenze
    TH1D *hist1 = new TH1D("#sigma_{slope}/slope distr", "Distribuzione di #sigma_{slope}/slope; #sigma_{slope}/slope; counts", 70, errm/m-0.0003, errm/m+0.0003);

    //filling
    for(double i: relPend)
        hist1->Fill(i);

    hist1->Draw();
    hist1->Fit("gaus");

    //modifiche
    gPad->Modified();
    hist1->GetXaxis()->SetTickLength(0.02);
    hist1->GetYaxis()->SetTickLength(0.02);
    hist1->GetXaxis()->SetMaxDigits(6);
}
