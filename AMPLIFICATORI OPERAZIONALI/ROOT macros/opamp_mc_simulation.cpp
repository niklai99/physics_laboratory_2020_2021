using namfuncace std;
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

        NSP::x.push_back(i);    //prima colonna
        f >> i;
        NSP::y.push_back(i);    //seconda colonna
        f >> i;
        NSP::errX.push_back(i);     //push_back(0) se non ho errori sull'asse x
        f >> i;
        NSP::errY.push_back(i);

    }
    f.close();

    //canvas
    TCanvas *c1 = new TCanvas ("canvas1", "canvas1", 1080, 720);
    c1->Divide(2,0);
    c1->cd(1);

    //grafico log lineare
    TGraphErrors *gr1 = new TGraphErrors ("../Data/data_opamp_all_nooutliers.txt");
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

    double offset = f1->GetParameter(0);
    double err_offset = 0;
    double slope = f1->GetParameter(1);
    double err_slope = 0;

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
            toyV[i][j]= g1->Gaus(mcVout[j], mcVout_err[j]);
            toyT[i][j]= g2->Gaus(mcVin[j], mcVin_err[j]);
        }
        
    }
    

   //linearizzazione dei toyV

   Double_t logtoyV[2000][8];

   for (int q = 0; q < 8; q++)
   {
       for (int p = 0; p < 2000; p++)
       {
           logtoyV[p][q]=log(toyV[p][q]);
       }
       
   }


   //I FIT

    Double_t slope[2000] = {};
    Double_t errslope[2000] = {};
    Double_t relslope[2000] = {};
    Double_t taus[2000] = {};
    Double_t intercept[2000] = {};
    Double_t ipsilon[8] = {};
    Double_t ics[8] = {};

    
    for (int l = 0; l < 2000; l++)
    {
        for (int m = 0; m < 8; m++)
        {
            ics[m] = toyT[l][m];
            ipsilon[m] = logtoyV[l][m];
        }

        TGraph *graph = new TGraph(8,ics,ipsilon);
        TF1 *fit = new TF1("fit", "[0]+[1]*x",-10,300);  
        fit->SetParNames("logV0","-1/TAU");
        //fit->SetParameter(0,3);
        //fit->SetParLimits(0,2.5,3.5);
        //fit->SetParameter(1,-0.019);
        //fit->SetParLimits(1,-0.03,-0.01);
        TFitResultPtr res = graph-> Fit("fit", "S");

        intercept[l]=fit->GetParameter(0);
        slope[l]=fit->GetParameter(1);
        errslope[l]=fit->GetParError(1);
        taus[l]=-1/(slope[l]);
        relslope[l] = errslope[l]/abs(slope[l]);
        //cout << relslope[l] << endl;
    }
 /*
 for (int test=0;test<8;test++){

     cout << [test] << endl;
 } 
*/

    TH1D *hist = new TH1D("#tau distr", "Distribuzione di #tau; #tau (#mus); counts", 50, 128,140);

    for(int filling=0; filling<2000; filling++){
        hist->Fill(taus[filling]);
    }
    hist->Draw();

    hist->Fit("gaus");

    gPad->Modified();
    hist->GetXaxis()->SetTickLength(0.02);
    hist->GetYaxis()->SetTickLength(0.02);
    


    c1->cd(2);

    TH1D *hist1 = new TH1D("#sigma_{m}/m distr", "Distribuzione di #sigma_{m}/m; #sigma_{m}/m; counts", 50, 0,0.02);

    for(int filling1=0; filling1<2000; filling1++){
        hist1->Fill(relslope[filling1]);
    }
    hist1->Draw();

    hist1->Fit("gaus");

    gPad->Modified();
    hist1->GetXaxis()->SetTickLength(0.02);
    hist1->GetYaxis()->SetTickLength(0.02);

    hist1->GetXaxis()->SetNdivisions(509, kTRUE);
    


}


