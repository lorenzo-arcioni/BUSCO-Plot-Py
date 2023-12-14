# -*- coding: utf-8 -*-
# This file is part of the Busco software suite.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Rectangle
from scipy.interpolate import splrep, splev
from scipy import interpolate

AZURE  = '#5795ad'
GREEN  = '#64ad57'
ORANGE = '#cc6535'
BLACK  = '#8a8a8a'
PURPLE = '#be8adb'

def chromoplot(karyotype: pd.DataFrame, 
               genes_dataframe: pd.DataFrame,
               title: str = 'Chromoplot',
               bin_number: int = 100,
               dpi: int = 300,
               plt_show: bool = False,
               output_path: str = '',
               targets: list = ['gene', 'mRNA', 'CDS', 'exon']
    ) -> None:

    """
    Plot the karyotype and gene density of each chromosome on separate subplots.
    """

    karyotype.columns = karyotype.columns.str.lower()

    assert 'chr' in karyotype.columns, 'The karyotype DataFrame must contain the "chr" column.'
    assert 'end' in karyotype.columns, 'The karyotype DataFrame must contain the "end" column.'
    assert 'start' in karyotype.columns, 'The karyotype DataFrame must contain the "start" column.'

    number_of_graphs = karyotype.shape[0]

    fig, ax = plt.subplots(ncols=1, nrows=number_of_graphs, figsize=(24, number_of_graphs * 2 + 3), squeeze=False)

    # set the spacing between subplots
    plt.subplots_adjust(#left  = 0.125,  # the left side of the subplots of the figure
    #                    #right = 0.9,    # the right side of the subplots of the figure
    #                    bottom = 0.05,   # the bottom of the subplots of the figure
    #                    #top = 1,      # the top of the subplots of the figure
    #                    #wspace = 0.2,   # the amount of width reserved for blank space between subplots
                         hspace = 0.8,   # the amount of height reserved for white space between subplots
    )

    ax[0, 0].set_title(title, color='black', rotation='horizontal', va='center', pad=35, fontsize=20)

    dict={}

    for index, row in karyotype.iterrows():

        bbox=ax[index, 0].get_position()

        plt.figtext(bbox.p0[0] - len(row['chr']) / 100.0, (bbox.p0[1] + bbox.p1[1]) / 2.0, row['chr'], fontsize=15)

        for target in targets:
        
            size = row['end']
            bins = np.linspace(0, size, bin_number + 1)
            counts = []

            for i in range(len(bins) - 1):
                number_of_matches = len(genes_dataframe[(genes_dataframe['type'] == target) & (genes_dataframe['sequence'] == row['chr'])].loc[
                                                        ((genes_dataframe['start'] <= bins[i]) & (genes_dataframe['end'] >= bins[i])) | 
                                                        ((genes_dataframe['start'] <= bins[i+1]) & (genes_dataframe['end'] >= bins[i+1])) |
                                                        ((genes_dataframe['start'] >= bins[i]) & (genes_dataframe['end'] <= bins[i+1])), :])
                counts.append(number_of_matches)

            counts.append(counts[-1])

            bspline = interpolate.make_interp_spline(bins, counts)
        
            X = np.linspace(0, size, bin_number**2)
            Y = bspline(X)

            ax[index, 0].set_xlim([0, size])
            ax[index, 0].set_ylim([0, max(max(counts), 1)])

            if target == 'gene':
                ax[index, 0].fill_between(X, 0, Y, color=GREEN, alpha=0.5)
            elif target == 'mRNA':
                ax[index, 0].fill_between(X, 0, Y, color=AZURE, alpha=0.5)
            elif target == 'CDS':
                ax[index, 0].fill_between(X, 0, Y, color=BLACK, alpha=0.5)
            elif target == 'exon':
                ax[index, 0].fill_between(X, 0, Y, color=ORANGE, alpha=0.5)

        # Add grid
        ax[index, 0].grid(True)
        ax[index, 0].set_xlabel('Chromosome position', fontsize=14)
        ax[index, 0].set_ylabel('Counts', fontsize=14)

    # Write the legend
    ax[0, 0].legend(handles=[Rectangle((0,0),1,1, color=GREEN), 
                          Rectangle((0,0),1,1, color=AZURE), 
                          Rectangle((0,0),1,1, color=BLACK),
                          Rectangle((0,0),1,1, color=ORANGE),
                          Rectangle((0,0),1,1, color=PURPLE),],
                          labels=['Gene', 'mRNA', 'CDS', 'exon', 'Gene + mRNA'], 
                          bbox_to_anchor=(1.1, 1)
    )

    if output_path:
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')

    if plt_show:
        plt.show()

    plt.close()

def chromoplot_details(genes_dataframe: pd.DataFrame,
                       title: str = 'Chromoplot',
                       dpi: int = 300,
                       plt_show: bool = False,
                       output_path: str = '',
    ) -> None:

    fig, axd = plt.subplot_mosaic(
        "AB;CC",
        figsize=(18, 10),
    )
    colors = [ORANGE, BLACK, GREEN, AZURE]

    ########################## First plot ##########################

    x_axis = genes_dataframe['type'].unique()
    y_axis = genes_dataframe['type'].value_counts().values

    axd['A'].set_title(title, color='black', rotation='horizontal', va='center', ha='center', pad=35, fontsize=16)

    # Add grid
    axd['A'].grid(True)
    axd['A'].set_xlabel('Feature type', fontsize=14)
    axd['A'].set_ylabel('Counts', fontsize=14)

    vc = genes_dataframe['type'].value_counts()

    axd['A'].set_ylim(0, vc.max() + 15)

    x_axis = vc.index
    y_axis = vc.values

    axd['A'].bar(x=x_axis, height=y_axis, color=colors, alpha=0.8, width=0.4)

    for i in range(len(x_axis)):
        axd['A'].annotate(y_axis[i], xy=(x_axis[i], y_axis[i]), ha='center', va='bottom', fontsize=12)

    ########################## Second plot ##########################

    N = 18
    ind = np.arange(N) 
    width = 0.25

    # Add grid
    axd['C'].grid(True)
    axd['C'].set_xlabel('Chromosome', fontsize=14)
    axd['C'].set_ylabel('Counts', fontsize=14)

    gb = genes_dataframe.groupby(['sequence', 'type']).size()

    x_axis = gb.index.get_level_values(0).unique()

    for target, color, idx in zip(['gene', 'mRNA', 'CDS', 'exon'], colors, range(4)):

        y_axis = gb.xs(target, level=1).values

        axd['C'].plot(ind, y_axis, width, color=colors[idx], alpha=0.8)
    
    axd['C'].set_xticks(ind, labels=x_axis, rotation=45)

    # Write the legend
    axd['C'].legend(handles=[Rectangle((0,0),1,1, color=GREEN), 
                             Rectangle((0,0),1,1, color=AZURE), 
                             Rectangle((0,0),1,1, color=BLACK),
                             Rectangle((0,0),1,1, color=ORANGE),],
                             labels=['Gene', 'mRNA', 'CDS', 'exon'], 
                             bbox_to_anchor=(1, 1)
    )

    ########################## Third plot ##########################

    # Create the plot of distribution gene length

    axd['B'].set_title('Gene length distribution', color='black', rotation='horizontal', va='center', ha='center', pad=35, fontsize=16)

    # Add grid
    axd['B'].grid(True)

    gb = genes_dataframe.groupby('sequence').size()

    x_axis = gb.index

    y_axis = gb.values

    axd['B'].set_xlabel('Chromosome', fontsize=14)

    axd['B'].set_ylabel('Counts', fontsize=14)

    # Create the dotplot

    axd['B'].plot(x_axis, y_axis, 'o', color=ORANGE, alpha=0.8)

    # Write the legend
    #ax.legend(handles=[Rectangle((0,0),1,1, color=GREEN), 
    #                   Rectangle((0,0),1,1, color=AZURE), 
    #                   Rectangle((0,0),1,1, color=BLACK),
    #                   Rectangle((0,0),1,1, color=ORANGE),],
    #                   labels=['Gene', 'mRNA', 'CDS', 'exon', 'Gene + mRNA'], 
    #                   bbox_to_anchor=(1, 1)
    #)

    if output_path:
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')

    if plt_show:
        plt.show()