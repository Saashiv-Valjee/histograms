#include "string.h"
#include "TPave.h"
#include <TArrayD.h>
#include <math.h>

vector<Color_t> mycolors = {kBlue + 1, kAzure + 7, kRed + 1, kOrange - 3, kPink + 10, kPink + 1, kYellow, kSpring - 1, kViolet, kViolet+4 , kBlack,kBlack,kBlack};
vector<Color_t> mycolors2 = {kRed, kBlue, kGreen + 3, kRed + 1, kAzure + 7, kPink + 10, kYellow + 1};
vector<Color_t> rainbow = {kRed, kOrange - 3, kYellow + 1, kSpring - 1, kAzure, kBlue + 2, kViolet};
string save_dir = "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/plots";

map<string, TH1D *> GetHistograms(vector<string> variables, string input_file) {
    map<string, TH1D *> hist_map;
    TFile *file_data = new TFile(Form("%s", input_file.c_str()), "READ");
    for (auto &var : variables) {
        hist_map[var] = (TH1D *)file_data->Get(Form("%s", var.c_str()));
    }
    return hist_map;
}

double CalculateXValueFromGivenPoint(TH1D* hist, double startPoint, double percentage) {
    int startBin = hist->GetXaxis()->FindBin(startPoint);  // Find the bin for the start point

    // Calculate the integral from the first bin to the startBin
    double partialIntegral = hist->Integral(1, startBin);
    double integral = hist->Integral();
    std::cout << "integral comparison: from mass vs full:" << partialIntegral << "vs" << integral << std::endl;
    double targetIntegral = percentage * partialIntegral;  // 68% of the partial integral

    double cumulativeSum = 0;

    // Start from the startBin and move backwards to calculate the cumulative sum
    for (int binIndex = startBin; binIndex >= 1; binIndex--) {
        cumulativeSum += hist->GetBinContent(binIndex);
        if (cumulativeSum >= targetIntegral) {
            double xValueAtPercentage = hist->GetXaxis()->GetBinLowEdge(binIndex);
            std::cout << "X-value at which cumulative integral reaches " << (percentage * 100) << "% from "
                      << startPoint << " GeV backward for histogram " << hist->GetName()
                      << " is approximately: " << xValueAtPercentage << " GeV" << std::endl;
            return xValueAtPercentage;  // Return the x-value where the cumulative integral reaches the target percentage
        }
    }

    // If no bin fulfills the condition, return the lowest edge of the histogram
    return hist->GetXaxis()->GetBinLowEdge(1);
}
void Plot_Histograms(string var, vector<TH1D *> hists, vector<string> legend_names, string tag, double mass, vector<TH1D*> env_hists,bool debug) { 
    int offset = 11;
    TCanvas *canv = new TCanvas("canv", "canv", 1920, 1080);
    gStyle->SetOptStat(0);
    gStyle->SetTextSize(0.6);

    // Define pads
    TPad *pad1 = new TPad("pad1", "pad1", 0.0, 0.5, 1.0, 1.0); // Top half of the canvas
    pad1->SetBottomMargin(0); // Set bottom margin to 0 to remove gap
    pad1->Draw(); // Draw the pad onto the canvas
    
    TPad *pad2 = new TPad("pad2", "pad2", 0.0, 0.1, 1.0, 0.5); // Bottom half of the canvas
    pad2->SetTopMargin(0);
    pad2->SetBottomMargin(0.2); // Leave some space for x-axis labels and title
    pad2->Draw(); // Draw the pad onto the canvas

    // First pad
    pad1->cd();
    TLegend *leg = new TLegend(0.85, 0.2, 0.75, 0.9);
    leg->SetTextSize(0.06);
    leg->SetBorderSize(0);
    leg->SetFillStyle(0);
    float max = 0;

    for (int i = 0; i < offset; i++) {
        hists[i]->SetLineColor(mycolors[i]);
        hists[i]->SetLineWidth(3);
        hists[i]->GetXaxis()->SetTitleSize(0); // X-axis title size
        hists[i]->GetXaxis()->SetLabelSize(0); // X-axis label size
        hists[i]->GetYaxis()->SetTitleSize(0.05); // Y-axis title size
        hists[i]->GetYaxis()->SetLabelSize(0.04); // Y-axis label size
        hists[i]->GetYaxis()->SetTitle("number of events");
        leg->AddEntry(hists[i], legend_names[i].c_str(), "l");
        if (hists[i]->GetMaximum() > max)
            max = hists[i]->GetMaximum();
    }

    pad1->SetGridx();
    pad1->SetGridy();
    double myxvalue = 0;

    for (int i = 0; i < offset; i++) {
        if (debug) std::cout << hists[i]->GetEntries() << std::endl;
        hists[i]->SetMaximum(max * 1.2);
        hists[i]->Draw("SAME");
        myxvalue = CalculateXValueFromGivenPoint(hists[i], mass, 0.68);
    }
    pad1->Update();
    TLine *linee = new TLine(myxvalue, 0, myxvalue,pad1->GetUymax());
    linee->SetLineColor(kBlack);
    linee->SetLineWidth(2);
    linee->Draw();

    TLine *llinee = new TLine(mass, 0, mass,pad1->GetUymax());
    llinee->SetLineColor(kBlack);
    llinee->SetLineWidth(2);
    llinee->Draw();

    //pad1->SetLogy();
    leg->Draw();

    // Second pad
    pad2->cd();
    max = 0;
    for (int i = offset; i < hists.size(); i++) {
        hists[i]->SetLineColor(mycolors[i - offset]);
        hists[i]->SetLineWidth(3);
        hists[i]->SetTitle("Norm Vs all");
        hists[i]->GetYaxis()->SetTitle("relative difference quadrature sums");
        hists[i]->GetXaxis()->SetTitleSize(0.07); // X-axis title size
        hists[i]->GetXaxis()->SetLabelSize(0.05); // X-axis label size
        hists[i]->GetYaxis()->SetTitleSize(0.05); // Y-axis title size
        hists[i]->GetYaxis()->SetLabelSize(0.04); // Y-axis label size 
        hists[i]->SetMaximum(1.5);
        hists[i]->SetMinimum(-1.5);
        if (i == hists.size() - 2 || i == hists.size() - 1) {
            if (debug) std::cout << "plotting quadrature envelops" << std::endl; // Check if it's one of the envelope histograms
            hists[i]->SetFillColor(17);  // A shade of grey
            hists[i]->SetFillStyle(3001); // Semi-transparent
            hists[i]->Draw("SAME");  // Draw filled and on the same plot
        } else {
            hists[i]->SetLineColor(mycolors[i - offset]);
            hists[i]->Draw("SAME");
        }
    }
    pad2->Update();
    double xmin = hists[0]->GetXaxis()->GetXmin();
    double xmax = hists[0]->GetXaxis()->GetXmax();

    // Drawing the norm
    
    // Find max and min between 0 and xValueAt68Percent
    double maxPositive = -std::numeric_limits<double>::max();
    double minNegative = std::numeric_limits<double>::max();
    int bin68 = env_hists[0]->GetXaxis()->FindBin(myxvalue);

    for (int bin = 1; bin <= bin68; bin++) {
        double posValue = env_hists[0]->GetBinContent(bin);  // envelope_positive
        double negValue = env_hists[1]->GetBinContent(bin);  // envelope_negative

        if (posValue > maxPositive) maxPositive = posValue;
        if (negValue < minNegative) minNegative = negValue;
    }       
    double xmaxPad2 = pad2->GetUxmax();
    double ymaxPad2 = pad2->GetUymax();

    TLine *lline = new TLine(0, 0.5 , xmaxPad2, 0.5);
    lline->SetLineColor(kRed);  // Set line color to red
    lline->SetLineWidth(2);
    lline->SetLineStyle(2);  // Set line style to dashed
    lline->Draw();

    TLine *liine = new TLine(0, -0.5 , xmaxPad2, -0.5);
    liine->SetLineColor(kRed);  // Set line color to red
    liine->SetLineWidth(2);
    liine->SetLineStyle(2);  // Set line style to dashed
    liine->Draw();

    TLine *lineee = new TLine(myxvalue, -1.5, myxvalue,1.5);
    lineee->SetLineColor(kBlack);
    lineee->SetLineWidth(2);
    lineee->Draw();

    TLine *liinnee = new TLine(mass, -1.5, mass,1.5);
    liinnee->SetLineColor(kBlack);
    liinnee->SetLineWidth(2);
    liinnee->Draw();

    pad2->SetGridx();
    pad2->SetGridy();
    // leg2->Draw();

    canv->SaveAs(Form("%s/%s%s.png", save_dir.c_str(),tag.c_str(), var.c_str()));
    delete canv;
    if (debug) std::cout << "Finished plotting histograms for variable: " << var << std::endl;
}

void quadrature() {

    vector<double> masses ={2500,2500,3000,3000,5000,5000};
    vector<string> tags = {"515503","515506","515507","515510","515519","515522"};
    vector<string> my_vars = {"mT_12"};
    double count = 0;
    for (string tag : tags ){
        vector<string> input_files = {
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_1/combined_hist_"+tag+"_1.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_2/combined_hist_"+tag+"_2.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_3/combined_hist_"+tag+"_3.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_4/combined_hist_"+tag+"_4.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_5/combined_hist_"+tag+"_5.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_6/combined_hist_"+tag+"_6.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_7/combined_hist_"+tag+"_7.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_8/combined_hist_"+tag+"_8.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_9/combined_hist_"+tag+"_9.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"_10/combined_hist_"+tag+"_10.root",
            "/eos/user/s/svaljee/svj-s-channel-signal-request/TruthAnalysisTests/run/ISRFSR/a"+tag+"/"+tag+"/combined_hist_"+tag+".root"
        };

        vector<map<string, TH1D *>> all_hists;
        for (auto &f : input_files) {
            map<string, TH1D *> hist_map = GetHistograms(my_vars, Form("%s", f.c_str()));
            all_hists.push_back(hist_map);
        }

        for (auto &var : my_vars) {
            vector<TH1D *> plot_hists, diff_hists;
            for (auto &mp : all_hists) {
                plot_hists.push_back(mp[var]);
            }

            TH1D* norm_hist = plot_hists[10]; // Assuming the first histogram is used as norm
            TH1D* envelope_positive = (TH1D*)norm_hist->Clone("envelope_positive");
            TH1D* envelope_negative = (TH1D*)norm_hist->Clone("envelope_negative");
            envelope_positive->Reset();
            envelope_negative->Reset();

            for (int i = 0; i < plot_hists.size()-1; i++) {
                TH1D* diff_hist = (TH1D*)plot_hists[i]->Clone();
                diff_hist->Add(norm_hist, -1); // Subtract the norm
                diff_hist->Divide(norm_hist); // Divide by the norm
                diff_hists.push_back(diff_hist);
            }

            for (int i = 0; i < diff_hists.size(); i++) {
                for (int bin = 1; bin <= diff_hists[i]->GetNbinsX(); bin++) {
                    double diff_value = diff_hists[i]->GetBinContent(bin);
                    if (diff_value >= 0) {
                        double existing_square = envelope_positive->GetBinContent(bin);
                        envelope_positive->SetBinContent(bin, existing_square + diff_value * diff_value);
                    } else {
                        double existing_square = envelope_negative->GetBinContent(bin);
                        envelope_negative->SetBinContent(bin, existing_square + diff_value * diff_value);
                    }
                }
            }

            // Calculate the square root of the quadrature sum for each component
            for (int bin = 1; bin <= envelope_positive->GetNbinsX(); bin++) {
                envelope_positive->SetBinContent(bin, sqrt(envelope_positive->GetBinContent(bin)));
                envelope_negative->SetBinContent(bin, (-1)*sqrt(envelope_negative->GetBinContent(bin)));
            }

            double maxPositive = envelope_positive->GetMaximum();
            double minNegative = envelope_negative->GetMinimum();        

            plot_hists.insert(plot_hists.end(), diff_hists.begin(), diff_hists.end());
            // Add the envelopes for plotting
            plot_hists.push_back(envelope_positive);
            plot_hists.push_back(envelope_negative);
            vector<TH1D*> env_hists = {envelope_positive, envelope_negative};

            vector<string> legend_names = {
                "Var1Up", "Var1Down",
                "Var2Up", "Var2Down",
                "Var3aUp", "Var3aDown",
                "Var3bUp", "Var3bDown",
                "Var3cUp", "Var3cDown", "Norm"
            };

            bool debug = true;
            Plot_Histograms(var, plot_hists, legend_names, tag, masses[count], env_hists, debug);
        }
        count = count + 1;
    }
}
