import os
import scipy.io

# Function to load the spike times of each clusters
def load_spike_times(path):
    #path_spikes=path+'/spike_times_good_clust.mat'
    if os.path.exists(path):
        spt_mat = scipy.io.loadmat(path)
        return spt_mat['spikeTimesGoodClust'],path
    else:
        print("Sorry, this folder doesn't exist, try another one")
        return
