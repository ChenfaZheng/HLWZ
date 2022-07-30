import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt


# class Figure():
#     def __init__(self, figsize=None, dpi=300, xlim=None, ylim=None):
#         self.figsize = figsize if figsize else (8, 4)
#         self.fig = plt.figure(figsize=self.figsize, dpi=dpi)
#         self.ax = self.fig.add_subplot(111)
#         # TODO
#         # edit styles using mpl.rc_context({...})
#         if xlim:
#             self.ax.set_xlim(xlim)
#         if ylim:
#             self.ax.set_ylim(ylim)
        
#     def draw_spectrum_line(self, f: float, i: float, st: dict):
#         '''
#         f: frequency, Hz
#         i: intensity, count / s
#         st: mpl style, dict
#         '''
#         with mpl.rc_context(st):
#             self.ax.axvline(f, ymin=0, ymax=1)
    
#     def draw_moleculer_lines(self, detail: dict, st: dict):
#         for f, i in detail.items():
#             self.draw_moleculer_lines(f, i, st)
    
#     def save(self, path='./spectrum.png', dpi=300):
#         self.fig.savefig(fname=path, dpi=dpi)

#     def show(self):
#         plt.show()


def main():
    # read df
    df = pd.read_csv('./data/cdmsjpl.tsv', delimiter='\t')

    # generate figure
    fig = plt.figure(figsize=(16, 4), dpi=300)
    ax = fig.add_subplot(111)
    # ax.set_xlim([70e6, 3e9])    # Hz
    ax.set_xlim([2900, 3000])
    ax.set_ylim([0, 1])
    ax.set_xlabel('frequency (MHz)')
    ax.set_xscale('log')

    # cmap settings
    freq_min = df['Freq-MHz(rest frame,redshifted)'].min()
    freq_max = df['Freq-MHz(rest frame,redshifted)'].max()
    color_norm = lambda x: (x - freq_min) / (freq_max - freq_min)

    print(freq_min, freq_max)

    ymin = 0
    ymax = 1

    rainbow = cm.get_cmap('rainbow')

    lw_scale = 1e6

    # filter data


    # plot
    freqs = df['Freq-MHz(rest frame,redshifted)'].to_numpy()
    intensities = df['CDMS/JPL Intensity'].to_numpy()
    lws = np.power(10, intensities) * lw_scale
    ax_object = ax.vlines(freqs, ymin=ymin, ymax=ymax, colors=rainbow(color_norm(freqs)), linewidths=lws, cmap=rainbow)
    plt.colorbar(ax_object)

    # # plot 
    # for spec_line in df.iterrows():
    #     freq_rest = spec_line[1][2] # MHz
    #     intensity = spec_line[1][7]
    #     lw = np.log10(np.abs(intensity))    # line width
    #     color = color_norm(freq_rest)
    #     # ymin = 0 if intensity < 0 else 0.5
    #     # ymax = 0.5 if intensity < 0 else 1
    #     ymin = 0
    #     ymax = 1
    #     ax.axvline(freq_rest, ymin=ymin, ymax=ymax, linewidth=lw, color=color, cmap='rainbow')
    
    plt.savefig('./test.png', dpi=300)
    plt.close()
    pass


if __name__ == '__main__':
    main()