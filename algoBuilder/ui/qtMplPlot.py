"""
inspired from:
https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_qt_sgskip.html
https://bastibe.de/2013-05-30-speeding-up-matplotlib.html
https://stackoverflow.com/questions/57891219/how-to-make-a-fast-matplotlib-live-plot-in-a-pyqt5-gui

once matplotlib supports Qt6 upgrade from PySide2 -> PySide6 can be made
https://github.com/matplotlib/matplotlib/pull/19255

^^^ The above has been done as we have now migrated to PySide 6 
"""
from __future__ import annotations

from ..commonUtil import pathUtil
from ..commonUtil.sparseDictList import SparseDictList
from .uiFilePaths import BASE_MPL_STYLE

import PySide6.QtCore

# matplotlib imports
import matplotlib as mpl
from matplotlib.backends.backend_qtagg import FigureCanvas
import matplotlib.pyplot as plt

from dataclasses import dataclass
import typing
import numbers


@dataclass
class graphSettings:
    """
    Defines the settings for each plot on the graph
    """

    name: str
    graphType: str = "line"
    color: str = "blue"
    yMin: float = 0.0
    yMax: float = 100.0


@dataclass
class graphData:
    """
    Stores the data for each plot on the graph
    """

    x: typing.List
    y: typing.List
    ax: mpl.axes.Axes
    line: mpl.lines.Line2D


class qtMplPlot(FigureCanvas):
    """
    This is the FigureCanvas in which the live plot is drawn.
    This widget can be used within the qt application for displaying plotted data

    """

    def __init__(
        self, xLen: int, model: typing.Any, settings: typing.List[graphSettings]
    ) -> None:
        """
        xLen:       The nr of data points shown in one plot
        model:      qt model this graph is connected to, the plot will connect updateCanvas to modelUpdatel
        settings:   list of graphSettings, this will be used to setup the plot

        """
        # Load Style first
        plt.style.use(BASE_MPL_STYLE)

        super().__init__(plt.figure())
        # Range settings
        self.xLen: int = xLen
        self.settings: typing.List = settings
        self.graphDataDict: typing.Dict(str, graphData) = {}

        # setup figure
        self.figure.patch.set_facecolor("#2a2a2a")

        # Store two lists x and y
        x = list(range(0, xLen))
        y = [0] * xLen

        # setup first axes
        ax = self.figure.subplots()
        ax.set_ylim(ymin=self.settings[0].yMin, ymax=self.settings[0].yMax)
        (line,) = ax.plot(
            x, y, label=self.settings[0].name, color=self.settings[0].color
        )
        self.graphDataDict[self.settings[0].name] = graphData(x, y, ax, line)

        # Setup all graphs:
        for setting in self.settings[1:]:
            newX = x.copy()
            newY = y.copy()
            newAx = ax.twinx()
            newAx.set_ylim(ymin=setting.yMin, ymax=setting.yMax)
            newLine = None
            if setting.graphType == "bar":
                newLine = newAx.bar(newX, newY, label=setting.name, color=setting.color)
            else:
                (newLine,) = newAx.plot(
                    newX, newY, label=setting.name, color=setting.color
                )
            self.graphDataDict[setting.name] = graphData(newX, newY, newAx, newLine)

        self.figure.legend()
        self.draw()

        # Connect to model signal
        model.modelUpdated.connect(self.updateCanvas)
        return

    def updateCanvas(self, newData: SparseDictList) -> None:
        """
        This function gets called by the model signal
        The model signal should carry the new data to the plot
        """
        if newData is not None and newData.getFirstListLength() > 0:
            for column in self.graphDataDict.keys():
                if column.lower() in newData:
                    gD: graphData = self.graphDataDict[column]
                    # Add new data and truncate those outside period
                    # we won't need any more than length of variables anyways
                    tempList = newData[column.lower()][-self.xLen :]
                    # if it's not a number replace it with 0
                    cleaned = [
                        data.value if isinstance(data.value, numbers.Number) else 0
                        for data in tempList
                    ]
                    if len(cleaned) == self.xLen:
                        gD.y = cleaned
                    else:
                        gD.y.extend(cleaned)
                        gD.y = gD.y[-self.xLen :]

                    # if it's a bar chart do thise
                    if isinstance(gD.line, mpl.container.BarContainer):
                        for x in range(0, len(gD.y)):
                            gD.line.patches[x].set_height(gD.y[x])
                        self.figure.canvas.draw()
                    else:
                        # set it to the line and draw artists
                        gD.line.set_ydata(gD.y)
                        gD.ax.draw_artist(gD.ax.patch)
                        gD.ax.draw_artist(gD.line)

            self.update()
            self.flush_events()
