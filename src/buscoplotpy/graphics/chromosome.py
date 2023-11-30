# -*- coding: utf-8 -*-

from matplotlib.patches import Wedge, Rectangle
from buscoplotpy.utils.label import Label


class Chromosome():

	def __init__(self, x_start: float, 
			  		   x_end: float, 
					   y_start: float, 
					   y_end: float, 
					   horizontal: bool = True,
					   round_edges: bool = False):
		
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

		self.x_start    = x_start
		self.x_end      = x_end
		self.y_start    = y_start
		self.y_end      = y_end

		self.horizontal = horizontal
		self.round_edges = round_edges

		self.labels  = []
		self.regions = []
		
		if self.horizontal and self.round_edges:

			# Calculate the center and radius of the chromosome semicircles
			center_y = (self.y_end + self.y_start)/2.0
			radius   = (self.y_end - self.y_start)/2.0

			# Calculate the angles of the semicircles
			theta1   = -90.0
			theta2   =  90.0
			
			# Create the start and the end semicircles
			self.w1 = Wedge((self.x_start, center_y), radius, theta2, theta1, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)
			self.w2 = Wedge((self.x_end,   center_y), radius, theta1, theta2, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)

		elif not self.horizontal and self.round_edges:

			# Calculate the center and radius of the chromosome semicircles
			center_x = (self.x_end + self.x_start)/2.0
			radius   = (self.x_end - self.x_start)/2.0

			# Calculate the angles of the semicircles
			theta1   = -90.0
			theta2   =  90.0
			
			# Create the start and the end semicircles
			self.w1 = Wedge((center_x, self.y_start), radius, theta2, theta1, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)
			self.w2 = Wedge((center_x, self.y_end),   radius, theta1, theta2, width=0.00001, facecolor='white', edgecolor='black', linewidth=0.6)
	
	def __str__(self):

		"""
		Returns a string representation of the Chromosome object.
		
		Returns:
			str: The string representation of the object.
		"""

		return 'Chromosome({}, {}, {}, {})'.format(self.x_start, self.x_end, self.y_start, self.y_end)

	def plot(self, ax, round_edges=False):

		"""
		Plot the chromosome on the given axes.

		Parameters:
			- ax: The axes to plot on.
			- round_edges: A boolean indicating whether to round the edges of the chromosome.
		Returns:
			None
		"""

		# Add the chromosome horizontal lines 
		ax.plot([self.x_start, self.x_end], [self.y_start, self.y_start], ls='-', color='black', linewidth=1)
		ax.plot([self.x_start, self.x_end], [self.y_end,   self.y_end],   ls='-', color='black', linewidth=1)

		if round_edges:

			# Add the semicircles on chromosomes
			ax.add_patch(self.w1)
			ax.add_patch(self.w2)	
		
		else:
        
			# Add the chromosome vertical lines
			ax.plot([self.x_start, self.x_start], [self.y_start, self.y_end], ls='-', color='black', linewidth=1)
			ax.plot([self.x_end,   self.x_end],   [self.y_start, self.y_end], ls='-', color='black', linewidth=1)
		
		for label in self.labels:
			label.plot(ax)
		
		for region in self.regions:
			ax.add_patch(region)
	
	def add_label(self, x: float, y: float, text: str, horizontalalignment: str, verticalalignment: str):

		label = Label(x, y, text, horizontalalignment=horizontalalignment, verticalalignment=verticalalignment)

		self.labels.append(label)
	
	def add_region(self, anchor_point: (float, float), width: float, height: float, color: str = 'black', linewidth: int = 1):

		region = Rectangle(xy=anchor_point, width=width, height=height, color=color, linewidth=linewidth)
		self.regions.append(region)