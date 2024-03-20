import correlation_toolbox.helper as ch
import numpy as np
import os
import sys

from multiarea_model import MultiAreaModel
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

from M2E_compute_synaptic_input import compute_synaptic_input

"""
Compute the functional connectivity between all areas of a given
simulation based on their time series of spiking rates or their
estimated BOLD signal.
"""

def compute_fc(M, data_path, label, param):
    # compute synaptic input
    for area in M.area_list:
        compute_synaptic_input(M, data_path, label, area)
        
    method = "synaptic_input"
    
    load_path = os.path.join(data_path,
                             label,
                             'Analysis',
                             method)
    save_path = os.path.join(data_path, 'parameter_scan')

    # """
    # Create MultiAreaModel instance to have access to data structures
    # """
    # M = MultiAreaModel({})
    
    time_series = []
    for area in M.area_list:
        fn = os.path.join(load_path,
                          '{}_{}.npy'.format(method, area))
        si = np.load(fn)
        if method == 'bold_signal':  # Cut off the long initial transient of the BOLD signal
            si = si[5000:]
        time_series.append(ch.centralize(si, units=True))

    D = pdist(time_series, metric='correlation')
    correlation_matrix = 1. - squareform(D)

    np.save(os.path.join(save_path,
                         'functional_connectivity_{}_{}.npy'.format(method, param)),
            correlation_matrix)
