# -*- coding: utf-8 -*-
# This calss represents a Chromosome object

from matplotlib.patches import Wedge, Rectangle
from buscoplotpy.graphics.label import Label


class Chromosome:

    def __init__(self, x_start: float, 
                       x_end: float, 
                       y_start: float, 
                       y_end: float,
                       size: float,
                       horizontal: bool = True,
                       round_edges: bool = False,
                       color: str = ''
    ):
		
        """
        Initialize the Chromosome class.
        
        Args:
            x_start (float): The starting x-coordinate of the chromosome.
            x_end (float): The ending x-coordinate of the chromosome.
            y_start (float): The starting y-coordinate of the chromosome.
            y_end (float): The ending y-coordinate of the chromosome.
            horizontal (bool, optional): Whether the chromosome is horizontal. Defaults to True.
            round_edges (bool, optional): Whether the chromosome has rounded edges. Defaults to False.
        """

        # Coordinates
        self.x_start = x_start
        self.x_end   = x_end
        self.y_start = y_start
        self.y_end   = y_end
        self.size    = size

        # Graphical attributes
        self.horizontal  = horizontal
        self.round_edges = round_edges
        self.color       = color

        # Elements
        self.labels  = []
        self.regions = []
        
        if self.horizontal and self.round_edges:

            # Calculate the center and radius of the chromosome semicircles
            center_y = (self.y_end + self.y_start)/2.0
            radius   = (self.y_end - self.y_start)/2.0

            # Calculate the angles of the semicircles
            theta1   = 0.0
            theta2   = 360.0
            
            # Create the start and the end semicircles
            self.w1 = Wedge((self.x_start + radius/2, center_y), radius, theta2, theta1, width=0.00001, facecolor='white', edgecolor='black', linewidth=1)
            self.w2 = Wedge((self.x_end   - radius/2, center_y), radius, theta1, theta2, width=0.00001, facecolor='white', edgecolor='black', linewidth=1)

        elif not self.horizontal and self.round_edges:

            # Calculate the center and radius of the chromosome semicircles
            center_x = (self.x_end + self.x_start)/2.0
            radius   = (self.x_end - self.x_start)/2.0

            # Calculate the angles of the semicircles
            theta1   =  0.0
            theta2   =  360.0
            
            # Create the start and the end semicircles
            self.w1 = Wedge((center_x, self.y_start), radius, theta2, theta1, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)
            self.w2 = Wedge((center_x, self.y_end), radius, theta1, theta2, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)
	
    def __str__(self):

        """
        Returns a string representation of the Chromosome object.
        
        Returns:
            str: The string representation of the object.
        """

        return 'Chromosome({}, {}, {}, {})'.format(self.x_start, self.x_end, self.y_start, self.y_end)

    def plot(self, ax):

        """
        Plot the chromosome on the given axes.

        Parameters:
            - ax: The axes to plot on.
            - round_edges: A boolean indicating whether to round the edges of the chromosome.
        Returns:
            None
        """

        if self.horizontal:
            # Add the chromosome horizontal lines 
            ax.plot([self.x_start, self.x_end], [self.y_start, self.y_start], ls='-', color='black', linewidth=1)
            ax.plot([self.x_start, self.x_end], [self.y_end,   self.y_end],   ls='-', color='black', linewidth=1)

            if self.round_edges:
                # Add the semicircles on chromosomes
                ax.add_patch(self.w1)
                ax.add_patch(self.w2)
            
            else:
                # Add the chromosome vertical lines
                ax.plot([self.x_start, self.x_start], [self.y_start, self.y_end], ls='-', color='black', linewidth=1)
                ax.plot([self.x_end,   self.x_end],   [self.y_start, self.y_end], ls='-', color='black', linewidth=1)

        else:
            # Add the chromosome vertical lines
            ax.plot([self.x_start, self.x_start], [self.y_start, self.y_end], ls='-', color='black', linewidth=1)
            ax.plot([self.x_end,   self.x_end],   [self.y_start, self.y_end], ls='-', color='black', linewidth=1)

            if self.round_edges:
                # Add the semicircles on chromosomes
                ax.add_patch(self.w1)
                ax.add_patch(self.w2)

            else: 
                # Add the chromosome horizontal lines
                ax.plot([self.x_start, self.x_end], [self.y_start, self.y_start], ls='-', color='black', linewidth=1)
                ax.plot([self.x_start, self.x_end], [self.y_end,   self.y_end],   ls='-', color='black', linewidth=1)
        
        if self.color:

            # Fill the chromosome with the specified color
            ax.add_patch(Rectangle(xy=(self.x_start, self.y_start), width=self.x_end - self.x_start, height=self.y_end - self.y_start, color=self.color))

        # Plot the labels
        for label in self.labels:
            label.plot(ax)
        
        # Plot the regions
        for region in self.regions:
            ax.add_patch(region)

    def add_label(self, x: float, y: float, text: str, rotation: float = 0, ha: str = 'left', va: str = 'baseline'):

        """
        Add a label to the plot at the specified coordinates.
        
        Args:
            x (float): The x-coordinate of the label.
            y (float): The y-coordinate of the label.
            text (str): The text of the label.
            ha (str, optional): The horizontal alignment of the label. Defaults to 'left'.
            va (str, optional): The vertical alignment of the label. Defaults to 'baseline'.
        """

        label = Label(x, y, text, rotation=rotation, ha=ha, va=va)
        self.labels.append(label)

    def add_region(self, anchor_point: (float, float), width: float, height: float, color: str = 'black', linewidth: int = 1):

        """
        Adds a region to the list of regions.
        
        Parameters:
            anchor_point (Tuple[float, float]): The anchor point of the region.
            width (float): The width of the region.
            height (float): The height of the region.
            color (str, optional): The color of the region. Defaults to 'black'.
            linewidth (int, optional): The linewidth of the region. Defaults to 1.
        """

        region = Rectangle(xy=anchor_point, width=width, height=height, color=color, linewidth=linewidth)
        self.regions.append(region)
    
    def get_relative_position(self, position: int) -> (float, float):

        """
        Returns the position relative to the start and end of the chromosome.

        Parameters:
            position (int): The position to convert.
        
        Returns:
            float: The position relative to the start and end of the chromosome.
        """

        if self.horizontal:
            return (position * (self.x_end - self.x_start) / self.size + self.x_start, self.y_end)            
        else:
            return (self.x_end, position * (self.y_end - self.y_start) / self.size + self.y_start)
