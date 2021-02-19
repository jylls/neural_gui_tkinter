import numpy as np

# Function to bin the spikes of cluster cluster_nbr with bin size time_window
def binning(spt_mat,trig,time_window,cluster_nbr,dmr=1,ftsize=22):
    fs=24414.0625
    #DMR delimitation (depending on trigger)
    first_t=np.amin(trig)/fs
    last_t=np.amax(trig)/fs

    #Preparing binning,rast_arr has the same duration as the dmr
    N_bins=int((last_t-first_t)/time_window)+1
    rast_arr=np.zeros(N_bins)

    #Getting cluster numbers
    N_clu=spt_mat.shape[0]
    list_clu=np.zeros(N_clu)

    for clu_ind in range(N_clu):
        list_clu[clu_ind]=spt_mat[clu_ind][0][0][0]

    # Figuring last spikes for cluster of interest
    ind_neuron=np.where(list_clu==cluster_nbr)[0][0]

    ind_last_spike=np.where(spt_mat[ind_neuron][1]/fs<=last_t)[0][-1]
    ind_first_spike=np.where(spt_mat[ind_neuron][1]/fs>=first_t)[0][0]

    #binning
    for t in np.arange(ind_first_spike,ind_last_spike+1):
        ind_bin=int((spt_mat[ind_neuron][1][t][0]/fs-first_t)/time_window)
        rast_arr[ind_bin]+=1

    return rast_arr[:-1]
