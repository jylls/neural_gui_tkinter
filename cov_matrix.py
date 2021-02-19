import numpy as np

#Returns the covariance matrix
def cov_matrix(z_norm_mat,cluster_list=None):
    cov_mat=np.matmul(z_norm_mat,np.transpose(z_norm_mat))
    cov_mat=cov_mat/z_norm_mat.shape[1]
    return cov_mat
