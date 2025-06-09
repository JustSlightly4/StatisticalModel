import yfinance as yf

def GetStockData(name):
	# Define ticker and fetch data
	try:
		stock = yf.Ticker(name)
		data = stock.history(period="31d")
	except Exception as e:
		return [], []

	# Extract dates and closing prices
	try:
		dates = data.index.strftime("%B, %d").tolist()
		prices = data['Close'].tolist()
	except Exception as e:
		return [], []
	
	return dates, prices
