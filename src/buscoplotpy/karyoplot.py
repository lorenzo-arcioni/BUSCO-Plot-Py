#Importing libraries
import matplotlib.pyplot as plt
import pandas as pd
import math as mt
from buscoplotpy.load_busco_fulltable import load_busco_fulltable

from matplotlib.patches import Wedge, Rectangle

def karyoplot(karyotype_file: str, 
              full_table_file: str = '', 
              output_file: str = 'karyoplot.png', 
              title: str = 'Karyoplot', 
              busco_fulltable: pd.DataFrame = None, 
              dpi: int = 300, 
              chrs_limit: int = 30, 
              plt_show: bool = False,
              palette: str in ['green', 'azure'] = 'green',
            ) -> None:

    """
    Plot a karyotype based on the karyotype file and the BUSCO fulltable.

    Parameters:
        karyotype_file (str): The path to the karyotype file.
        full_table_file (str, optional): The path to the BUSCO's full table.
        output_file (str, optional): The path to save the output plot.
        title (str, optional): The title of the plot.
        busco_fulltable (str, optional): The BUSCO's full table DataFrame.
        dpi (int, optional): The DPI (dots per inch) of the output plot. Default is 300.
        chrs_limit (int, optional): The maximum number of chromosomes to plot. Default is 30.
        plt_show (bool, optional): Whether to show the plot. Default is False.

    Output:
        - The karyotype plot in png format.
    Returns:
        None
    """

    # Define the dimensions of the karyotype plot
    DIM = 6

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
        elif status == 'Partial':
            return selected[1]
        else:
            return selected[2]

    # Read the karyotype file into a DataFrame
    karyotype = pd.read_csv(karyotype_file, sep="\t")

    # Load the BUSCO fulltable
    if busco_fulltable is not None:
        fulltable = busco_fulltable
    elif full_table_file == '':
        raise ValueError('Please provide BUSCO full table DataFrame or a path to the BUSCO full table.')
    else:
        fulltable = load_busco_fulltable(path=full_table_file)

    # Remove rows where status is 'Missing'
    fulltable = fulltable[fulltable['status'] != 'Missing']

    # Extract the sequence name from the 'sequence' column
    fulltable.loc[:, 'sequence'] = fulltable['sequence'].map(lambda x: x.split(':')[0])
    ##########################################################################################################

    # If the number of chromosomes is greater than chr_limit,
    #   then sort the karyotype DataFrame by the most hitting BUSCOs chromosome
    if len(karyotype) > chrs_limit:
        karyotype.set_index('chr', inplace=True)

        # Select the most significant chromosomes (the chromosomes with more hits)
        first_chrs = fulltable['sequence'].value_counts().index.to_list()[:chrs_limit]
        karyotype = karyotype.loc[first_chrs].sort_values(by='end', ascending=False)
        karyotype = karyotype.reset_index()

    ###########################################################################################################
    # Approximate the length of the karyotype plot
    approx_height = ((len(karyotype) * 1.7 / 100) + 1.8) * mt.sqrt(len(karyotype))

    # Create a new figure and axis
    fig, ax   = plt.subplots(figsize=(20, approx_height))

    # Turn off the axis
    ax.axis('off')

    # Calculate the limits of the plot
    X_lim = DIM * len(max(karyotype['chr'], key=len))
    Y_lim = DIM * len(karyotype) + 20

    # Set the x and y limits of the plot
    ax.set_xlim([0, X_lim])
    ax.set_ylim([0, Y_lim])

    # Insert the plot title
    ax.text(X_lim / 2, Y_lim - 4, title, fontsize=20, ha='center')

    # Calculate the maximum length of the chromosome name
    chr_max_len = len(max(karyotype['chr'], key=len))

    # Get the maximum length of the karyotype
    chr_max_dim = karyotype['end'].max()

    # Plot the karyotypes
    for index, row in karyotype.iterrows():
        
        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = chr_max_len * DIM * 0.13
        x_end   = x_start + chr_dim * (X_lim*7.5/10) / chr_max_dim
        y_start = (len(karyotype) - index) * DIM
        y_end   = y_start + (DIM * 0.45)

        # Add the chromosome name to the plot
        ax.text(0.5, y_start, row['chr'])

        #plot the karyotypes
        for i, item in fulltable[fulltable['sequence'] == row.chr].iterrows():

            # Define the coordinates for the rectangle
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

            # Create the rectangle based on converted coordinates
            re = Rectangle(xy=anchor_point, width=width, height=height, color=get_color(item['status'], palette), linewidth=1)
            ax.add_patch(re)
        
        # Calculate the center and radius of the chromosome semicircles
        center_y = (y_end + y_start)/2.0
        radius   = (y_end - y_start)/2.0

        # Calculate the angles of the semicircles
        theta1   = -90.0
        theta2   =  90.0

        # Create the start and the end semicircles
        w1 = Wedge((x_start, center_y), radius, theta2, theta1, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)
        w2 = Wedge((x_end, center_y),   radius, theta1, theta2, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)

        # Add the semicircles on chromosomes
        ax.add_patch(w1)
        ax.add_patch(w2)

        # Add the chromosome lines
        ax.plot([x_start, x_end], [y_start, y_start], ls='-', color='black', linewidth=1)
        ax.plot([x_start, x_end], [y_end, y_end],     ls='-', color='black', linewidth=1)

    # Write the legend
    plt.legend(handles=[Rectangle((0,0),1,1, color=selected[0]), 
                        Rectangle((0,0),1,1, color=selected[1]), 
                        Rectangle((0,0),1,1, color=selected[2])],
                        labels=['Complete', 'Fragmented', 'Missing'], 
                        loc='upper right'
    )

    # Save and show the plot
    plt.savefig(output_file, dpi=dpi)

    if plt_show:
        plt.show()
    
    plt.close()