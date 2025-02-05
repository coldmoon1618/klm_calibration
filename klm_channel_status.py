##########################################################################
# basf2 (Belle II Analysis Software Framework)                           #
# Author: The Belle II Collaboration                                     #
#                                                                        #
# See git log for contributors and copyright holders.                    #
# This file is licensed under LGPL-3.0, see LICENSE.md.                  #
##########################################################################

'''
Validation of KLM channel status calibration.
'''

# import math
import numpy
import ROOT
# from ROOT.Belle2 import KLMChannelStatus
from prompt import ValidationSettings
import argparse
import matplotlib.pyplot as plt
from basf2 import B2INFO
import collections  # <-- For easy grouping by experiment

#: Tells the automated system some details of this script
settings = ValidationSettings(name='KLM channel status',
                              description=__doc__,
                              download_files=['stdout'],
                              expert_config={
                                  "chunk_size": 100
                              })


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('job_path')
    parser.add_argument('input_data_path')
    parser.add_argument('requested_iov')
    parser.add_argument('expert_config')
    return parser.parse_args()


def plot(exp_num,
         run_num_arry,
         eklm_dead_arry,
         eklm_hot_arry,
         bklm_dead_arry,
         bklm_hot_arry,
         fname='plots.pdf',
         drawLims=True):
    """
    Make four subplots showing dead/hot channels in EKLM/BKLM vs run number.
    """
    fig, axs = plt.subplots(2, 2, sharex=True)
    axs = axs.ravel()

    axs[0].plot(run_num_arry, eklm_dead_arry, '.', color='C0')
    axs[0].tick_params(labelbottom=True)
    axs[0].set_ylabel("EKLM dead channels")

    axs[1].plot(run_num_arry, eklm_hot_arry, '.', color='C1')
    axs[1].tick_params(labelbottom=True)
    axs[1].set_ylabel("EKLM hot channels")

    axs[2].plot(run_num_arry, bklm_dead_arry, '.', color='C0')
    axs[2].set_ylabel("BKLM dead channels")
    axs[2].set_xlabel("Run numbers")

    axs[3].plot(run_num_arry, bklm_hot_arry, '.', color='C1')
    axs[3].set_ylabel("BKLM hot channels")
    axs[3].set_xlabel("Run numbers")

    if drawLims:
        axs[0].axhline(300, ls='--', color='r')
        axs[1].axhline(8, ls='--', color='r')
        axs[2].axhline(300, ls='--', color='r')
        axs[3].axhline(8, ls='--', color='r')

    fig.suptitle(f'KLM channel status calibration validation for experiment {exp_num}')
    fig.savefig(fname)


if __name__ == '__main__':
    args = parse_args()
    job_path = args.job_path
    input_data_path = args.input_data_path
    requested_iov = args.requested_iov
    expert_config = args.expert_config

    database_file = f'{job_path}/KLMChannelStatus/outputdb/database.txt'

    rev = []
    ini = []
    fin = []

    # if len(sys.argv) != 2:
    #     print('Usage: basf2 generateValidationRoot.py dirName')
    #     print('')
    #     sys.exit(1)
    # dirName = str(sys.argv[1])
    # caliDir = dirName

    exp_ini = []
    exp_fin = []

    with open(database_file, 'r') as iovfile:
        for line in iovfile:
            lst = line.split()
            # e.g. line format:  KLMChannelStatus <rev> <exp_ini>,<ini>,<exp_fin>,<fin>
            rev.append(lst[1])
            iov = lst[2].split(',')
            exp_ini.append(int(iov[0]))
            ini.append(int(iov[1]))
            exp_fin.append(int(iov[2]))
            fin.append(int(iov[3]))

    # We will accumulate the results for each experiment in a dictionary:
    #   experiment -> {
    #       'rev': [],
    #       'run_num': [],
    #       'eklm_dead': [],
    #       'eklm_hot': [],
    #       'bklm_dead': [],
    #       'bklm_hot': []
    #   }
    data_by_exp = collections.defaultdict(lambda: {
        'rev': [],
        'run_num': [],
        'eklm_normal': [],
        'eklm_dead': [],
        'eklm_hot': [],
        'bklm_normal': [],
        'bklm_dead': [],
        'bklm_hot': [],
    })

    for x in range(len(rev)):
        filename = f'{job_path}/KLMChannelStatus/outputdb/dbstore_KLMChannelStatus_rev_{rev[x]}.root'
        channel_status_file = ROOT.TFile(filename)
        channel_status_obj = channel_status_file.Get("KLMChannelStatus")

        # Temporary counters
        eklm_normal = 0
        eklm_dead = 0
        eklm_hot = 0
        bklm_normal = 0
        bklm_dead = 0
        bklm_hot = 0

        # Count how many channels are normal/dead/hot in EKLM and BKLM
        for i in range(1, 65536):
            status = channel_status_obj.getChannelStatus(i)
            if status == 1:
                # Normal
                if i <= 15600:
                    eklm_normal += 1
                else:
                    bklm_normal += 1
            elif status != 1 and status != 0:
                # Dead or hot
                if i <= 15600:
                    if status == 2:
                        eklm_dead += 1
                    elif status == 3:
                        eklm_hot += 1
                else:
                    if status == 2:
                        bklm_dead += 1
                    elif status == 3:
                        bklm_hot += 1

        channel_status_file.Close()

        # Use the "initial experiment" as the key, assuming exp_ini == exp_fin
        this_exp = exp_ini[x]

        # Store the relevant data in our dictionary
        data_by_exp[this_exp]['rev'].append(rev[x])
        data_by_exp[this_exp]['run_num'].append(ini[x])
        data_by_exp[this_exp]['eklm_normal'].append(eklm_normal)
        data_by_exp[this_exp]['eklm_dead'].append(eklm_dead)
        data_by_exp[this_exp]['eklm_hot'].append(eklm_hot)
        data_by_exp[this_exp]['bklm_normal'].append(bklm_normal)
        data_by_exp[this_exp]['bklm_dead'].append(bklm_dead)
        data_by_exp[this_exp]['bklm_hot'].append(bklm_hot)

    # Now we have all the data grouped by experiment in data_by_exp.
    # Produce one validation root file + one PDF plot per experiment:
    all_exps = sorted(data_by_exp.keys())
    B2INFO(f'Found experiments: {all_exps}')

    for exp in all_exps:
        # Prepare arrays for building a TTree
        rev_num_arr = numpy.array(data_by_exp[exp]['rev'], dtype='O')  # object/string
        run_num_arr = numpy.array(data_by_exp[exp]['run_num'], dtype='i')
        eklm_normal_arr = numpy.array(data_by_exp[exp]['eklm_normal'], dtype='i')
        eklm_dead_arr = numpy.array(data_by_exp[exp]['eklm_dead'], dtype='i')
        eklm_hot_arr = numpy.array(data_by_exp[exp]['eklm_hot'], dtype='i')
        bklm_normal_arr = numpy.array(data_by_exp[exp]['bklm_normal'], dtype='i')
        bklm_dead_arr = numpy.array(data_by_exp[exp]['bklm_dead'], dtype='i')
        bklm_hot_arr = numpy.array(data_by_exp[exp]['bklm_hot'], dtype='i')
        B2INFO(f'Run range for experiment {exp}: [{numpy.min(run_num_arr)},{numpy.max(run_num_arr)}]')

        # Create a new ROOT file for this experiment
        root_filename = f'validation_exp{exp}.root'
        outfile = ROOT.TFile(root_filename, 'recreate')

        # We will store one TTree named 'tree'
        tree = ROOT.TTree('tree', 'KLM Channel Status Validation')

        # Prepare numpy arrays that TTree will store entry-by-entry
        rev_num = numpy.zeros(1, dtype=object)
        run_num = numpy.zeros(1, dtype='int32')
        eklm_normal = numpy.zeros(1, dtype='int32')
        eklm_dead = numpy.zeros(1, dtype='int32')
        eklm_hot = numpy.zeros(1, dtype='int32')
        bklm_normal = numpy.zeros(1, dtype='int32')
        bklm_dead = numpy.zeros(1, dtype='int32')
        bklm_hot = numpy.zeros(1, dtype='int32')

        # Create branches
        tree.Branch('rev_num', rev_num, 'rev_num/C')  # store as char*
        tree.Branch('run_num', run_num, 'run_num/I')
        tree.Branch('eklm_normal', eklm_normal, 'eklm_normal/I')
        tree.Branch('eklm_dead', eklm_dead, 'eklm_dead/I')
        tree.Branch('eklm_hot', eklm_hot, 'eklm_hot/I')
        tree.Branch('bklm_normal', bklm_normal, 'bklm_normal/I')
        tree.Branch('bklm_dead', bklm_dead, 'bklm_dead/I')
        tree.Branch('bklm_hot', bklm_hot, 'bklm_hot/I')

        # Fill the tree
        for i in range(len(run_num_arr)):
            rev_num[0] = rev_num_arr[i].encode('utf-8')  # needed for a C-style char array
            run_num[0] = run_num_arr[i]
            eklm_normal[0] = eklm_normal_arr[i]
            eklm_dead[0] = eklm_dead_arr[i]
            eklm_hot[0] = eklm_hot_arr[i]
            bklm_normal[0] = bklm_normal_arr[i]
            bklm_dead[0] = bklm_dead_arr[i]
            bklm_hot[0] = bklm_hot_arr[i]
            tree.Fill()

        # Write the TTree
        tree.Write()
        outfile.Close()

        # Now make a PDF plot for this experiment
        pdf_filename = f'plots_exp{exp}.pdf'
        plot(
            exp_num=exp,
            run_num_arry=run_num_arr,
            eklm_dead_arry=eklm_dead_arr,
            eklm_hot_arry=eklm_hot_arr,
            bklm_dead_arry=bklm_dead_arr,
            bklm_hot_arry=bklm_hot_arr,
            fname=pdf_filename
        )

    # Done!
    B2INFO("Validation completed successfully.")