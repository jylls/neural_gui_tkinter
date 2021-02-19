import numpy as np
from scipy.stats import zscore

#z-score the spike matrix
def z_scoring(spike_mat,cluster_list=None):
    N_clu=spike_mat.shape[0]
    z_norm_mat=zscore(spike_mat,axis=1)
    return z_norm_mat
