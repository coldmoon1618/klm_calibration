#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import numpy
import ROOT
from ROOT.Belle2 import KLMChannelStatus

import os.path
from os import path

rev = []
ini = []
fin = []

iovfile = open('/home/belle2/zhai/outputdb/centraldb/exp12_iov.txt','r')
for line in iovfile:
    lst = line.split()
    rev.append(lst[0])
    ini.append(lst[2])
    fin.append(lst[4])
iovfile.close()

rev_num = numpy.zeros(1, dtype = int)
run_num = numpy.zeros(1, dtype = int)

eklm_normal = numpy.zeros(1, dtype = int)
eklm_dead = numpy.zeros(1, dtype = int)
eklm_hot = numpy.zeros(1, dtype = int)

bklm_normal = numpy.zeros(1, dtype = int)
bklm_dead = numpy.zeros(1, dtype = int)
bklm_hot = numpy.zeros(1, dtype = int)

tree = ROOT.TTree('tree','')
tree.Branch('rev_num', rev_num, 'rev_num/I')
tree.Branch('run_num', run_num, 'run_num/I')
tree.Branch('eklm_normal', eklm_normal, 'eklm_normal/I')
tree.Branch('eklm_dead', eklm_dead, 'eklm_dead/I')
tree.Branch('eklm_hot', eklm_hot, 'eklm_hot/I')
tree.Branch('bklm_normal', bklm_normal, 'bklm_normal/I')
tree.Branch('bklm_dead', bklm_dead, 'bklm_dead/I')
tree.Branch('bklm_hot', bklm_hot, 'bklm_hot/I')

for x in range(0,len(rev)):
    filename='/home/belle2/zhai/outputdb/centraldb/dbstore_KLMChannelStatus_rev_'+str(rev[x])+'.root'
    if(not path.exists(filename)):
        continue
    channel_status_file = ROOT.TFile(filename)
    channel_status_obj = channel_status_file.Get("KLMChannelStatus")
    eklm_normal[0]=0
    eklm_dead[0]=0
    eklm_hot[0]=0
    bklm_normal[0]=0
    bklm_dead[0]=0
    bklm_hot[0]=0
    for i in range(1, 65536):
        status = channel_status_obj.getChannelStatus(i)
        if(status==1):
            if(i<=15600):
                eklm_normal[0]+=1
            else:
                bklm_normal[0]+=1
        elif(status!=1 and status!=0):
            if(i<=15600):
                if(status==2):
                    eklm_dead[0]+=1
                elif(status==3):
                    eklm_hot[0]+=1
            else:
                if(status==2):
                    bklm_dead[0]+=1
                elif(status==3):
                    bklm_hot[0]+=1
    channel_status_file.Close()
    rev_num[0]=rev[x]
    run_num[0]=ini[x]
    tree.Fill()
    if(int(rev[x]==4)):
        continue
    myIni = int(ini[x])
    myFin = int(fin[x])
    while(myIni<myFin+1):
        myIni+=1
        run_num[0]=myIni
outfile = ROOT.TFile('validation_numbers.root', 'recreate')
tree.Write()
outfile.Close()
