import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import date, timedelta
import numpy as np
import yfinance as yf

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a vertical box layout
        layout = QVBoxLayout(self)

        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Adds a white canvas to the screen
        layout.addWidget(self.canvas)

        # Draw the initial plot
        self.plot()

    def plot(self):
        # Clear any existing plot
        self.figure.clear()
        
        #Get Date
        today = date.today()

        # Create a subplot and plot data
        ax = self.figure.add_subplot(1, 1, 1)
			
        #X and Y axis
        # Define ticker and fetch data
        ticker = "AAPL"
        stock = yf.Ticker(ticker)
        data = stock.history(period="5d")  # 1 year of daily data

        # Extract dates and closing prices
        dates = data.index.strftime("%B, %d").tolist()  # convert to string if needed
        prices = data['Close'].tolist()
        
        #Plots the x and y arrays to the screen
        ax.plot(dates, prices, label="y = ?", marker='.')

		#Writes all the graph information
        ax.set_title("Predicted Market Model")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.legend()

        # Refresh canvas
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Market Model")

        # Set the central widget
        self.setCentralWidget(GraphWidget())

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
