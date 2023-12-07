# -*- coding: utf-8 -*-

#Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Import the chromosome and link classes
from buscoplotpy.graphics.chromosome import Chromosome
from buscoplotpy.graphics.link import Link

# Set the constants
CHR_DISTANCE = 2
CHR_FACTOR   = 0.99

# Set the x and y limits
VERTICAL_X_LIM   = 0
VERTICAL_Y_LIM   = 0
HORIZONTAL_X_LIM = 0
HORIZONTAL_Y_LIM = 0

def generate_left_karyotype(karyotype: pd.DataFrame, dim: int, round_edges: bool) -> dict:

    """
    Plot the left karyotype chromosomes.

    Parameters:
        - karyotype: pandas DataFrame containing information about the chromosomes
        - dim: dimension of the chromosomes
        - round_edges: flag indicating whether to round the edges of the chromosomes

    Returns:
        - C: A dictionary mapping chromosome names to their corresponding Chromosome objects.
    """

    # Initialize the step
    step = 0

    # Get the chromosome length sum
    chr_len_sum = karyotype['end'].sum()

    # Left chromosomes dictionary
    C = {}

    # Get chromosome color
    if 'color' in karyotype.columns:
        color = karyotype['color'][0]
    else:
        color = ''

    # Plot the karyotypes
    for index, row in karyotype.iterrows():

        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = len(max(karyotype['chr'], key=len))
        x_end   = x_start + dim

        y_start = CHR_DISTANCE + step
        y_end   = y_start + chr_dim * (VERTICAL_Y_LIM * 0.9 - CHR_DISTANCE * len(karyotype)) / chr_len_sum

        step = y_end

        # Create a Chromosome object
        c = Chromosome(x_start=x_start,
                       x_end=x_end,
                       y_start=y_start,
                       y_end=y_end,
                       size=chr_dim,
                       horizontal=False,
                       round_edges=round_edges,
                       color=color
        )

        # Add the chromosome label
        c.add_label(x=3, y=(y_start + y_end) / 2, text=row['chr'], ha='center', va='center')

        # Add the chromosome to the dictionary
        C[row['chr']] = c
    
    return C

def generate_right_karyotype(karyotype: pd.DataFrame, dim: int, round_edges: bool) -> dict:

    """
    Plot the left karyotype chromosomes.

    Parameters:
        - karyotype: pandas DataFrame containing information about the chromosomes
        - dim: dimension of the chromosomes
        - round_edges: flag indicating whether to round the edges of the chromosomes

    Returns:
        - C: A dictionary mapping chromosome names to their corresponding Chromosome objects.
    """

    # Initialize the step
    step = 0

    # Get the chromosome length sum
    chr_len_sum = karyotype['end'].sum()

    # Right chromosomes dict
    C = {}

    # Get chromosome color
    if 'color' in karyotype.columns:
        color = karyotype['color'][0]
    else:
        color = ''

    # Plot the karyotypes
    for index, row in karyotype.iterrows():

        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = VERTICAL_X_LIM - len(max(karyotype['chr'], key=len)) - dim
        x_end   = x_start + dim

        y_start = CHR_DISTANCE + step
        y_end   = y_start + chr_dim * (VERTICAL_Y_LIM * 0.9 - CHR_DISTANCE * len(karyotype)) / chr_len_sum

        step = y_end

        c = Chromosome(x_start=x_end,# This switch is for visualize the colors correctly
                       x_end=x_start,    # This switch is for visualize the colors correctly
                       y_start=y_start,
                       y_end=y_end,
                       size=chr_dim,
                       horizontal=False,
                       round_edges=round_edges,
                       color=color
        )
        
        # Add the chromosome label
        c.add_label(x=VERTICAL_X_LIM - 3, y=(y_start + y_end) / 2, text=row['chr'], ha='center', va='center')
        
        # Add the chromosome to the dictionary
        C[row['chr']] = c

    return C

def generate_bottom_karyotype(karyotype: pd.DataFrame, dim: int, round_edges: bool) -> dict:

    """
    Generate a bottom karyotype plot.

    Args:
        karyotype (pd.DataFrame): DataFrame containing karyotype information.
        dim (int): Dimension of the karyotype plot.
        round_edges (bool): Whether to round the edges of the chromosomes.

    Returns:
        dict: Dictionary containing the generated chromosomes.
    """

    # Initialize the step
    step = 0

    # Get the chromosome length sum
    chr_len_sum = karyotype['end'].sum()

    # Right chromosomes dict
    C = {}

    # Get chromosome color
    if 'color' in karyotype.columns:
        color = karyotype['color'][0]
    else:
        color = ''

    # Plot the karyotypes
    for index, row in karyotype.iterrows():

        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Get the maximum chromosome name length
        max_chr_name_length = len(max(karyotype['chr'], key=lambda x: len(x)))

        # Define the coordinates for the rectangle
        x_start = CHR_DISTANCE + step
        x_end   = x_start + chr_dim * (HORIZONTAL_X_LIM * CHR_FACTOR - CHR_DISTANCE * len(karyotype)) / chr_len_sum

        y_start = max_chr_name_length + 10
        y_end   = y_start + dim

        step = x_end

        c = Chromosome(x_start=x_start,
                       x_end=x_end,
                       y_start=y_start,
                       y_end=y_end,
                       size=chr_dim,
                       horizontal=True,
                       round_edges=round_edges,
                       color=color
        )

        # Add the chromosome label
        c.add_label(x=(x_start + x_end) / 2.0, y=max_chr_name_length, text=row['chr'], rotation=90, ha='center', va='center')
        
        # Add the chromosome to the dictionary
        C[row['chr']] = c

    return C

def generate_up_karyotype(karyotype: pd.DataFrame, dim: int, round_edges: bool) -> dict:

    """
    Generate an upward karyotype plot based on the given karyotype data.

    Args:
        karyotype (pd.DataFrame): DataFrame containing karyotype information.
        dim (int): Dimension of the karyotype plot.
        round_edges (bool): Flag indicating whether to use rounded edges for the chromosomes.

    Returns:
        dict: Dictionary containing the generated karyotype plot.
    """

    # Initialize the step
    step = 0

    # Get the chromosome length sum
    chr_len_sum = karyotype['end'].sum()

    # Get the maximum chromosome name length
    max_chr_name_length = len(max(karyotype['chr'], key=lambda x: len(x)))

    # Right chromosomes dict
    C = {}

    # Get chromosome color
    if 'color' in karyotype.columns:
        color = karyotype['color'][0]
    else:
        color = ''

    # Plot the karyotypes
    for index, row in karyotype.iterrows():

        # Get the dimension of the karyotype
        chr_dim = row['end']

        # Define the coordinates for the rectangle
        x_start = CHR_DISTANCE + step
        x_end   = x_start + chr_dim * (HORIZONTAL_X_LIM * CHR_FACTOR - CHR_DISTANCE * len(karyotype)) / chr_len_sum

        y_start = HORIZONTAL_Y_LIM - max_chr_name_length - 15
        y_end   = y_start + dim

        step = x_end

        c = Chromosome(x_start=x_start,
                       x_end=x_end,
                       y_start=y_end,# This switch is for visualize the colors correctly
                       y_end=y_start,# This switch is for visualize the colors correctly
                       size=chr_dim,
                       horizontal=True,
                       round_edges=round_edges,
                       color=color
        )

        c.add_label(x=(x_start + x_end) / 2.0, y=HORIZONTAL_Y_LIM - max_chr_name_length - 5, text=row['chr'], rotation=90, ha='center', va='center')

        C[row['chr']] = c

    return C

def generate_links(ft_1: pd.DataFrame, 
                   ft_2: pd.DataFrame, 
                   right_chromosomes: dict, 
                   left_chromosomes: dict, 
                   link_colors: str,
                   straight_line: bool,
                   horizontal: bool,
) -> list:
    
    """
    Generates and plots links between two data frames.
    
    Parameters:
        ft_1 (pd.DataFrame): First full table data frame.
        ft_2 (pd.DataFrame): Second full table data frame.
        right_chromosomes (dict): Dictionary mapping sequence names to right chromosomes.
        left_chromosomes (dict): Dictionary mapping sequence names to left chromosomes.
        link_colors (str): Dictionary mapping sequence names to link colors.
        straight_line (bool): Flag indicating whether to plot links as straight lines.

    Returns:
        None
    """
    
    # Filter ft_1 and ft_2 to keep only complete rows
    ft_1 = ft_1[ft_1['status'] == 'Complete']
    ft_2 = ft_2[ft_2['status'] == 'Complete']

    # Merge the two data frames on 'busco_id' column
    df = pd.merge(ft_1, ft_2, on='busco_id', how='inner')

    # Filter df to keep only rows with sequence names in left_chromosomes and right_chromosomes
    df = df.loc[df['sequence_x'].isin(left_chromosomes.keys())]
    df = df.loc[df['sequence_y'].isin(right_chromosomes.keys())]

    # Initialize the links list
    links = []

    # Iterate over the rows of df
    for index, row in df.iterrows():

        # If the link color is not specified, use gray by default
        if row['sequence_x'] in link_colors.keys():
            color = link_colors[row['sequence_x']]
        elif row['sequence_y'] in link_colors.keys():
            color = link_colors[row['sequence_y']]
        else:
            color = '#d1d1d1'

        # Generate the link
        link = Link(C1=left_chromosomes[row['sequence_x']], 
                    C2=right_chromosomes[row['sequence_y']], 
                    p_1=row['gene_start_x'], 
                    p_2=row['gene_start_y'], 
                    color=color, 
                    straight_line=straight_line,
                    horizontal=horizontal
               )
        
        # Add the link to the links list
        links.append(link)
    
    return links

def plot_chromosomes(chromosomes: dict, ax: plt.Axes) -> None:
    """
    Plots the chromosomes on the given axes.
    
    Parameters:
        chromosomes (dict): Dictionary mapping sequence names to Chromosome objects.
        ax (plt.Axes): Matplotlib axes object to plot the chromosomes on.

    Returns:
        None
    """

    for c in chromosomes.values():
        c.plot(ax)

def plot_links(links: list, ax: plt.Axes) -> None:
    """
    Plots the links on the given axes.
    
    Parameters:
        links (list): List of Link objects.
        ax (plt.Axes): Matplotlib axes object to plot the links on.

    Returns:
        None
    """

    for l in links:
        l.plot(ax)

def vertical_synteny_plot(ft_1: pd.DataFrame, 
                          ft_2: pd.DataFrame,
                          karyotype_1: pd.DataFrame,
                          karyotype_2: pd.DataFrame,
                          title: str = 'Synteny plot',
                          dim: int = 2,
                          figsize=(18, 10),
                          dpi: int = 300,
                          round_edges: bool = False,
                          link_colors: dict = {},
                          straight_line: bool = False,
                          output_path: str = None,
                          bbox_inches: str = 'tight',
                          plt_show: bool = False
):
    """
    Generate a vertical synteny plot.
    
    Parameters:
        ft_1 (pd.DataFrame): Full table for the left karyotype.
        ft_2 (pd.DataFrame): Full table for the right karyotype.
        karyotype_1 (pd.DataFrame): Karyotype dataframe for the left karyotype.
        karyotype_2 (pd.DataFrame): Karyotype dataframe for the right karyotype.
        title (str, optional): The title of the plot. Defaults to 'Synteny plot'.
        dim (int, optional): The dimension of the chromosomes. Defaults to 2.
        figsize (tuple, optional): The size of the plot figure. Defaults to (18, 10).
        dpi (int, optional): The resolution of the plot figure. Defaults to 300.
        round_edges (bool, optional): Whether to round the edges of the karyotype blocks. Defaults to False.
        link_colors (dict, optional): A dictionary mapping link colors to chromosome pairs. Defaults to {}.
        straight_line (bool, optional): Whether to use straight lines for links. Defaults to False.
        output_path (str, optional): The path to save the plot to. Defaults to None.
        plt_show (bool, optional): Whether to show the plot. Defaults to False.

    Returns:
        None
    """

    # Global variables
    global VERTICAL_X_LIM
    global VERTICAL_Y_LIM
    
    # Lowercase the column names
    karyotype_1.columns = karyotype_1.columns.str.lower()
    karyotype_2.columns = karyotype_2.columns.str.lower()

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Turn off the axis
    ax.axis('off')

    # Set the x and y limits
    VERTICAL_X_LIM   = figsize[0] * 10
    VERTICAL_Y_LIM   = figsize[1] * 10

    # Set the x and y limits of the plot
    ax.set_xlim([0, VERTICAL_X_LIM])
    ax.set_ylim([0, VERTICAL_Y_LIM])

    # Insert the plot title
    ax.text(VERTICAL_X_LIM / 2, VERTICAL_Y_LIM - 3, karyotype_1['organism'][0] + ' - ' + karyotype_2['organism'][0] + ' ' + title, fontsize=20, ha='center')

    # Plot left and right karyotypes
    left_chromosomes  = generate_left_karyotype(karyotype_1, dim, round_edges)
    right_chromosomes = generate_right_karyotype(karyotype_2, dim, round_edges)

    # Generate and plot links
    links = generate_links(ft_1, ft_2, right_chromosomes, left_chromosomes, link_colors=link_colors, straight_line=straight_line, horizontal=False)

    # Plot the links
    plot_links(links, ax)

    # Plot the chromosomes
    plot_chromosomes(left_chromosomes, ax)
    plot_chromosomes(right_chromosomes, ax)

    # Write the legend
    plt.legend(handles=[Rectangle((0,0),1,1, color=karyotype_1['color'][0]), 
                        Rectangle((0,0),1,1, color=karyotype_2['color'][0])],
                        labels=[karyotype_1['organism'][0], karyotype_2['organism'][0]], 
                        loc='upper right'
    )

    # Plt tight layout
    plt.tight_layout()

    # Save the plot if output path is provided
    if output_path is not None:
        plt.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches)
    
    # Show the plot
    if plt_show:
        plt.show()
    
    plt.close()

def horizontal_synteny_plot(ft_1: pd.DataFrame, 
                            ft_2: pd.DataFrame,
                            karyotype_1: pd.DataFrame,
                            karyotype_2: pd.DataFrame,
                            title: str = 'Synteny plot',
                            dim: int = 2,
                            figsize: (int, int) = (30, 10),
                            dpi: int = 300,
                            round_edges: bool = False,
                            link_colors: dict = {},
                            straight_line: bool = False,
                            output_path: str = None,
                            bbox_inches: str = 'tight',
                            plt_show: bool = False
):
    """
    Generate a horizontal synteny plot.
    
    Parameters:
        ft_1 (pd.DataFrame): Full table for the left karyotype.
        ft_2 (pd.DataFrame): Full table for the right karyotype.
        karyotype_1 (pd.DataFrame): Karyotype dataframe for the left karyotype.
        karyotype_2 (pd.DataFrame): Karyotype dataframe for the right karyotype.
        title (str, optional): The title of the plot. Defaults to 'Synteny plot'.
        dim (int, optional): The dimension of the chromosomes. Defaults to 2.
        figsize (tuple, optional): The size of the plot figure. Defaults to (18, 10).
        dpi (int, optional): The resolution of the plot figure. Defaults to 300.
        round_edges (bool, optional): Whether to round the edges of the karyotype blocks. Defaults to False.
        link_colors (dict, optional): A dictionary mapping link colors to chromosome pairs. Defaults to {}.
        straight_line (bool, optional): Whether to use straight lines for links. Defaults to False.
        output_path (str, optional): The path to save the output plot. Defaults to None.
        plt_show (bool, optional): Whether to show the plot. Defaults to False.

    Returns:
        None
    """

    # Global variables
    global HORIZONTAL_X_LIM
    global HORIZONTAL_Y_LIM
    
    # Lowercase the column names
    karyotype_1.columns = karyotype_1.columns.str.lower()
    karyotype_2.columns = karyotype_2.columns.str.lower()

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Turn off the axis
    ax.axis('off')

    # Set the x and y limits
    HORIZONTAL_X_LIM   = figsize[0] * 10
    HORIZONTAL_Y_LIM   = figsize[1] * 10

    # Set the x and y limits of the plot
    ax.set_xlim([0, HORIZONTAL_X_LIM])
    ax.set_ylim([0, HORIZONTAL_Y_LIM])

    # Insert the plot title
    ax.text(HORIZONTAL_X_LIM / 2, HORIZONTAL_Y_LIM - 3, karyotype_1['organism'][0] + ' - ' + karyotype_2['organism'][0] + ' ' + title, fontsize=20, ha='center')

    # Plot left and right karyotypes
    bottom_chromosomes = generate_bottom_karyotype(karyotype_1, dim, round_edges)
    top_chromosomes    = generate_up_karyotype(karyotype_2, dim, round_edges)

    # Generate and plot links
    links = generate_links(ft_1, ft_2, top_chromosomes, bottom_chromosomes, link_colors=link_colors, straight_line=straight_line, horizontal=True)

    # Plot the links
    plot_links(links, ax)

    # Plot the chromosomes
    plot_chromosomes(bottom_chromosomes, ax)
    plot_chromosomes(top_chromosomes, ax)

    # Write the legend
    plt.legend(handles=[Rectangle((0,0),1,1, color=karyotype_1['color'][0]), 
                        Rectangle((0,0),1,1, color=karyotype_2['color'][0])],
                        labels=[karyotype_1['organism'][0], karyotype_2['organism'][0]], 
                        loc='upper right'
    )

    # Save the plot if output path is provided
    if output_path is not None:
        plt.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches)
    
    # Show the plot if plt_show is True
    if plt_show:
        plt.show()
    
    plt.close()

