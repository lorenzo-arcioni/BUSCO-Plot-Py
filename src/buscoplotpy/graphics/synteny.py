# -*- coding: utf-8 -*-

#Importing libraries
import matplotlib.pyplot as plt
import pandas as pd
from buscoplotpy.graphics.chromosome import Chromosome
from buscoplotpy.graphics.link import Link

CHR_DISTANCE = 2
CHR_FACTOR = 90

# Set the x and y limits
X_lim = 180
Y_lim = 100

def plot_left_karyotype(karyotype: pd.DataFrame, dim: int, ax) -> dict:

    # Initialize the step
    step = 0

    # Get the chromosome length sum
    chr_len_sum = karyotype['end'].sum()

    # Left chromosomes dict
    C = {}

    # Plot the karyotypes
    for index, row in karyotype.iterrows():

        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = len(max(karyotype['chr'], key=len))
        x_end   = x_start + dim

        y_start = CHR_DISTANCE + step
        y_end   = y_start + chr_dim * (CHR_FACTOR - CHR_DISTANCE * len(karyotype)) / chr_len_sum

        step = y_end

        # Get the color
        color = 'gray'

        c = Chromosome(x_start=x_start,
                       x_end=x_end,
                       y_start=y_start,
                       y_end=y_end,
                       size=chr_dim,
                       horizontal=False,
                       round_edges=True
        )

        c.add_label(x=3, y=(y_start + y_end) / 2, text=row['chr'], ha='center', va='center')

        c.plot(ax)

        C[row['chr']] = c
    
    return C

def plot_right_karyotype(karyotype: pd.DataFrame, dim: int, ax) -> dict:

    # Initialize the step
    step = 0

    # Get the chromosome length sum
    chr_len_sum = karyotype['end'].sum()

    # Right chromosomes dict
    C = {}

    # Plot the karyotypes
    for index, row in karyotype.iterrows():

        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = X_lim - len(max(karyotype['chr'], key=len)) - dim
        x_end   = x_start + dim

        y_start = CHR_DISTANCE + step
        y_end   = y_start + chr_dim * (CHR_FACTOR - CHR_DISTANCE * len(karyotype)) / chr_len_sum

        step = y_end

        # Get the color
        color = 'gray'

        c = Chromosome(x_start=x_start,
                       x_end=x_end,
                       y_start=y_start,
                       y_end=y_end,
                       size=chr_dim,
                       horizontal=False,
                       round_edges=True
        )

        c.add_label(x=X_lim - 3, y=(y_start + y_end) / 2, text=row['chr'], ha='center', va='center')

        c.plot(ax)

        C[row['chr']] = c
    
    return C



def generate_links(ft_1: pd.DataFrame, 
                   ft_2: pd.DataFrame, 
                   right_chromosomes: dict, 
                   left_chromosomes: dict, 
                   color: str, 
                   ax: plt.Axes
) -> None:

    """
    Generates the links between the two organisms.

    Parameters:
        - df_1 (pd.DataFrame): The first data frame.
        - df_2 (pd.DataFrame): The second data frame.

    Returns:
        - links (pd.DataFrame): The links between the two data frames.
    """

    ft_1 = ft_1[ft_1['status'] == 'Complete']
    ft_2 = ft_2[ft_2['status'] == 'Complete']

    # Merge the two data frames
    df = pd.merge(ft_1, ft_2, on='busco_id', how='inner')

    # Initialize the links
    links = []

    # Iterate over the rows
    for index, row in df.iterrows():

        # Generate the link
        link = Link(C1=left_chromosomes[row['sequence_x']], C2=right_chromosomes[row['sequence_y']], p_1=row['gene_start_x'], p_2=row['gene_start_y'], color=color)

        link.plot(ax)

def vertical_synteny_plot(ft_1: pd.DataFrame, 
                          ft_2: pd.DataFrame,
                          karyotype_1: pd.DataFrame,
                          karyotype_2: pd.DataFrame,
                          palette: str in ['gray'] = 'gray',
                          title: str = 'Synteny plot',
                          dim: int = 2,
                          dpi: int = 300
):

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
    else:
        selected = palette

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

    # Lowercase the column names
    karyotype_1.columns = karyotype_1.columns.str.lower()
    karyotype_2.columns = karyotype_2.columns.str.lower()

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(18, 10), dpi=dpi)

    # Axis off
    ax.axis('off')

    # Set the x and y limits of the plot
    ax.set_ylim([0, Y_lim])
    ax.set_xlim([0, X_lim])

    # Insert the plot title
    ax.text(X_lim / 2, Y_lim - 3, title, fontsize=20, ha='center')

    left_chromosomes   = plot_left_karyotype(karyotype_1, dim, ax)
    right_chromosomes  = plot_right_karyotype(karyotype_2, dim, ax)

    generate_links(ft_1, ft_2, right_chromosomes, left_chromosomes, color='gray', ax=ax)

