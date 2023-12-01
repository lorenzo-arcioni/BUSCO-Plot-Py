# -*- coding: utf-8 -*-

#Importing libraries
import matplotlib.pyplot as plt
import pandas as pd
from buscoplotpy.graphics.chromosome import Chromosome

def synteny_plot(#df_1: pd.DataFrame, 
                 #df_2: pd.DataFrame,
                 karyotype_1: pd.DataFrame,
                 karyotype_2: pd.DataFrame,
                 palette: str in ['green', 'azure'] = 'green',
                 title: str = 'Synteny plot',
                 dim: int = 2,
                 dpi: int = 300):

    """
    Plots a synteny diagram using the provided data frame.

    Parameters:
        - df (pd.DataFrame): The data frame containing the synteny information.
        - x_start (float): The starting x-coordinate of the synteny diagram.
        - x_end (float): The ending x-coordinate of the synteny diagram.
        - y_start (float): The starting y-coordinate of the synteny diagram.
        - y_end (float): The ending y-coordinate of the synteny diagram.
        - horizontal (bool, optional): Whether the synteny diagram is horizontal. Defaults to True.

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
        
    # Create the synteny diagram
    #fig, ax = plt.subplots()

    # Read the karyotype file into a DataFrame
    karyotype = pd.concat([karyotype_1, karyotype_2], ignore_index=True)

    # Lowercase the column names
    karyotype.columns = karyotype.columns.str.lower()

    # Set the x and y limits
    X_lim = 100
    Y_lim = 10 + 280 + 10

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(20, 20*Y_lim/X_lim), dpi=dpi)

    # Axis off
    ax.axis('off')

    # Set the x and y limits of the plot
    ax.set_ylim([0, Y_lim])
    ax.set_xlim([0, X_lim])

    # Insert the plot title
    ax.text(X_lim / 2, Y_lim - 1, title, fontsize=20, ha='center')

    # Calculate the maximum length of the chromosome name
    chr_max_len = len(max(karyotype['chr'], key=len))

    # Get the maximum length of the chromosome
    chr_max_dim = karyotype['end'].max()

    step = 0

    # Plot the karyotypes
    for index, row in karyotype.iterrows():

        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = 30
        x_end   = x_start + dim

        y_start = 10 + step
        y_end   = y_start + chr_dim * (Y_lim*9/10) / chr_max_dim

        step += y_end

        # Get the color
        color = 'gray'

        C = Chromosome(x_start=x_start,
                       x_end=x_end,
                       y_start=y_start,
                       y_end=y_end,
                       horizontal=True
        )

        C.add_label(x=(x_start + x_end) / 2, y=y_end - 5, text=row['chr'], ha='center', va='center')

        C.plot(ax)

    return karyotype

    

