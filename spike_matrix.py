import numpy as np
from binning import binning

# Function to return spike_matrix binned at time_window
def spike_matrix(spt_mat,trig,time_window,cluster_list=None,dmr=1,shuffled=False):
    if cluster_list is not None:
        N_clu_list=len(cluster_list)
    else:
        N_clu_list=spt_mat.shape[0]
    spike_mat=[]
    if cluster_list is None:
        for c in range(N_clu_list):
            spike_mat.append(binning(spt_mat,trig,time_window,spt_mat[c][0][0][0],dmr))

    else:
        for c in range(N_clu_list):
            spike_mat.append(binning(spt_mat,trig,time_window,cluster_list[c],dmr))


    spike_mat=np.array(spike_mat)
    #Shuffle spike_matrix
    if shuffled==True:
        for c in range(N_clu_list):
            perm=np.random.permutation(spike_mat.shape[1])
            spike_mat[c,:]=spike_mat[c,perm]

    return spike_mat
