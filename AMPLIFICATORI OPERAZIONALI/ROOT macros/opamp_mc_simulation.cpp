using namespace std;
#include<cmath>


void opamp_mc_simulation()
{
    //plot range
    double XMIN = -2;
    double XMAX = 2;
    double YMIN = -18;
    double YMAX = 18;

    string FILE_NAME = "../Data/data_opamp_all_nooutliers.txt";

    vector<double> x, y, errX, errY;

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

    //grafico log lineare
    TGraphErrors *gr1 = new TGraphErrors (x.size(), &x[0], &y[0], &errX[0], &errY[0]);
    gr1-> SetTitle("OpAmp Mc Simulation; V_in (V); V_out (V)");

    gr1-> SetLineColor(kBlack);
    gr1-> SetMarkerStyle(20);
    gr1-> SetMarkerColor(kBlack);
    gr1-> SetMarkerSize(1);
    
    
    TF1 *f1 = new TF1("f1", "[0] + [1]*x", XMIN, XMAX);
    f1->SetLineColor(kRed);
    f1->SetParNames("offset","slope");

    TFitResultPtr r1 = gr1-> Fit("f1", "S");
    gr1->GetFunction("f1")->SetLineColor(kRed);


    //mc preliminars

    double q = f1->GetParameter(0);
    double err_q = 0;
    double m = f1->GetParameter(1);
    double err_m = 0;

    TF1 *func = new TF1("func", "-0.0115109 + 9.98815*x", XMIN, XMAX);

    double* mcVin = &x[0];
    double* mcVout;
    double* mcVin_err = &errX[0];
    double* mcVout_err = &errY[0];


    for (unsigned int k = 0; k < x.size(); k++){

        mcVout[k]=func->Eval(mcVin[k]);
    }

    //random numbers
    TRandom *g1 = new TRandom();
    TRandom *g2 = new TRandom();
    double toyVout[2000][16];
    double toyVin[2000][16];

    for (int j = 0; j < 16; j++)
    {
        for (int i = 0; i < 2000; i++)
        {
            toyVout[i][j]= g1->Gaus(mcVout[j], mcVout_err[j]);
            toyVin[i][j]= g2->Gaus(mcVin[j], mcVin_err[j]);
        }
        
    }

   //I FIT

    Double_t slope[2000] = {};
    Double_t errslope[2000] = {};
    Double_t relslope[2000] = {};
    Double_t offset[2000] = {};
    Double_t ipsilon[16] = {};
    Double_t ics[16] = {};

    TH1D *hist = new TH1D("slope distr", "Distribuzione di slope; slope; counts", 50, 9.984, 9.992);
    TH1D *hist1 = new TH1D("#sigma_{slope}/slope distr", "Distribuzione di #sigma_{slope}/slope; #sigma_{slope}/slope; counts", 50, 0.0072, 0.0076);

    
    for (int l = 0; l < 2000; l++)
    {
        for (int m = 0; m < 16; m++)
        {
            ics[m] = toyVin[l][m];
            ipsilon[m] = toyVout[l][m];
            //cout << ics[m] << "\n" << ipsilon[m] << "\n\n\n";
        }

        TGraphErrors *graph = new TGraphErrors(16, ics, ipsilon, mcVin_err, mcVout_err);
        TF1 *fit = new TF1("fit", "[0]+[1]*x",-10,300);  
        //fit->SetParNames("offset", "slope");
  
        //TFitResultPtr res = graph-> Fit("fit", "SQ");
        graph-> Fit("fit", "Q");

        offset[l]=fit->GetParameter(0);
        slope[l]=fit->GetParameter(1);
        errslope[l]=fit->GetParError(1);
        relslope[l] = errslope[l]/abs(slope[l]);
        //cout << relslope[l] << endl;

        hist->Fill(slope[l]);
        hist1->Fill(relslope[l]);

    }

    hist->Fit("gaus");
    hist1->Fit("gaus");


    hist->Draw();

    

    gPad->Modified();
    hist->GetXaxis()->SetTickLength(0.02);
    hist->GetYaxis()->SetTickLength(0.02);
    


    c1->cd(2);

    hist1->Draw();

    

    gPad->Modified();
    hist1->GetXaxis()->SetTickLength(0.02);
    hist1->GetYaxis()->SetTickLength(0.02);

    hist1->GetXaxis()->SetMaxDigits(3);
    
    //c1->SaveAs("../Plots/opamp_mc.png");
    gStyle->SetStripDecimals(kFALSE);

}


