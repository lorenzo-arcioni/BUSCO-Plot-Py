# -*- coding: utf-8 -*-

import pandas as pd

def load_metaeuk_coordinates(path: str) -> pd.DataFrame:

    """
    Load the metaeuk gff coordinates file into a pandas DataFrame.
    
    Parameters:
        path (str): The path to the metaeuk coordinates file.
        
    Returns:
        pd.DataFrame: The loaded metaeuk coordinates with all informations.
    """
    
    gff_column_names =[
        'sequence',
        'source',
        'type',
        'start',
        'end',
        'score',
        'strand',
        'phase',
        'attributes'
    ]

    # Read the metaeuk coordinates from the file
    metaeuk_coordinates = pd.read_csv(path, sep='\t', header=None, names=gff_column_names)

    return metaeuk_coordinates