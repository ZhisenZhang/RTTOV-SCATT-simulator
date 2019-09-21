# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import utils
import plotconst
import os

# path spec.
Project_home    = "../RTTOV-simulator"
hydro_dir       = os.path.join(Project_home, "RTTOV_Output", "hydrometeor", "feiyan")
model_time      = "2018083100003"
output_dir      = "./"

# dimension
nprof       = 41 * 41
nlevels     = 30
hydros      = ['cc', 'ciw', 'clw', 'rain', 'sp']
dist_range  = (0.35, 0.45)

# data dic
hydro_data  = {}
hydro_avgprof = {}

# [I] read data

# [A]. get lat lon
suffix      = "_centre.dat"
filename    = os.path.join(hydro_dir, model_time + suffix)

with open(filename, "r") as fin:
    center = np.array(fin.readline().split()).astype('float')
    lat = utils.readtable(fin, 5, nprof)
    lon = utils.readtable(fin, 5, nprof)

# nlevels (highlevel-->lowlevel)
# [B]. get hydro
for hydro in hydros:
    filename = os.path.join(hydro_dir, model_time + "_" + hydro + ".dat")
    hydro_data[hydro] = np.zeros((nlevels, nprof), dtype='float')

    with open(filename, 'r') as fin:
        for ilevel in range(nlevels):
            hydro_data[hydro][ilevel, :] = utils.readtable(fin, 5, nprof)


# [C]. dist_range
dist_sq = (lat - center[0]) ** 2 + (lon - center[1]) ** 2
dist_filter = (dist_range[0] ** 2 < dist_sq) & (dist_sq < dist_range[1] ** 2)

for hydro in hydros:
    filtered_hydro_data = hydro_data[hydro][:, dist_filter]
    hydro_avgprof[hydro] = np.mean(filtered_hydro_data, axis=1)

# [II] plot avgprof.pdf

fig, ax1 = plt.subplots(figsize=(6, 8))

fontsize = 10
plevel = plotconst.pressure_levels
for hydro in hydros:
    if hydro != "cc":
        hydroq = hydro_avgprof[hydro]

        ax1.plot(hydroq, plevel, label=plotconst.hydro_labels[hydro],
        color=plotconst.hydro_colors[hydro], linestyle=plotconst.hydro_linestyles[hydro],)

# add the shape boundary line
ax1.plot([1e-5, 1e-3], [325, 325], color='red', linestyle='--', linewidth=0.7)
# add the annotation
ax1.annotate("boundary line of ice particle habit 325hPa", xy=(1.2e-5, 325), xycoords='data',
xytext=(0.75, 0.45), textcoords='axes fraction',
arrowprops=dict(color='black', shrink=0.01, width=0.2, headlength=4, headwidth=2),
horizontalalignment='right', verticalalignment='center',
color='black')

ax1.set_yscale("log")
ax1.set_xscale("log")

ax1.set_xlim((1e-5, 1e-3))
ax1.set_ylim((7e+1, 1e+3))

plt.yticks([70, 100, 200, 300, 325, 400, 600, 1000],
['70', '100', '200', '300', '325', '400', '600', '1000'])

ax1.invert_yaxis()

ax1.set_xlabel("mixing ratio [kg/kg]", fontsize=fontsize * 1.2)
ax1.set_ylabel("pressure level [hPa]", fontsize=fontsize * 1.2)

plt.legend(loc="upper right", fontsize=fontsize / 1.2)

ax2 = ax1.twiny()
ax2.set_xlabel('percentage [%]')
ax2.set_xlim((0, 80))
ax2.plot(hydro_avgprof['cc'], plevel, label=plotconst.hydro_labels['cc'],
color=plotconst.hydro_colors['cc'], linestyle=plotconst.hydro_linestyles['cc'])

plt.title("Tropical Cyclone Feiyan Eyewall hydrometeor profile", fontsize=fontsize * 1.4)

plt.legend(loc="upper left", fontsize=fontsize / 1.2)

plt.tight_layout()
plt.savefig("./avgprof.pdf")

# [III] output avgprof.dat
filename = output_dir + "avgprof.dat"
with open(filename, "w") as fout:
    for hydro in hydros:
        temp_avgprof = hydro_avgprof[hydro]
        if hydro != 'cc':
            for ilevel in range(nlevels):
                fout.write("{:>10.3e}".format(temp_avgprof[ilevel]))
            fout.write("\n")
        else:
            for ilevel in range(nlevels):
                fout.write("{:>10.2f}".format(temp_avgprof[ilevel]))
            fout.write("\n")