#include <iostream>
#include <fstream>
#include <cmath>

#include <TTree.h>
#include <TFile.h>
#include <TH1.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TString.h>
#include <TMath.h>
#include <TChain.h>

void setAndDraw(TGraph *gr, const char *title, int color, int style, double max, bool makeLog){
    gr -> SetMarkerColor(color);
    gr -> SetTitle(title);
    gr -> SetMarkerStyle(style);
    gr -> SetMarkerSize(1.2);
    gr -> Draw("AP");
    gr -> GetXaxis() -> SetTitle("Run numbers");
    gr -> GetYaxis() -> SetTitle("Number of channels");
    if(makeLog)gPad -> SetLogy();
    else if(false){
        gr -> SetMaximum(max);
        gr -> SetMinimum(0.);
    }
}

void MakePlots(TString caliName) {
    bool makeLog = 0;

    ////////////////////////////////////////////////
    TChain *tree = new TChain("tree");            //
                                                  //
    tree -> AddFile(caliName+"_validation.root"); //
                                                  //
    Int_t allEntries = tree -> GetEntries();      //
    ////////////////////////////////////////////////

    ////////////////////////////////////////// entries ////////////////////////////////////////////////
    Short_t   rev_num;
    tree -> SetBranchAddress("rev_num", &rev_num);
    Int_t   run_num;
    tree -> SetBranchAddress("run_num", &run_num);
    Int_t   eklm_dead;
    tree -> SetBranchAddress("eklm_dead", &eklm_dead);
    Int_t   eklm_hot;
    tree -> SetBranchAddress("eklm_hot", &eklm_hot);
    Int_t   bklm_dead;
    tree -> SetBranchAddress("bklm_dead", &bklm_dead);
    Int_t   bklm_hot;
    tree -> SetBranchAddress("bklm_hot", &bklm_hot);

    Int_t run_num_arry[allEntries];
    Int_t eklm_dead_arry[allEntries];
    Int_t eklm_hot_arry[allEntries];
    Int_t bklm_dead_arry[allEntries];
    Int_t bklm_hot_arry[allEntries];
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for(int i=0; i < allEntries; i++){
        tree -> GetEntry(i);

        run_num_arry[i]=run_num;
        eklm_dead_arry[i]=eklm_dead;
        eklm_hot_arry[i]=eklm_hot;
        bklm_dead_arry[i]=bklm_dead;
        bklm_hot_arry[i]=bklm_hot;
    }

    TCanvas *c_klm = new TCanvas("c_klm","c_klm",1000,700);
    c_klm->Divide(2,2,.005,.005,0);
    c_klm->cd(1);
    TGraph *gr_eklm_dead = new TGraph(allEntries,run_num_arry,eklm_dead_arry);
    setAndDraw(gr_eklm_dead,"EKLM dead channels",kRed+2,26,300,makeLog);

    c_klm->cd(2);
    TGraph *gr_eklm_hot = new TGraph(allEntries,run_num_arry,eklm_hot_arry);
    setAndDraw(gr_eklm_hot,"EKLM hot channels",kBlue+2,24,8,makeLog);

    c_klm->cd(3);
    TGraph *gr_bklm_dead = new TGraph(allEntries,run_num_arry,bklm_dead_arry);
    setAndDraw(gr_bklm_dead,"BKLM dead channels",kRed+2,26,300,makeLog);

    c_klm->cd(4);
    TGraph *gr_bklm_hot = new TGraph(allEntries,run_num_arry,bklm_hot_arry);
    setAndDraw(gr_bklm_hot,"BKLM hot channels",kBlue+2,24,8,makeLog);

    c_klm -> SaveAs(caliName+"_plots.pdf");
   
    return ;
}
