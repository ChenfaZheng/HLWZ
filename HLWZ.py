import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import cm
import matplotlib.pyplot as plt

import argparse


def main():
    # load console args
    parser = argparse.ArgumentParser(description='HLWZ -- The program to show moleculer spectrums.')
    parser.add_argument('--fmin', type=float, default=1050, 
                    help='The min frequency [MHz] to be shown. Default is 1050.')
    parser.add_argument('--fmax', type=float, default=1450, 
                    help='The min frequency [MHz] to be shown. Default is 1450.')
    parser.add_argument('--imin', type=float, default=None, 
                    help='The lower limit of the logged spectrum intensity to be shown.')
    parser.add_argument('--imax', type=float, default=None, 
                    help='The upper limit of the logged spectrum intensity to be shown.')
    parser.add_argument('--el', type=float, default=None, 
                    help='Lower stat energy in K.')
    parser.add_argument('--eu', type=float, default=None, 
                    help='Higher stat energy in K.')
    parser.add_argument('-z', '--redshift', type=float, default=0, 
                    help='The redshift of the acquired spectrums. Calculated using frequencies.')
    parser.add_argument('-m', '--molecules', type=str, nargs='+', default=None, 
                    help='The molecules to be shown. Capital sensitive.')
    parser.add_argument('-l', '--linelist', default='ALL', type=str, choices=['ALL', 'JPL', 'CDMS'], 
                    help='The project that used in database [JPL/CDMS]. Default is `ALL`, that use both JPL and CDMS.')
    parser.add_argument('--linewidth', action='store_true', 
                    help='Set the linewidth of the spectrum changes with intensity. Default is True.')
    parser.add_argument('--lwscale', type=float, default=1e6, 
                    help='The linewidth scale.')
    parser.add_argument('--userainbow', action='store_true', 
                    help='Use the rainbow colormap (along the frequency axis) to show spectrum.')
    parser.add_argument('--datapath', type=str, default='./data/cdmsjpl.tsv', 
                    help='The path of the spectrum data. Default is ./data/cdmsjpl.tsv')
    parser.add_argument('--logscale', action='store_true', 
                    help='Use log scale on x-axis. Otherwise linear scale.')
    parser.add_argument('--saveto', type=str, default='./moleculer.png', 
                    help='Where to save the figure. Default is ./moleculer.png')
    parser.add_argument('--show', action='store_true', 
                    help='Show figure with GUI backend.')
    parser.add_argument('--alpha', type=float, default=0.9, 
                    help='Transparency of the spectrum lines. Range in [0, 1]')
    parser.add_argument('--dark', action='store_true', 
                    help='Use dark style.')

    args = parser.parse_args()
    print(args)

    # load conf
    fmin = args.fmin
    fmax = args.fmax
    imin = args.imin
    imax = args.imax
    z = args.redshift
    ms = args.molecules
    ll = args.linelist
    if args.linewidth:
        lw_scale = args.lwscale
    data_path = args.datapath
    userainbow = args.userainbow

    # read df
    df = pd.read_csv(data_path, delimiter='\t')

    # mask-out repeated spectrums
    df.sort_values(by='Freq-MHz(rest frame,redshifted)', inplace=True)
    freq_arr = df['Freq-MHz(rest frame,redshifted)'].to_numpy()
    freq_same_mask = np.diff(freq_arr, prepend=1.0) != 0
    df = df[freq_same_mask]


    # redshift data
    if z > 0:
        df['Freq-MHz(rest frame,redshifted)'] /= (1 + z)

    # filter data
    df = df[df['Freq-MHz(rest frame,redshifted)'] >= fmin]
    df = df[df['Freq-MHz(rest frame,redshifted)'] <= fmax]
    if imin:
        df = df[df['CDMS/JPL Intensity'] >= imin]
    if imax:
        df = df[df['CDMS/JPL Intensity'] <= imax]
    if args.el:
        df = df[df['E_L (K)'] >= args.el]
    if args.eu:
        df = df[df['E_U (K)'] <= args.eu]
    if ll == 'JPL':
        df = df[df['Linelist'] == 'JPL']
    elif ll == 'CDMS':
        df = df[df['Linelist'] == 'CDMS']
    if ms:
        ms_masks = []
        for m_name in ms:
            ms_masks.append(df['Species'] == m_name)
        ms_mask0 = ms_masks[0]
        for mask in ms_masks[1:]:
            ms_mask0 = ms_mask0 | mask
        df = df[ms_mask0]

    print(f'Total {df.shape[0]:d} spectrums')
    
    # cmap settings
    if userainbow:
        rainbow = cm.get_cmap('rainbow_r')
        freq_min = df['Freq-MHz(rest frame,redshifted)'].min()
        freq_max = df['Freq-MHz(rest frame,redshifted)'].max()
        color_norm = lambda x: (x - freq_min) / (freq_max - freq_min)

    # linewidth settings
    if args.linewidth:
        intensities = df['CDMS/JPL Intensity'].to_numpy()
        lws = np.power(10, intensities) * lw_scale

    # generate figure
    if args.dark:
        plt.style.use(['dark_background'])
    fig = plt.figure(figsize=(8, 4), dpi=150)
    ax = fig.add_subplot(111)

    ymin = 0
    ymax = 1

    freqs = df['Freq-MHz(rest frame,redshifted)'].to_numpy()

    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left=False,      # ticks along the bottom edge are off
        right=False,         # ticks along the top edge are off
        labelleft=False
    ) # labels along the bottom edge are off
    ax.set_xlim([fmin, fmax])
    ax.set_ylim([0, 1])
    ax.set_xlabel('frequency (MHz)')
    if args.logscale:
        ax.set_xscale('log')

    # plot
    if userainbow and args.linewidth:
        ax.vlines(freqs, ymin=ymin, ymax=ymax, colors=rainbow(color_norm(freqs)), linewidths=lws, cmap=rainbow, alpha=args.alpha)
    elif userainbow:
        ax.vlines(freqs, ymin=ymin, ymax=ymax, colors=rainbow(color_norm(freqs)), cmap=rainbow, alpha=args.alpha)
    elif args.linewidth:
        ax.vlines(freqs, ymin=ymin, ymax=ymax, linewidths=lws, alpha=args.alpha)
    else:
        ax.vlines(freqs, ymin=ymin, ymax=ymax, alpha=args.alpha)

    plt.tight_layout()
    plt.savefig(args.saveto, dpi=300)
    if args.show:
        plt.show()
    plt.close()
    pass


if __name__ == '__main__':
    main()