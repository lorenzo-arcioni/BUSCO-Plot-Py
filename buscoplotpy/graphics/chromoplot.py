# -*- coding: utf-8 -*-
# This file is part of the Busco software suite.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from scipy.interpolate import splrep, splev

AZURE  = '#90afe0'
GREEN  = '#6aa683'
RED    = '#c28484'
BLACK  = '#8a8a8a'
PURPLE = '#be8adb'

def chromoplot(karyotype: pd.DataFrame, 
               genes_dataframe: pd.DataFrame,
               title: str = 'Chromoplot',
               bin_number: int = 100,
               s: int = 15,
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

    fig, ax = plt.subplots(ncols=1, nrows=number_of_graphs, figsize=(22, number_of_graphs * 2 + 3), dpi=dpi)

    # set the spacing between subplots
    plt.subplots_adjust(#left  = 0.125,  # the left side of the subplots of the figure
    #                    #right = 0.9,    # the right side of the subplots of the figure
    #                    bottom = 0.05,   # the bottom of the subplots of the figure
    #                    #top = 1,      # the top of the subplots of the figure
    #                    #wspace = 0.2,   # the amount of width reserved for blank space between subplots
                         hspace = 0.8,   # the amount of height reserved for white space between subplots
    )

    ax[0].set_title(title, color='black', rotation='horizontal', va='center', pad=35, fontsize=20)

    for index, row in karyotype.iterrows():

        bbox=ax[index].get_position()

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
            X_Y_Spline = splrep(bins, counts, s=s)

            X = bins
            Y = splev(X, X_Y_Spline)

            ax[index].set_xlim([0, size])
            ax[index].set_ylim([0, max(max(counts), 1)])

            if target == 'gene':
                ax[index].fill_between(X, 0, Y, color=GREEN, alpha=0.2)
            elif target == 'mRNA':
                ax[index].fill_between(X, 0, Y, color=AZURE, alpha=0.2)
            elif target == 'CDS':
                ax[index].fill_between(X, 0, Y, color=BLACK, alpha=0.2)
            elif target == 'exon':
                ax[index].fill_between(X, 0, Y, color=RED, alpha=0.2)
            
        ax[index].set_xlabel('Chromosome position', fontsize=14)
        ax[index].set_ylabel('Counts', fontsize=14)

    # Write the legend
    ax[0].legend(handles=[Rectangle((0,0),1,1, color=GREEN), 
                          Rectangle((0,0),1,1, color=AZURE), 
                          Rectangle((0,0),1,1, color=BLACK),
                          Rectangle((0,0),1,1, color=RED),
                          Rectangle((0,0),1,1, color=PURPLE),],
                          labels=['Gene', 'mRNA', 'CDS', 'exon', 'Gene + mRNA'], 
                          bbox_to_anchor=(1.1, 1)
    )

    if output_path:
        plt.savefig(output_path, dpi=dpi, bbox_inches='tight')

    if plt_show:
        plt.show()

    plt.close()