#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import basf2
import ROOT
from ROOT.Belle2 import KLMChannelStatus

import os.path
from os import path

for ele in range(1,127):
    filename='/home/belle2/zhai/calibration_results/KLMChannelStatus/outputdb/dbstore_KLMChannelStatus_rev_'+str(ele)+'.root'
    if(not path.exists(filename)):
        continue
    channel_status_file = ROOT.TFile(filename)
    channel_status_obj = channel_status_file.Get("KLMChannelStatus")

    EKLM_normal = 0
    EKLM_dead = 0
    EKLM_hot = 0

    BKLM_normal = 0
    BKLM_dead = 0
    BKLM_hot = 0

    for i in range(1, 65536):
        status = channel_status_obj.getChannelStatus(i)
        if(status==1):
            if(i<=15600):
                EKLM_normal += 1
            else:
                BKLM_normal += 1
        elif(status!=1 and status!=0):
            if(i<=15600):
                #print(i,' EKLM',status)
                if(status==2):
                    EKLM_dead += 1
                elif(status==3):
                    EKLM_hot += 1
            else:
                #print(i,' BKLM',status)
                if(status==2):
                    BKLM_dead += 1
                elif(status==3):
                    BKLM_hot += 1
    
    print('\n',filename)
    print('         EKLM      |        BKLM')
    print(' dead | hot |normal| dead | hot |normal')
    print(EKLM_dead,' | ',EKLM_hot,' | ',EKLM_normal,' | ',BKLM_dead,' | ',BKLM_hot,' | ',BKLM_normal)
