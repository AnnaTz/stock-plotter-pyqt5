from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class StockPlotterApp(QMainWindow):
    def __init__(self, fig):
        super().__init__()
        self.canvas = FigureCanvasQTAgg(fig)
        self.current_ax = None
        self.lines = []
        self.init_ui()
        self.zoom_factor = 1.1


    def init_ui(self):
        self.setCentralWidget(self.canvas)

        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('key_press_event', self.on_key)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
                
        self.setWindowTitle('StockPlotterApp')
        self.showMaximized()


    def on_click(self, event):
        if event.inaxes is None:
            return
        if self.current_ax is None:
            self.current_ax = event.inaxes
            self.line_start = (event.xdata, event.ydata)
        else:
            if event.inaxes == self.current_ax:
                line = self.current_ax.plot([self.line_start[0], event.xdata], [self.line_start[1], event.ydata], 'w-')[0]
                self.canvas.draw()
                self.lines.append((self.current_ax, line))
            self.current_ax = None


    def on_key(self, event):
        if self.lines:
            _, line_to_delete = self.lines.pop()
            line_to_delete.remove()
            self.canvas.draw()


    def on_scroll(self, event):
        ax = event.inaxes
        if ax:
            xdata, ydata = event.xdata, event.ydata
            if event.button == 'up':
                scale_factor = 1 / self.zoom_factor
            elif event.button == 'down':
                scale_factor = self.zoom_factor
            else:
                return
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax.set_xlim([xdata + (x - xdata) * (scale_factor*1.1 if scale_factor>1 else scale_factor/1.1) for x in xlim])
            ax.set_ylim([ydata + (y - ydata) * scale_factor for y in ylim])
            self.canvas.draw_idle()
            