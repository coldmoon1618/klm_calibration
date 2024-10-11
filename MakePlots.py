import uproot
import matplotlib.pyplot as plt
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('fname')
parser.add_argument('--drawLims',action='store_true')
args=parser.parse_args()
fname=args.fname
drawLims=args.drawLims

tree=uproot.open(fname)['tree']
run_num_arry=tree.arrays('run_num')
eklm_dead_arry=tree.arrays('eklm_dead')
eklm_hot_arry=tree.arrays('eklm_hot')
bklm_dead_arry=tree.arrays('bklm_dead')
bklm_hot_arry=tree.arrays('bklm_hot')

fig,axs=plt.subplots(2,2,sharex=True)
axs=axs.ravel()

axs[0].plot(run_num_arry,eklm_dead_arry,'.',color='C0')
axs[0].set_ylabel("EKLM dead channels")
axs[0].set_xlabel("Run numbers")

axs[1].plot(run_num_arry,eklm_hot_arry,'.',color='C1')
axs[1].set_ylabel("EKLM hot channels")
axs[1].set_xlabel("Run numbers")

axs[2].plot(run_num_arry,bklm_dead_arry,'.',color='C0')
axs[2].set_ylabel("BKLM dead channels")
axs[2].set_xlabel("Run numbers")

axs[3].plot(run_num_arry,bklm_hot_arry,'.',color='C1')
axs[3].set_ylabel("BKLM hot channels")
axs[3].set_xlabel("Run numbers")

if drawLims:
    axs[0].axhline(300,ls='--',color='r')
    axs[1].axhline(8,ls='--',color='r')
    axs[2].axhline(300,ls='--',color='r')
    axs[3].axhline(8,ls='--',color='r')

fig.savefig('plots.pdf')