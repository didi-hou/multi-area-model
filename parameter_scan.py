# Create config file
with open('config.py', 'w') as fp:
    fp.write(
'''import os
base_path = os.path.abspath(".")
data_path = os.path.abspath("simulations")
jobscript_template = "python {base_path}/run_simulation.py {label}"
submit_cmd = "bash -c"
''')
    
import numpy as np
import sys
import os

from multiarea_model import MultiAreaModel
from multiarea_model import Analysis
from config import base_path, data_path

sys.path.append('./figures/MAM2EBRAINS')
from M2E_compute_rate_time_series import compute_rate_time_series
from compute_save_fc import compute_fc

# Function for performing a simlation, compute functional connectivity and save it as a .npy file
def perform_simulation(param):
    scale_down_to = 0.006
    
    cc_weights_factor = param

    complete_area_list = ['V1', 'V2', 'VP', 'V3', 'V3A', 'MT', 'V4t', 'V4', 'VOT', 'MSTd',
                          'PIP', 'PO', 'DP', 'MIP', 'MDP', 'VIP', 'LIP', 'PITv', 'PITd',
                          'MSTl', 'CITv', 'CITd', 'FEF', 'TF', 'AITv', 'FST', '7a', 'STPp',
                          'STPa', '46', 'AITd', 'TH']

    areas_simulated = complete_area_list

    replace_non_simulated_areas = 'het_poisson_stat'

    g = -11.

    rate_ext = 10.
    
    # Determine replace_cc_input_source
    replace_cc_input_source = None                                               # By default, replace_cc_input_source is set to None
                                                                                 # where areas_simulated is complete_area_list                                                           
    if set(areas_simulated) != set(complete_area_list):                                                                                       
        if replace_non_simulated_areas == 'hom_poisson_stat':                   
            replace_cc_input_source = None
        elif replace_non_simulated_areas == 'het_poisson_stat' or replace_non_simulated_areas == 'het_current_nonstat':
            replace_cc_input_source = os.path.join(base_path, 'tests/fullscale_rates.json')
        else:
            raise Exception("'hom_poisson_stat', 'het_poisson_stat', or 'het_current_nonstat' should be assigned to replace_non_simulated_areas when not all areas are simulated!")

    # Determine cc_weights_I_factor from cc_weights_factor
    if cc_weights_factor == 1.0:                                                  # For ground state with cc_weights_factor as 1., 
        cc_weights_I_factor = 1.0                                                 # cc_weights_I_factor is set to 1.
    elif cc_weights_factor > 1.0:                                                 # For cc_weights_factor larger than 1.0,
        cc_weights_I_factor = 2.0                                                 # cc_weights_I_factor is set to 2.
    else:                                                                         # cc_weights_factor outside of (1., 2.5], raise error
        raise Exception("A value that is equal to or larger than 1.0 should be assigned to the parameter cc_weights_factor!")

    # Connection parameters
    conn_params = {
        'replace_non_simulated_areas': replace_non_simulated_areas,               # Whether to replace non-simulated areas by Poisson sources 
        'g': g,                                                                   # It sets the relative inhibitory synaptic strength, by default: -11.
        'replace_cc_input_source': replace_cc_input_source,                       # Specify the data used to replace non-simulated areas      
        'cc_weights_factor': cc_weights_factor,
        'cc_weights_I_factor': cc_weights_I_factor
    }

    # Input parameters
    input_params = {
        'rate_ext': rate_ext                                                      # Rate of the Poissonian spike generator (in spikes/s), by default: 10.
    } 

    # Network parameters
    network_params = {
        'N_scaling': scale_down_to,                                               # Scaling of population sizes, by default: 1. for full scale multi-area model
        'K_scaling': scale_down_to,                                               # Scaling of indegrees, by default: 1. for full scale multi-area model
        'fullscale_rates': os.path.join(base_path, 'tests/fullscale_rates.json'), # Absolute path to the file holding full-scale rates for scaling synaptic weights, by default: None
        'input_params': input_params,                                             # Input parameters
        'connection_params': conn_params,                                         # Connection parameters
    } 

    # Simulation parameters
    sim_params = {
        'areas_simulated': areas_simulated,                                       # Cortical areas included in the simulation
        't_sim': 2000.,                                                           # Simulated time (in ms), by default: 10.
        'rng_seed': 1                                                             # Global random seed
    }
    
    M = MultiAreaModel(network_params, 
                   simulation=True,
                   sim_spec=sim_params,
                   theory=True)
    
    # Run the simulation, depending on the model parameter and downscale ratio, the running time varies largely.
    M.simulation.simulate()
    
    label = M.simulation.label
    A = Analysis(M, M.simulation, data_list=['spikes'], load_areas=None)
    
    for area in M.area_list:
            compute_rate_time_series(M, data_path, label, area, 'full')
            
    param = cc_weights_factor
    
    compute_fc(M, data_path, label, param)

    

# Parameter scan
cc_weights_factor_list = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

for param in cc_weights_factor_list:
    perform_simulation(param)