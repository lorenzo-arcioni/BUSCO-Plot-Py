# -*- coding: utf-8 -*-
# This class represents a link between two chromosomes.

import chromosome as Chromosome
import numpy as np

class Link:

    def __init__(self, C1: Chromosome, C2: Chromosome, p_1: int, p_2: int, color: str = '#d1d1d1', 
                 straight_line: bool = False, horizontal: bool = False):
        """
        Initialize the Line class.

        Parameters:
            C1 (Chromosome): The first chromosome object.
            C2 (Chromosome): The second chromosome object.
            p_1 (int): The position on the first chromosome.
            p_2 (int): The position on the second chromosome.
            color (str, optional): The color of the line. Defaults to '#d1d1d1'.
            straight_line (bool, optional): Whether the line should be straight. Defaults to False.
            horizontal (bool, optional): Whether the line should be horizontal. Defaults to False.
        """

        # Set Link properties
        self.C1 = C1
        self.C2 = C2
        self.straight_line = straight_line
        self.color = color
        self.horizontal = horizontal

        # Set Link coordinates
        self.start_point = self.C1.get_relative_position(p_1)
        self.end_point   = self.C2.get_relative_position(p_2)
    
    def bezier_curve(self, t, p0, p1, p2, p3):
        """
        Calculate the Bezier curve at time t.

        Args:
            t (float): The time parameter between 0 and 1.
            p0 (float): The starting point of the curve.
            p1 (float): The first control point.
            p2 (float): The second control point.
            p3 (float): The ending point of the curve.
        Returns:
            float: The position on the Bezier curve at time t.
        """

        return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3

    def plot(self, ax):

        """
        Plot the link on the given axes.
        
        Args:
            ax (matplotlib.axes.Axes): The axes on which to plot the link.
        """
        
        # If not straight line then calculate the Bezier curve
        if not self.straight_line:

            # Create a range of 100 values between 0 and 1
            t_values = np.linspace(0, 1, 100)

            if self.horizontal:
                # Get middle of C1 and C2
                y_middle_c1_c2 = (self.start_point[1] + self.end_point[1]) / 2.0

                # Calculate the x and y coordinates of the Bezier curve
                x_values = [self.bezier_curve(t, self.start_point[0], self.start_point[0], self.end_point[0], self.end_point[0]) for t in t_values]
                y_values = [self.bezier_curve(t, self.start_point[1], y_middle_c1_c2, y_middle_c1_c2, self.end_point[1]) for t in t_values]
            else:
                # Get middle of C1 and C2
                x_middle_c1_c2 = (self.start_point[0] + self.end_point[0]) / 2.0

                # Calculate the x and y coordinates of the Bezier curve
                x_values = [self.bezier_curve(t, self.start_point[0], x_middle_c1_c2, x_middle_c1_c2, self.end_point[0]) for t in t_values]
                y_values = [self.bezier_curve(t, self.start_point[1], self.C1.y_end, self.C2.y_start, self.end_point[1]) for t in t_values]

        # Else if straight line  
        else:
            # Calculate the x and y coordinates of the straight line
            x_values = [self.start_point[0], self.end_point[0]]
            y_values = [self.start_point[1], self.end_point[1]]

        # Then plot the line
        ax.plot(x_values, y_values, ls='-', color=self.color, linewidth=1)
