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

if len(sys.argv) != 2:
    print('Usage: basf2 generateValidationRoot.py dirName')
    print('')
    sys.exit(1)
dirName = str(sys.argv[1])
caliDir = '/home/belle2/zhai/extraSpace/klm_calibration/calibration_outputdb/'+sys.argv[1]+'/'

iovfile = open(caliDir+'database.txt','r')
for line in iovfile:
    lst = line.split()
    rev.append(lst[1])
    iov = lst[2].split(',')
    ini.append(int(iov[1]))
    fin.append(int(iov[3]))
iovfile.close()

#rev_num = numpy.zeros(1, dtype = int)
rev_num = numpy.zeros(1, dtype = str)
run_num = numpy.zeros(1, dtype = int)

eklm_normal = numpy.zeros(1, dtype = int)
eklm_dead = numpy.zeros(1, dtype = int)
eklm_hot = numpy.zeros(1, dtype = int)

bklm_normal = numpy.zeros(1, dtype = int)
bklm_dead = numpy.zeros(1, dtype = int)
bklm_hot = numpy.zeros(1, dtype = int)

tree = ROOT.TTree('tree','')
tree.Branch('rev_num', rev_num, 'rev_num/S')
tree.Branch('run_num', run_num, 'run_num/I')
tree.Branch('eklm_normal', eklm_normal, 'eklm_normal/I')
tree.Branch('eklm_dead', eklm_dead, 'eklm_dead/I')
tree.Branch('eklm_hot', eklm_hot, 'eklm_hot/I')
tree.Branch('bklm_normal', bklm_normal, 'bklm_normal/I')
tree.Branch('bklm_dead', bklm_dead, 'bklm_dead/I')
tree.Branch('bklm_hot', bklm_hot, 'bklm_hot/I')

for x in range(0,len(rev)):
    filename=caliDir+'dbstore_KLMChannelStatus_rev_'+str(rev[x])+'.root'
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
    myIni = int(ini[x])
    myFin = int(fin[x])
    '''
    #undesired behavior because this crowds the histogram too much
    while(myIni<myFin):
        myIni+=1
        run_num[0]=myIni
        rev_num[0]=rev[x]
        tree.Fill()
    '''
outfile = ROOT.TFile(dirName+'_validation.root', 'recreate')
tree.Write()
outfile.Close()
