# -*- coding: utf-8 -*-

import matplotlib.pyplot

class Label():

    def __init__(self, x: float, y: float, text: str, horizontalalignment: str, verticalalignment: str):

        self.x = x
        self.y = y
        self.text = text

        self.horizontalalignment = horizontalalignment
        self.verticalalignment = verticalalignment
    
    def plot(self, ax):

        ax.text(self.x, self.y, self.text, horizontalalignment=self.horizontalalignment, erticalalignment=self.verticalalignment)