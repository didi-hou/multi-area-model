import json
import numpy as np
import matplotlib.pyplot as pl
import os

from helpers import area_list, datapath
from matplotlib import gridspec
from matplotlib.colors import LogNorm
from matplotlib.ticker import FixedLocator
from matplotlib import rc_file
from multiarea_model import MultiAreaModel
from plotcolors import myblue
from scipy import stats

# rc_file('plotstyle.rc')

def visualize_interareal_connectivity(M):
    scale_down_to = 1
    cc_weights_factor = 1.0
    areas_simulated = ['V1', 'V2', 'VP', 'V3', 'V3A', 'MT', 'V4t', 'V4', 'VOT', 'MSTd', 
                       'PIP', 'PO', 'DP', 'MIP', 'MDP', 'VIP', 'LIP', 'PITv', 'PITd', 
                       'MSTl', 'CITv', 'CITd', 'FEF', 'TF', 'AITv', 'FST', '7a', 'STPp', 
                       'STPa', '46', 'AITd', 'TH']
    replace_non_simulated_areas = 'het_poisson_stat'
    
    conn_params = {
        'replace_non_simulated_areas': 'het_poisson_stat',
        'g': -11.,
        'K_stable': 'K_stable.npy',
        'fac_nu_ext_TH': 1.2,
        'fac_nu_ext_5E': 1.125,
        'fac_nu_ext_6E': 1.41666667,
        'av_indegree_V1': 3950.
    }

    input_params = {
        'rate_ext': 10.
    } 

    neuron_params = {
        'V0_mean': -150.,
        'V0_sd': 50.}

    network_params = {
        'N_scaling': scale_down_to, # Scaling of population sizes, by default: 1.
        'K_scaling': scale_down_to, # Scaling of indegrees, by default: 1.
        'fullscale_rates': 'tests/fullscale_rates.json',
        'input_params': input_params, # Input parameters
        'connection_params': conn_params, # Connection parameters
        'neuron_params': neuron_params # Neuron parameters
    } 

    sim_params = {
        'areas_simulated': areas_simulated,
        't_sim': 2000., # Simulated time (in ms), by default: 10.0
        'num_processes': 1, # The number of MPI processes, by default: 1
        'local_num_threads': 1, # The number of threads per MPI process, by default: 1
        'recording_dict': {'record_vm': False},
        'rng_seed': 1  # global random seed
    }

    theory_params = {
        'dt': 0.1 # The time step of the mean-field theory integration, by default: 0.01
    } 

    M_full_scale = MultiAreaModel(network_params, 
                                  simulation=True,
                                  sim_spec=sim_params,
                                  theory=True,
                                  theory_spec=theory_params)
    
    """
    Figure layout
    """
    nrows = 2
    ncols = 2
    width = 6.8556
    panel_wh_ratio = 0.7 * (1. + np.sqrt(5)) / 2.  # golden ratio

    height = width / panel_wh_ratio * float(nrows) / ncols
    print(width, height)
    pl.rcParams['figure.figsize'] = (width, height)

    fig = pl.figure()
    axes = {}

    # gs1 = gridspec.GridSpec(2, 2)
    gs1 = gridspec.GridSpec(1, 2)
    gs1.update(left=0.06, right=0.95, top=0.95, bottom=0.1, wspace=0.1, hspace=0.3)

    # axes['A'] = pl.subplot(gs1[:1, :1])
    # axes['B'] = pl.subplot(gs1[:1, 1:2])
    axes['B'] = pl.subplot(gs1[:1, :1])
    axes['D'] = pl.subplot(gs1[:1, 1:2])

    # pos = axes['A'].get_position()
    pos2 = axes['D'].get_position()
    # axes['C'] = pl.axes([pos.x0 + 0.01, pos2.y0, pos.x1 - pos.x0 - 0.025, 0.23])

    print(pos.x1 - pos.x0 - 0.025)

    # labels = ['A', 'B', 'C', 'D']
    labels = ['B', 'D']
    for label in labels:
        if label in ['C']:
            label_pos = [-0.045, 1.18]
        else:
            label_pos = [-0.2, 1.04]
        # pl.text(label_pos[0], label_pos[1], r'\bfseries{}' + label,
        #         fontdict={'fontsize': 10, 'weight': 'bold',
        #                   'horizontalalignment': 'left', 'verticalalignment':
        #                   'bottom'}, transform=axes[label].transAxes)
        pl.text(label_pos[0], label_pos[1], label,
                 fontdict={'fontsize': 10, 'weight': 'bold', 
                           'horizontalalignment': 'left', 'verticalalignment': 
                           'bottom'}, transform=axes[label].transAxes)

    # """
    # Load data
    # """
    # M = MultiAreaModel({})

    # with open(os.path.join(datapath, 'viscortex_processed_data.json'), 'r') as f:
    #     proc = json.load(f)
    # with open(os.path.join(datapath, 'viscortex_raw_data.json'), 'r') as f:
    #     raw = json.load(f)

    # FLN_Data_FV91 = proc['FLN_Data_FV91']

    # cocomac_data = raw['cocomac_data']
    # median_distance_data = raw['median_distance_data']

    # cocomac = np.zeros((32, 32))
    # conn_matrix = np.zeros((32, 32))
    # for i, area1 in enumerate(area_list[::-1]):
    #     for j, area2 in enumerate(area_list):
    #         if M.K_areas[area1][area2] > 0. and area2 in cocomac_data[area1]:
    #             cocomac[i][j] = 1.
    #         if area2 in FLN_Data_FV91[area1]:
    #             conn_matrix[i][j] = FLN_Data_FV91[area1][area2]

    # """
    # Panel A: CoCoMac Data
    # """
    # ax = axes['A']
    # ax.yaxis.set_ticks_position("left")
    # ax.xaxis.set_ticks_position("bottom")

    # ax.set_aspect(1. / ax.get_data_ratio())
    # ax.yaxis.set_ticks_position("none")
    # ax.xaxis.set_ticks_position("none")

    # masked_matrix = np.ma.masked_values(cocomac, 0.0)
    # cmap = pl.cm.binary
    # cmap.set_bad('w', 1.0)

    # x = np.arange(0, len(area_list) + 1)
    # y = np.arange(0, len(area_list[::-1]) + 1)
    # X, Y = np.meshgrid(x, y)

    # ax.set_xticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    # ax.set_xticklabels(area_list, rotation=90, size=6.)

    # ax.set_yticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    # ax.set_yticklabels(area_list[::-1], size=6.)

    # ax.set_ylabel('Target area')
    # ax.set_xlabel('Source area')

    # im = ax.pcolormesh(masked_matrix, cmap=cmap,
    #                    edgecolors='None', vmin=0., vmax=1.)

    # t = FixedLocator([])
    # cbar = pl.colorbar(im, ticks=t, fraction=0.046, ax=ax)
    # cbar.set_alpha(0.)
    # cbar.remove()

    # """
    # Panel B: Data from Markov et al. (2014) "A weighted and directed
    # interareal connectivity matrix for macaque cerebral cortex."
    # Cerebral Cortex, 24(1), 17–36.
    # """
    # ax = axes['B']
    # ax.set_aspect(1. / ax.get_data_ratio())
    # ax.yaxis.set_ticks_position("none")
    # ax.xaxis.set_ticks_position("none")

    # masked_matrix = np.ma.masked_values(conn_matrix, 0.0)
    # cmap = pl.get_cmap('inferno')
    # cmap.set_bad('w', 1.0)

    # x = np.arange(0, len(area_list) + 1)
    # y = np.arange(0, len(area_list[::-1]) + 1)
    # X, Y = np.meshgrid(x, y)

    # ax.set_xticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    # ax.set_xticklabels(area_list, rotation=90, size=6.)

    # ax.set_yticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    # ax.set_yticklabels(area_list[::-1], size=6.)

    # im = ax.pcolormesh(masked_matrix, cmap=cmap,
    #                    edgecolors='None', norm=LogNorm(vmin=1e-6, vmax=1.))

    # t = FixedLocator([1e-6, 1e-4, 1e-2, 1])
    # cbar = pl.colorbar(im, ticks=t, fraction=0.046, ax=ax)
    # cbar.set_alpha(0.)

    """
    Panel B: Interareal connectivity of full-scaling multi-area model
    """
    conn_matrix_full_scale = np.zeros((32, 32))
    for i, area1 in enumerate(area_list[::-1]):
        for j, area2 in enumerate(area_list):
            conn_matrix_full_scale[i][j] = M_full_scale.K_areas[area1][
                area2] / np.sum(list(M_full_scale.K_areas[area1].values()))

    ax = axes['D']
    ax.yaxis.set_ticks_position("none")
    ax.xaxis.set_ticks_position("none")

    ax.set_aspect(1. / ax.get_data_ratio())

    masked_matrix_full_scale = np.ma.masked_values(conn_matrix_full_scale, 0.0)
    cmap = pl.get_cmap('inferno')
    cmap.set_bad('w', 1.0)

    x = np.arange(0, len(area_list) + 1)
    y = np.arange(0, len(area_list[::-1]) + 1)
    X, Y = np.meshgrid(x, y)

    ax.set_xticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    ax.set_xticklabels(area_list, rotation=90, size=6.)

    ax.set_yticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    ax.set_yticklabels(area_list[::-1], size=6.)

    ax.set_ylabel('Target area')
    ax.set_xlabel('Source area')
    im = ax.pcolormesh(masked_matrix_full_scale, cmap=cmap,
                       edgecolors='None', norm=LogNorm(vmin=1e-6, vmax=1.))

    t = FixedLocator([1e-6, 1e-4, 1e-2, 1])
    cbar = pl.colorbar(im, ticks=t, fraction=0.046, ax=ax)
    cbar.set_alpha(0.)

    # """
    # Panel C: Exponential decay of FLN with distance
    # """
    # FLN_values_FV91 = np.array([])
    # distances_FV91 = np.array([])

    # for target_area in FLN_Data_FV91:
    #     for source_area in FLN_Data_FV91[target_area]:
    #         if target_area in median_distance_data and source_area in median_distance_data:
    #             if FLN_Data_FV91[target_area][source_area]:
    #                 FLN_values_FV91 = np.append(FLN_values_FV91, FLN_Data_FV91[
    #                                             target_area][source_area])
    #                 distances_FV91 = np.append(distances_FV91, median_distance_data[
    #                                            target_area][source_area])

    # # Linear fit of distances vs. log FLN
    # print("\n \n Linear fit to logarithmic values")
    # gradient, intercept, r_value, p_value, std_err = stats.linregress(
    #     distances_FV91, np.log(FLN_values_FV91))
    # print("Raw parameters: ", gradient, intercept)
    # print("Transformed parameters: ", -gradient, np.exp(intercept))
    # print('r_value**2', r_value ** 2)
    # print('p_value', p_value)
    # print('std_err', std_err)

    # ax = axes['C']
    # ax.yaxis.set_ticks_position("left")
    # ax.xaxis.set_ticks_position("bottom")

    # ax.yaxis.set_ticks_position("left")
    # ax.xaxis.set_ticks_position("bottom")

    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # ax.yaxis.set_ticks_position("left")
    # ax.xaxis.set_ticks_position("bottom")

    # ax.plot(distances_FV91, np.log10(FLN_values_FV91), '.', color=myblue)
    # x = np.arange(np.min(distances_FV91), np.max(distances_FV91), 1)
    # ax.plot(x, (intercept + gradient * x) / np.log(10), linewidth=2.0,
    #         color='Black', label='Linear regression fit')

    # ax.set_xlabel('Distance (mm)', labelpad=7)
    # ax.set_ylabel(r'$\log(FLN)$')
    # ax.set_yticks([-6, -4, -2, 0])

    # print("log fit")
    # print(np.corrcoef(gradient * distances_FV91 + intercept, np.log(FLN_values_FV91))[0][1])

    # """
    # Panel D: Resulting connectivity matrix
    # """
    # conn_matrix = np.zeros((32, 32))
    # for i, area1 in enumerate(area_list[::-1]):
    #     for j, area2 in enumerate(area_list):
    #         conn_matrix[i][j] = M.K_areas[area1][
    #             area2] / np.sum(list(M.K_areas[area1].values()))

    # ax = axes['D']
    # ax.yaxis.set_ticks_position("none")
    # ax.xaxis.set_ticks_position("none")

    # ax.set_aspect(1. / ax.get_data_ratio())

    # masked_matrix = np.ma.masked_values(conn_matrix, 0.0)
    # cmap = pl.get_cmap('inferno')
    # cmap.set_bad('w', 1.0)

    # x = np.arange(0, len(area_list) + 1)
    # y = np.arange(0, len(area_list[::-1]) + 1)
    # X, Y = np.meshgrid(x, y)

    # ax.set_xticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    # ax.set_xticklabels(area_list, rotation=90, size=6.)

    # ax.set_yticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    # ax.set_yticklabels(area_list[::-1], size=6.)

    # ax.set_ylabel('Target area')
    # ax.set_xlabel('Source area')
    # im = ax.pcolormesh(masked_matrix, cmap=cmap,
    #                    edgecolors='None', norm=LogNorm(vmin=1e-6, vmax=1.))

    # t = FixedLocator([1e-6, 1e-4, 1e-2, 1])
    # cbar = pl.colorbar(im, ticks=t, fraction=0.046, ax=ax)
    # cbar.set_alpha(0.)

    """
    Panel D: Interareal connectivity of down-scaling multi-area model
    """
    conn_matrix_down_scale = np.zeros((32, 32))
    for i, area1 in enumerate(area_list[::-1]):
        for j, area2 in enumerate(area_list):
            conn_matrix_down_scale[i][j] = M.K_areas[area1][
                area2] / np.sum(list(M.K_areas[area1].values()))

    ax = axes['D']
    ax.yaxis.set_ticks_position("none")
    ax.xaxis.set_ticks_position("none")

    ax.set_aspect(1. / ax.get_data_ratio())

    masked_matrix_down_scale = np.ma.masked_values(conn_matrix_down_scale, 0.0)
    cmap = pl.get_cmap('inferno')
    cmap.set_bad('w', 1.0)

    x = np.arange(0, len(area_list) + 1)
    y = np.arange(0, len(area_list[::-1]) + 1)
    X, Y = np.meshgrid(x, y)

    ax.set_xticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    ax.set_xticklabels(area_list, rotation=90, size=6.)

    ax.set_yticks([i + 0.5 for i in np.arange(0, len(area_list) + 1, 1)])
    ax.set_yticklabels(area_list[::-1], size=6.)

    ax.set_ylabel('Target area')
    ax.set_xlabel('Source area')
    im = ax.pcolormesh(masked_matrix_down_scale, cmap=cmap,
                       edgecolors='None', norm=LogNorm(vmin=1e-6, vmax=1.))

    t = FixedLocator([1e-6, 1e-4, 1e-2, 1])
    cbar = pl.colorbar(im, ticks=t, fraction=0.046, ax=ax)
    cbar.set_alpha(0.)

    # """
    # Save figure
    # """
    # pl.savefig('Fig4_connectivity.eps')