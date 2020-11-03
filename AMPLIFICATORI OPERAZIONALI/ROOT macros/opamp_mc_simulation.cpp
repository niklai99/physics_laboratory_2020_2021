using namespace std;
#include<cmath>


void opamp_mc_simulation()
{
    //plot range
    double XMIN = -2;
    double XMAX = 2;
    double YMIN = -18;
    double YMAX = 18;

    //nome file
    string FILE_NAME = "../Data/data_opamp_all_nooutliers.txt";

    //vectors dove mettere i dati
    vector<double> x, y, errX, errY;

    /*--- fin qui tutto chiaro spero---*/

    //LEGGO I DATI 
    ifstream f;
    f.open(FILE_NAME);
    double i = 0;
    while(f >> i) {

        x.push_back(i);    //prima colonna
        f >> i;
        y.push_back(i);    //seconda colonna
        f >> i;
        errX.push_back(i);     //push_back(0) se non ho errori sull'asse x
        f >> i;
        errY.push_back(i);

    }
    f.close();

    //canvas
    TCanvas *c1 = new TCanvas ("canvas1", "canvas1", 1080, 720);
    c1->Divide(2,0);
    c1->cd(1);


    /*
        faccio il fit dei dati per ricavare i parametri della retta che mi servono per generare i punti monte carlo
    */
    //grafico lineare
    TGraphErrors *gr1 = new TGraphErrors (FILE_NAME); //invece di file name posso mettere le reference ai vectors

    
    TF1 *f1 = new TF1("f1", "[0] + [1]*x", XMIN, XMAX);
    f1->SetParNames("offset","slope");

    TFitResultPtr r1 = gr1-> Fit("f1", "S");


    //mc preliminars

    double q = f1->GetParameter(0);
    double m = f1->GetParameter(1);

    //qui vorrei non dover mettere i valori a mano visto che ho appena fatto i due getparameter dioboia
    //sarebbe da fare una funzione c++ così che se li prende da soli
    TF1 *func = new TF1("func", "-0.0115109 + 9.98815*x", XMIN, XMAX);

    //da vector passo ad array perchè non so fare le matrici con i vector
    double* mcVin = &x[0];
    double* mcVout;
    double* mcVin_err = &errX[0];
    double* mcVout_err = &errY[0];

    //calcolo il punto y che sta sulla retta relativo al punto x
    for (unsigned int k = 0; k < x.size(); k++){

        mcVout[k]=func->Eval(mcVin[k]);
    }

    //random numbers
    TRandom *g1 = new TRandom();
    TRandom *g2 = new TRandom();
    double toyVout[2000][16];
    double toyVin[2000][16];

    //genero i 2000 punti simulati
    for (int j = 0; j < 16; j++)
    {
        for (int i = 0; i < 2000; i++)
        {
            toyVout[i][j]= g1->Gaus(mcVout[j], mcVout_err[j]);
            toyVin[i][j]= g2->Gaus(mcVin[j], mcVin_err[j]);
        }
        
    }

   //I FIT

    double slope[2000] = {};
    double errslope[2000] = {};
    double relslope[2000] = {};
    double offset[2000] = {};
    double ipsilon[16] = {};
    double ics[16] = {};

    
    for (int l = 0; l < 2000; l++)
    {
        //in questo ciclo seleziono i dati per fare i fit
        for (int m = 0; m < 16; m++)
        {
            ics[m] = toyVin[l][m];
            ipsilon[m] = toyVout[l][m];
            //cout << ics[m] << "\n" << ipsilon[m] << "\n\n\n";
        }

        //creo ogni volta il grafico = MOLTO MALE -> bisognerebbe crearlo fuori e poi aggiungerci i punti volta per volta... diventerebbe stra più veloce
        TGraphErrors *graph = new TGraphErrors(16, ics, ipsilon, mcVin_err, mcVout_err);
        //idem, anche questo andrebbe fuori dal ciclo altrimenti fotto la memoria
        TF1 *fit = new TF1("fit", "[0]+[1]*x",-10,300);  
  
        TFitResultPtr res = graph-> Fit("fit", "SQ");

        //inserisco negli array i parametri del fit 2000 volte
        offset[l]=fit->GetParameter(0);
        slope[l]=fit->GetParameter(1);
        errslope[l]=fit->GetParError(1);
        relslope[l] = errslope[l]/abs(slope[l]);
        //cout << relslope[l] << endl;
    }


    TH1D *hist = new TH1D("slope distr", "Distribuzione di slope; slope; counts", 50, 9.984, 9.992);

    //fillo il primo hist
    for(int filling=0; filling<2000; filling++){
        hist->Fill(slope[filling]);
    }
    hist->Draw();

    hist->Fit("gaus");

    //personalizzazione hist
    gPad->Modified();
    hist->GetXaxis()->SetTickLength(0.02);
    hist->GetYaxis()->SetTickLength(0.02);   
    gStyle->SetStripDecimals(kFALSE);

    c1->cd(2);

    TH1D *hist1 = new TH1D("#sigma_{slope}/slope distr", "Distribuzione di #sigma_{slope}/slope; #sigma_{slope}/slope; counts", 50, 0.0072, 0.0076);

    //fillo il secondo hist
    for(int filling1=0; filling1<2000; filling1++){
        hist1->Fill(relslope[filling1]);
    }
    hist1->Draw();

    hist1->Fit("gaus");

    //personalizzazione hist
    gPad->Modified();
    hist1->GetXaxis()->SetTickLength(0.02);
    hist1->GetYaxis()->SetTickLength(0.02);

    hist1->GetXaxis()->SetMaxDigits(6);
    


}


