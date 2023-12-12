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
               s: int = 15) -> None:

    """
    Plot the karyotype and gene density of each chromosome on separate subplots.
    """

    number_of_graphs = karyotype.shape[0]

    fig, ax = plt.subplots(ncols=1, nrows=number_of_graphs, figsize=(22, number_of_graphs * 1.5))

    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                        bottom=1.0, 
                        right=0.9, 
                        top=2.0, 
                        wspace=0.4, 
                        hspace=0.5)

    ax[0].set_title(title, y=1.5, fontsize=18)

    for index, row in karyotype.iterrows():

        for target in ['gene', 'mRNA', 'CDS', 'exon']:
        
            size = row['end']
            bins = np.linspace(0, size, bin_number)
            counts = []

            for i in range(len(bins) - 1):
                number_of_matches = len(genes_dataframe[(genes_dataframe['type'] == target) & (genes_dataframe['sequence'] == row['chr'])].loc[
                                            ((genes_dataframe['start'] <= bins[i]) & (genes_dataframe['end'] >= bins[i])) | 
                                            ((genes_dataframe['start'] <= bins[i+1]) & (genes_dataframe['end'] >= bins[i+1])) |
                                            ((genes_dataframe['start'] >= bins[i]) & (genes_dataframe['end'] <= bins[i+1])), :])
                counts.append(number_of_matches)

            X_Y_Spline = splrep(bins[1:], counts, s=s)

            X = bins
            Y = splev(X, X_Y_Spline)

            ax[index].set_xlim([0, size])
            ax[index].set_ylim([0, max(max(counts), 1)])
            #ax[index].plot(X, Y, color='black', linewidth=1)

            if target == 'gene':
                ax[index].fill_between(X, 0, Y, color='red', alpha=0.2)
            elif target == 'mRNA':
                ax[index].fill_between(X, 0, Y, color='blue', alpha=0.2)
            elif target == 'CDS':
                ax[index].fill_between(X, 0, Y, color='black', alpha=0.2)
            elif target == 'exon':
                ax[index].fill_between(X, 0, Y, color='green', alpha=0.2)
            
        ax[index].set_xlabel('Chromosome position', fontsize=14)
        ax[index].set_ylabel('Counts', fontsize=14)
        ax[index].set_title(row['chr'], color='black', rotation='horizontal', va='center', x=-0.1,y=0.5)
        # Write the legend
    ax[0].legend(handles=[Rectangle((0,0),1,1, color=RED), 
                                Rectangle((0,0),1,1, color=AZURE), 
                                Rectangle((0,0),1,1, color=GREEN),
                                Rectangle((0,0),1,1, color=BLACK),
                                Rectangle((0,0),1,1, color=PURPLE),],
                                labels=['Gene', 'mRNA', 'CDS', 'exon', 'Gene + mRNA'], 
                                bbox_to_anchor=(1.1, 1)
    )

    plt.tight_layout()

    plt.show()