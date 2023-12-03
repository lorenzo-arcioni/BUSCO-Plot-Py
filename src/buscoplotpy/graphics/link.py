
import buscoplotpy.graphics.chromosome as Chromosome
import numpy as np

# Set the x and y limits
VERTICAL_X_LIM   = 180
VERTICAL_Y_LIM   = 100
HORIZONTAL_X_LIM = 300
HORIZONTAL_Y_LIM = 100

class Link:

    def __init__(self, C1: Chromosome, C2: Chromosome, p_1: int, p_2: int, color: str = 'black', straight_line: bool = False, horizontal: bool = False):

        """
        Initialize the object with the given values.
        Args:
            x_1 (float): The x-coordinate of the start point.
        """

        self.C1 = C1
        self.C2 = C2
        self.straight_line = straight_line
        self.color = color
        self.horizontal = horizontal

        if self.horizontal:
            self.start_point = self.C1.get_horizontal_relative_position(p_1)
            self.end_point   = self.C2.get_horizontal_relative_position(p_2)
        else:
            self.start_point = self.C1.get_vertical_relative_position(p_1)
            self.end_point   = self.C2.get_vertical_relative_position(p_2)
    
    def bezier_curve(self, t, p0, p1, p2, p3):
        """
        Calculate the Bezier curve at time t.
        """
        return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3

    def plot(self, ax):

        """
        Plot the link on the given axes.
        Args:
            ax (matplotlib.axes.Axes): The axes on which to plot the link.
        """
        
        if not self.straight_line:
            # Parametro t da 0 a 1
            t_values = np.linspace(0, 1, 100)

            if self.horizontal:
                # Get middle of C1 and C2
                y_middle_c1_c2 = (self.start_point[1] + self.end_point[1]) / 2.0

                # Calcola le coordinate x e y sulla curva di Bezier per ogni t
                x_values = [self.bezier_curve(t, self.start_point[0], self.start_point[0], self.end_point[0], self.end_point[0]) for t in t_values]
                y_values = [self.bezier_curve(t, self.start_point[1], y_middle_c1_c2, y_middle_c1_c2, self.end_point[1]) for t in t_values]
            else:
                # Get middle of C1 and C2
                x_middle_c1_c2 = (self.start_point[0] + self.end_point[0]) / 2.0

                # Calcola le coordinate x e y sulla curva di Bezier per ogni t
                x_values = [self.bezier_curve(t, self.start_point[0], x_middle_c1_c2, x_middle_c1_c2, self.end_point[0]) for t in t_values]
                y_values = [self.bezier_curve(t, self.start_point[1], self.C1.y_end, self.C2.y_start, self.end_point[1]) for t in t_values]
            
        else:
            x_values = [self.start_point[0], self.end_point[0]]
            y_values = [self.start_point[1], self.end_point[1]]

        ax.plot(x_values, y_values, ls='-', color=self.color, linewidth=1)