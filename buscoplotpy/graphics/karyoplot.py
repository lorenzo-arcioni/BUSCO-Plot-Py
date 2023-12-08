# -*- coding: utf-8 -*-

#Importing libraries
import matplotlib.pyplot as plt
import pandas as pd

from chromosome import Chromosome
from matplotlib.patches import Rectangle

# Define the colors
GREEN = {'Complete':'green', 'Duplicated':'gray', 'Fragmented':'black'}
AZURE = {'Complete':'#50c7fa', 'Duplicated':'gray', 'Fragmented':'black'}

# Define constants
CHR_FACTOR = 9.0 / 10.0

def karyoplot(karyotype: pd.DataFrame, 
              output_file: str = '', 
              title: str = 'Karyoplot', 
              fulltable: pd.DataFrame = None, 
              dpi: int = 300, 
              chrs_limit: int = 30, 
              plt_show: bool = False,
              palette: str in ['green', 'azure'] = 'green',
              bbox_inches: str = 'tight',
              dim: int = 2
) -> None:

    """
    Plot a karyotype based on the karyotype file and the BUSCO fulltable.

    Parameters:
        karyotype (pd.DataFrame): The karyotype DataFrame.
        output_file (str, optional): The path to save the output plot.
        title (str, optional): The title of the plot.
        fulltable (pd.DataFrame): The BUSCO's full table DataFrame.
        dpi (int, optional): The DPI (dots per inch) of the output plot. Default is 300.
        chrs_limit (int, optional): The maximum number of chromosomes to plot. Default is 30.
        plt_show (bool, optional): Whether to show the plot. Default is False.

    Output:
        - The karyotype plot in png format.

    Returns:
        None
    """
    
    # Selecting the right palette
    if palette == 'green':
        selected = GREEN
    elif palette == 'azure':
        selected = AZURE

    # Lowercase the column names
    karyotype.columns = karyotype.columns.str.lower()

    # Remove rows where status is 'Missing'
    fulltable = fulltable[fulltable['status'] != 'Missing']

    # If the number of chromosomes is greater than chr_limit,
    #   then select the most significant chromosomes
    if len(karyotype) > chrs_limit:

        #if len(fulltable) == 0:
            karyotype = karyotype.iloc[:chrs_limit, :]
        #else:
        #    karyotype.set_index('chr', inplace=True)

            # Select the most significant chromosomes (the chromosomes with more hits)
        #    first_chrs = fulltable['sequence'].value_counts().index.to_list()[:chrs_limit]
        #    karyotype = karyotype.loc[first_chrs].sort_values(by='end', ascending=False)
        #    karyotype = karyotype.reset_index()

    # Calculate the limits of the plot
    X_lim = 100
    Y_lim = dim * len(karyotype) + dim + 5

    # Create a new figure and axis
    fig, ax   = plt.subplots(figsize=(20, 20*Y_lim/X_lim), dpi=dpi)

    # Turn off the axis
    ax.axis('off')

    # Set the x and y limits of the plot
    ax.set_xlim([0, X_lim])
    ax.set_ylim([0, Y_lim])

    # Insert the plot title
    ax.text(X_lim / 2, Y_lim - 1, karyotype['organism'][0] + ' ' + title, fontsize=20, ha='center')

    # Calculate the maximum length of the chromosome name
    chr_max_len = len(max(karyotype['chr'], key=len))

    # Get the maximum length of the chromosome
    chr_max_dim = karyotype['end'].max()

    # Plot the karyotypes
    for index, row in karyotype.iterrows():
        
        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = chr_max_len / 2
        x_end   = x_start + chr_dim * (X_lim * CHR_FACTOR) / chr_max_dim
        y_start = (len(karyotype) - index) * dim
        y_end   = y_start + dim / 2

        # Create the chromosome
        C = Chromosome(x_start=x_start, x_end=x_end, y_start=y_start, y_end=y_end, size=chr_dim)

        # Add the name of the chromosome
        C.add_label(x=0.0, y=(y_start + y_end) / 2, text=row['chr'], ha='center', va='center')
        

        # Create all chromosome region
        for i, item in fulltable[fulltable['sequence'] == row.chr].iterrows():

            # Define the coordinates for the region
            converted_start_pos = item['gene_start'] * (x_end - x_start) / chr_dim
            converted_end_pos   = item['gene_end']   * (x_end - x_start) / chr_dim

            anchor_point = (x_start + converted_start_pos, y_start)
            width        = converted_end_pos - converted_start_pos
            height       = y_end - y_start

            #:                +------------------+
            #:                |                  |
            #:              height               |
            #:                |                  |
            #:               (xy)---- width -----+

            # Add the seleted region to the chromosome
            C.add_region(anchor_point=anchor_point, width=width, height=height, color=selected[item['status']], linewidth=1)
        
        # Plot the chromosome
        C.plot(ax)

    # Write the legend
    plt.legend(handles=[Rectangle((0,0),1,1, color=selected['Complete']), 
                        Rectangle((0,0),1,1, color=selected['Duplicated']), 
                        Rectangle((0,0),1,1, color=selected['Fragmented'])],
                        labels=['Complete', 'Duplicated', 'Fragmented'], 
                        loc='upper right'
    )

    # Save and show the plot
    if output_file:
        plt.savefig(output_file, dpi=dpi, bbox_inches=bbox_inches)

    if plt_show:
        plt.show()
    
    plt.close()
