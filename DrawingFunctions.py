import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import date, timedelta

import LogicFunctions
import StockDataClass

#Plots the graph using the provided instance of the stock class
def PlotGraph(figure, canvas, stock):
	
	if not stock:
		return False
	
	# Clear any existing plot
	figure.clear()
	
	#Get Date
	today = date.today()

	# Create a subplot and plot data
	ax = figure.add_subplot(1, 1, 1)
	
	#Plots the x and y arrays to the screen
	#x size is determined by the size of the dates list
	ax.plot(stock.GetDates(), stock.GetPrices(), label="y = ?", marker='.')
	numOfLabels = 5 #Number of labels on the x-axis
	if stock.GetSize() >= numOfLabels:
		# Calculate tick indices evenly spaced between 0 and size-1
		step = (stock.GetSize() - 1) / (numOfLabels - 1)
		tick_positions = [round(step * i) for i in range(numOfLabels)]
	else:
		tick_positions = list(range(stock.GetSize()))  # show all if less than 5 data points
	ax.set_xticks(tick_positions)

	#Writes all the graph information
	ax.set_title(stock.GetLongName() + " Market Model")
	ax.set_xlabel("Time")
	ax.set_ylabel("Price")
	ax.legend()

	# Refresh canvas
	figure.set_layout_engine('constrained')
	canvas.draw()
	
	return True
	
def handleSearch(figure, canvas, input_field):
	textboxFlag = PlotGraph(figure, canvas, StockDataClass.Stock.create(name))
	if textboxFlag == False:
		input_field.setStyleSheet("background-color: red;") #Changes search bar to red
		print("Failed Search!")
	else:
		input_field.setStyleSheet("")  #Changes search bar back to normal
		

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Market Model")

        # Create central widget and set layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)

        # Create the graph
        figure = Figure()
        canvas = FigureCanvas(figure)
        layout.addWidget(canvas)

        # Create the input box
        # Create horizontal layout for input + button
        input_layout = QHBoxLayout()
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter ticker name here...")
        submit_button = QPushButton("Search")
        # Add input and button side-by-side
        input_layout.addWidget(input_field)
        input_layout.addWidget(submit_button)
        #Add input box and button to the main layout
        layout.addLayout(input_layout)

        # Set central widget
        self.setCentralWidget(central_widget)
        
        #User Inputs
        submit_button.clicked.connect(lambda: handleSearch(figure, canvas, input_field))
        input_field.returnPressed.connect(lambda: handleSearch(figure, canvas, input_field))
