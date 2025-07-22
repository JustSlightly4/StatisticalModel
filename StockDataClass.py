import yfinance as yf
import json
import os
from datetime import datetime

#Stock Class
#When creating a instance of the stock class it is important
#that you use the create method instead of the regular Stock()
#method
class Stock:
	#Intialization
	#the self. means that those variables are saved
	#as part of the class from now on.
	def __init__(self, tickerName):
		self.valid = False
		
		#TRY GETTING DATA FROM LOCAL COMP FIRST
		self.load_from_json(tickerName)
		
		#TRY GETTING DATA FROM YFINANCE API
		if not self.valid:
			try:
				#Not Saved Variables
				stock = yf.Ticker(tickerName)
				history = stock.history(period="31d")
				
				#Saved Variables
				self.tickerName = tickerName
				self.longName = stock.info.get("longName")
				self.dates = history.index.strftime("%b %d, %Y").tolist()
				self.prices = [round(p, 2) for p in history['Close'].tolist()] #rounds to 2 decimals
				self.valid = True
			except:
				pass

	#Use create for intialization
	#On successfull creation saves data and returns class
	#On creation failure return None to prevent future problems
	@classmethod
	def create(Stock, tickerName):
		obj = Stock(tickerName)
		if obj.valid:
			obj.save_to_json()
			return obj
		else:
			return None
			
	#Saves data to a JSON file
	def save_to_json(self):
		data = {
			"tickerName": self.tickerName,
			"longName": self.longName,
			"valid": self.valid,
			"dates": self.dates,
			"prices": self.prices
		}
		with open(self.tickerName + ".json", "w") as f:
			json.dump(data, f)
			
	# Loads data from a JSON file
	#In this function so errors are handled by try-catch and so by if-statements
	def load_from_json(self, tickerName):
		try:
			with open(tickerName + ".json", "r") as f:
				data = json.load(f)
				self.tickerName = data["tickerName"]
				self.longName = data["longName"]
				self.valid = data["valid"]
				self.dates = data["dates"]
				self.prices = data["prices"]
				
			#Once stock is loaded, check to see if most recent date and set valid or not
			today = datetime.today()
			most_recent_str = self.dates[-1]
			most_recent_date = datetime.strptime(most_recent_str, "%b %d, %Y")
			if today.date() == most_recent_date.date():
				print("Dates match!")
			elif today.date() > most_recent_date.date():
				print("Today's date is more recent.")
				self.valid = False
			else:
				print("List has a more recent date than today.")
				self.valid = False
				
		except FileNotFoundError:
			print(f"Error: File '{tickerName}' not found.")
			self.valid = False  # mark the object as invalid
		except json.JSONDecodeError:
			print(f"Error: File '{tickerName}' is not a valid JSON file.")
			self.valid = False
	
	#Handles when the dates list is not up to date
	#Variables today and most_recent_date of datetime variables
	def _Handle_Outdated_Dates_and_Prices(self, today, most_recent_date):
		history = stock.history(period=(str((most_recent_date - today).days) + "d"))
				
	def GetDates(self):
		return self.dates
		
	def GetPrices(self):
		return self.prices
	
	def GetTickerName(self):
		return self.tickerName
		
	def GetLongName(self):
		return self.longName
		
	def IsValid(self):
		return self.valid
		
	def GetSize(self):
		return len(self.dates)
		
