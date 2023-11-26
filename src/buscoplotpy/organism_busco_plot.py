#Importing libraries
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from matplotlib.patches import Patch

def organism_busco_barplot(df: pd.DataFrame,
                           group_name: str = '',
                           organism_name: str = '',
                           out_path: str = './', 
                           filename: str = 'busco_barplot',
                           dpi: int = 300,
                           plt_show: bool = False
                        ) -> None:
    
    """
    Generate a barplot to visualize the completeness of assembly for different organisms on the same BUSCO dataset.

    Parameters:
        - df (pd.DataFrame): The input dataframe containing the data to be plotted.
        - group_name (str): The name of the group to be plotted.
        - organism_name (str): The name of the organism to be plotted.
        - out_path (str): The path where the plot image will be saved.
        - filename (str): The name of the plot image file.

    Output:
        - A barplot image with the completeness of assembly for different organisms on the same BUSCO dataset in .png format.

    Returns:
        - None
    """

    if group_name == '':
        group_name = df['group'].iloc[0]


    # Create a list of species names
    species_names = []

    # If the organism name is not provided, get the unique species names from the dataframe    
    if organism_name == '':
        organisms = df['organism'].unique()

        for organism in list(organisms):
            species_names = species_names + [organism + '_' + i for i in df[df['organism'] == organism]['version']]
    
    # Else if the organism name is provided, set the list of species names to the provided name
    else:
        species_names = [organism_name]
    
    # Get the group and dataset name from the dataframe
    dataset_name = df['dataset_name'].iloc[0]

    # Create a matrix of completeness values
    matrix = df[['single copy', 'multi copy', 'fragmented', 'missing']].to_numpy()

    # Get the one-line summary
    one_line_summary = df['one_line_summary'].to_list()

    # Set the style of Seaborn
    sns.set(style="whitegrid")

    # Define the colors and labels for the plot
    colors = ['#49a34b', '#636633', '#664f33', '#4b5669']
    labels = ['Complete - single', 'Complete - multi', 'Fragmented', 'Missing']
    busco_labels = ['Single copy', 'Multi copy', 'Fragmented', 'Missing']

    # Generate the values matrix
    values_matrix = matrix.copy()

    # Calculate the cumulative sum of the matrix
    for row in range(len(values_matrix)):
        for col in range(len(values_matrix[row])):
            if col != 0:
                values_matrix[row][col] = values_matrix[row][col-1] + values_matrix[row][col]

    # Transpose the matrix
    values_matrix = values_matrix.T

    # Create the plot
    fig, axs = plt.subplots(figsize=(20, len(species_names)+1), ncols=1, nrows=1)
    
    # Create the individual bars with different colors
    for idx, label in enumerate(labels):
        sns.barplot(x=values_matrix[-idx-1], color=colors[-idx-1], y=species_names, ax=axs, errorbar=None, alpha=0.99)
    
    # Add a text string to each bar
    for i in range(len(one_line_summary)):
        axs.text(0.9, i+0.1, str(one_line_summary[i]), color='white', fontsize=15)
    
    # Set the locator of the major ticker
    axs.xaxis.set_major_locator(ticker.MultipleLocator(5))
    
    # Customize the x and y axes and tick labels
    axs.set_xlabel('Percentage', fontsize=18)
    axs.set_ylabel('Organism', fontsize=18)
    axs.set_title(dataset_name + ' ' + group_name + ' - Barplot of completeness of assembly', fontsize=20, weight='bold', pad=30)
    axs.tick_params(labelsize=15)

    # Set the x-axis limits
    axs.set_xlim(0, 100)

    # Remove the borders of the plot
    sns.despine(top=True, right=True, left=True, bottom=True)

    # Remove the y-axis ticks
    axs.tick_params(axis='y', length=0)

    # Create the legend
    patches_list = [Patch(color=colors[i], label=labels[i], alpha=0.75) for i in range(len(labels))]
    axs.legend(handles=patches_list, bbox_to_anchor=(-0.5, 1), fontsize=15)

    
    # Create the values table
    #table_data = [["Species"] + busco_labels]
    #for row, species in zip(matrix, species_names):
    #    table_data.append([species] + [str(i) + '%' for i in row])
    #table = axs[1].table(cellText=table_data, loc='center')
    #table.set_fontsize(34)
    #table.scale(1, 2)
    #table.auto_set_column_width(col=range(len(table_data)))
    #axs[1].set_title("Percentage table", weight='bold', size=15)
    #for (row, col), cell in table.get_celld().items():
    #    if (row == 0) or (col == -1):
    #        cell.set_text_props(fontproperties=FontProperties(weight='bold'))  
    #axs[1].axis('off')

    # Save and show the plot
    plt.savefig(out_path + filename + '_completeness.png', bbox_inches='tight', dpi=dpi)

    if plt_show:
        plt.show()