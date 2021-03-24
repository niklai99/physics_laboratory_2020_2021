#!/usr/bin/python

import ROOT
import sys, getopt
import numpy as np


def main(argv):
    # read data from command line
    # TODO: define function and better syntax
    fname = ''
    bkgfrom = -1
    bkgto = -1
    projYfrom = -1
    projYto = -1
    hrname = ''
    try:
        opts, args = getopt.getopt(argv,
                                   "hf:h:bf:bt:yf:yt:",
                                   ["filename=","histname=",
                                    "bkgto=","bkgfrom=",
                                    "projYto=", "projYfrom="])
    except getopt.GetoptError:
        print("wrong commands")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('zeeman.py -f <filename> -hf <histname> ...')
            sys.exit()
        elif opt in ("-f", "--filename"):
            fname = arg
        elif opt in ("-h", "--histname"):
            hrname = arg

    # constants
    npixels=7926
    maxcolumns=1024

    # read root file
    pf = open(fname, "rb")

    # read data by chunks and store ncolumns
    ncolumns = 0
    byte = pf.read(npixels*2)
    while byte:
        ncolumns+=1
        byte = pf.read(npixels*2)
    pf.close()

    print("number of columns", ncolumns)
    #if(bkgto>ncolumns): bkgto=ncolumns

    # 2D histogram
    hzee = ROOT.TH2S("hzee", "Original Zeeman Image",
                     ncolumns,0,ncolumns, npixels, 0, npixels)


    # read file by chunks (again) to fill histogram
    pf = open(fname, "rb")
    icol = 0;
    byte = pf.read(npixels*2)
    while byte:
        sumpx=0
        for i in range(npixels):
            hzee.SetBinContent(icol+1,i+1,byte[i])
            sumpx+=byte[i]
        byte = pf.read(npixels*2)
        icol+=1

    pf.close()

    # TODO: fix 2D hist not draawing
    #c1 = ROOT.TCanvas("czee")
    #c1.cd()
    #hzee.SetStats(0)
    #c1.Draw()
    #hzee.Draw("")

    # get hist projection
    hpro = hzee.ProjectionX("_px")
    #ROOT.TCanvas("cpx")
    #c2.cd()
    hpro.Draw()

    # TODO: use extra patameters


if __name__ == "__main__":
   main(sys.argv[1:])
