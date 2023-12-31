# -*- coding: utf-8 -*-

#Importing libraries
import pandas as pd

def load_busco_fulltable(path: str, 
                         group: str='', 
                         organism: str='', 
                         genome_version: str=''
) -> pd.DataFrame:

    """
    Load the full table generated by BUSCO into a pandas DataFrame.
    
    Parameters:
        group (str): The group the organism belongs to.
        organism (str): The name of the organism.
        genome_version (str): The version of the genome.
        path (str): The path to the full table.
        
    Returns:
        pd.DataFrame: The loaded full table with busco gene information.
    """
    
    # Initialize the empty full table
    full_table = pd.DataFrame()

    # Read the busco table from the file
    busco_table = pd.read_csv(path, skiprows=2, sep='\t')

    # Populate the columns of the full table with data from the busco table
    full_table['busco_id'] = busco_table['# Busco id']
    full_table['status'] = busco_table['Status']
    full_table['sequence'] = busco_table['Sequence']
    full_table['gene_start'] = busco_table['Gene Start']
    full_table['gene_end'] = busco_table['Gene End']
    full_table['strand'] = busco_table['Strand']
    full_table['score'] = busco_table['Score']
    full_table['length'] = busco_table['Length']
    full_table['group'] = group
    full_table['organism'] = organism
    full_table['genome_version'] = genome_version

    # Try to assign the 'OrthoDB url' column to the full table, otherwise assign None
    try:
        full_table['ortho_db_url'] = busco_table['OrthoDB url']
    except:
        full_table['ortho_db_url'] = None
    
    # Try to assign the 'Description' column to the full table, otherwise assign None
    try:
        full_table['description'] = busco_table['Description']
    except:
        full_table['description'] = None

    # Extract the sequence name from the 'sequence' column
    full_table.loc[:, 'sequence'] = full_table['sequence'].map(lambda x: x.split(':')[0] if pd.notna(x) else None)

    # Return the loaded full table
    return full_table