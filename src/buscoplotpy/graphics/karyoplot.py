# -*- coding: utf-8 -*-

#Importing libraries
import matplotlib.pyplot as plt
import pandas as pd
from buscoplotpy.graphics.chromosome import Chromosome

from matplotlib.patches import Wedge, Rectangle

def karyoplot(karyotype_file: str, 
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
        karyotype_file (str): The path to the karyotype file.
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

    # Define the colors
    green = ['green', 'gray', 'black']
    azure = ['#5999ff', '#ffff05', '#21211d']
    selected = []
    
    # Selecting the right palette
    if palette == 'green':
        selected = green
    elif palette == 'azure':
        selected = azure

    def get_color(status: str, palette: str = 'green') -> str:

        """
        Get the color based on the status of the item.
        Parameters:
            item (dict): The item containing the status.
        Returns:
            str: The color corresponding to the status.
        """
        
        # Reurn the color based on the palette/status
        if status == 'Complete':
            return selected[0]
        elif status == 'Duplicated':
            return selected[1]
        else:
            return selected[2]

    # Read the karyotype file into a DataFrame
    karyotype = pd.read_csv(karyotype_file, sep="\t")

    # Lowercase the column names
    karyotype.columns = karyotype.columns.str.lower()

    # Remove rows where status is 'Missing'
    fulltable = fulltable[fulltable['status'] != 'Missing']

    # Extract the sequence name from the 'sequence' column
    fulltable.loc[:, 'sequence'] = fulltable['sequence'].map(lambda x: x.split(':')[0])

    # If the number of chromosomes is greater than chr_limit,
    #   then select the most significant chromosomes

    if len(karyotype) > chrs_limit:

        if len(fulltable) == 0:
            karyotype = karyotype.iloc[:chrs_limit, :]
        else:
            karyotype.set_index('chr', inplace=True)

            # Select the most significant chromosomes (the chromosomes with more hits)
            first_chrs = fulltable['sequence'].value_counts().index.to_list()[:chrs_limit]
            karyotype = karyotype.loc[first_chrs].sort_values(by='end', ascending=False)
            karyotype = karyotype.reset_index()

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
    ax.text(X_lim / 2, Y_lim - 1, title, fontsize=20, ha='center')

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
        x_end   = x_start + chr_dim * (X_lim*9/10) / chr_max_dim
        y_start = (len(karyotype) - index) * dim
        y_end   = y_start + dim / 2

        C = Chromosome(x_start, x_end, y_start, y_end)
        C.add_label(x=0.0, y=(y_start + y_end) / 2, text=row['chr'], horizontalalignment='center', verticalalignment='center')
        

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
            C.add_region(anchor_point=anchor_point, width=width, height=height, color=get_color(item['status'], palette), linewidth=1)
        
        # Plot the chromosome
        C.plot(ax)

    # Write the legend
    plt.legend(handles=[Rectangle((0,0),1,1, color=selected[0]), 
                        Rectangle((0,0),1,1, color=selected[1]), 
                        Rectangle((0,0),1,1, color=selected[2])],
                        labels=['Complete', 'Duplicated', 'Fragmented'], 
                        loc='upper right'
    )

    # Save and show the plot
    if output_file:
        plt.savefig(output_file, dpi=dpi, bbox_inches=bbox_inches)

    if plt_show:
        plt.show()
    
    plt.close()
