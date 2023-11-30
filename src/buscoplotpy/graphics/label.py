# -*- coding: utf-8 -*-
# This class represents a label on a plot.

class Label():

    def __init__(self, x: float, y: float, text: str, ha: str = 'left', va: str = 'baseline'):

        """
        Initialize the object with the given values.
        Args:
            x (float): The x-coordinate of the object.
            y (float): The y-coordinate of the object.
            text (str): The text content of the object.
            ha (str): The horizontal alignment of the object. Default is 'left'.
            va (str): The vertical alignment of the object. Default is 'baseline'.
        """
        
        # Coordinates
        self.x    = x
        self.y    = y
        self.text = text

        # Graphical attributes
        self.horizontalalignment = ha
        self.verticalalignment   = va
    
    def plot(self, ax):

        """
        Plot the text on the given axes.
        Parameters:
            ax (matplotlib.axes.Axes): The axes on which to plot the text.
        """

        # Add the text to the axes at the specified coordinates
        ax.text(self.x, self.y, self.text, ha=self.horizontalalignment, va=self.verticalalignment)