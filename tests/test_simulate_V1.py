import h5py_wrapper.wrapper as h5w
import numpy as np
import os
from multiarea_model import MultiAreaModel
from multiarea_model.default_params import complete_area_list, population_list

"""
Test simulating only V1
"""


def test_het_poisson_stat_sim():
    base_dir = os.getcwd()
    fn = os.path.join(base_dir, 'fullscale_rates.json')
    network_params = {'connection_params': {'replace_non_simulated_areas': 'het_poisson_stat',
                                            'replace_cc_input_file': fn},
                      'N_scaling': 0.001,
                      'K_scaling': 0.0001,
                      'fullscale_rates': 'fullscale_rates.json'}
    sim_params = {'t_sim': 0.1,
                  'areas_simulated': ['V1']}
    M = MultiAreaModel(network_params, simulation=True, sim_spec=sim_params)
    M.simulation.simulate()


def test_hom_poisson_stat_sim():
    network_params = {'connection_params': {'replace_non_simulated_areas': 'hom_poisson_stat'},
                      'N_scaling': 0.001,
                      'K_scaling': 0.0001,
                      'fullscale_rates': 'fullscale_rates.json'}
    sim_params = {'t_sim': 0.1,
                  'areas_simulated': ['V1']}

    M = MultiAreaModel(network_params, simulation=True, sim_spec=sim_params)
    M.simulation.simulate()


def test_het_current_non_stat_sim():
    curr = np.ones(10) * 10.
    het_current = {area: {pop: curr for pop in population_list} for area in complete_area_list}
    h5w.save('het_current.h5', het_current, write_mode='w')

    base_dir = os.getcwd()
    fn = os.path.join(base_dir, 'het_current.h5')
    network_params = {'connection_params': {'replace_non_simulated_areas': 'het_current_nonstat',
                                            'replace_cc_input_file': fn},
                      'N_scaling': 0.001,
                      'K_scaling': 0.0001,
                      'fullscale_rates': 'fullscale_rates.json'}
    sim_params = {'t_sim': 10.,
                  'areas_simulated': ['V1']}

    M = MultiAreaModel(network_params, simulation=True, sim_spec=sim_params)
    M.simulation.simulate()
