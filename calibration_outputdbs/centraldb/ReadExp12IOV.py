#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import numpy

rev = []
ini = []
fin = []

iovfile = open('exp12_iov.txt','r')
for line in iovfile:
    lst = line.split()
    rev.append(lst[0])
    ini.append(lst[2])
    fin.append(lst[4])
iovfile.close()

rev_num = numpy.zeros(1, dtype = int)
ini_run = numpy.zeros(1, dtype = int)
fin_run = numpy.zeros(1, dtype = int)

import ROOT
outfile = ROOT.TFile('validation_numbers.root', 'recreate')
tree = ROOT.TTree('tree','')
tree.Branch('rev_num', rev_num, 'rev_num/I')
tree.Branch('ini_run', ini_run, 'ini_run/I')
tree.Branch('fin_run', fin_run, 'fin_run/I')

for x in range(0,len(rev)):
    rev_num[0]=rev[x]
    ini_run[0]=ini[x]
    fin_run[0]=fin[x]
    tree.Fill()
tree.Write()
outfile.Close()


