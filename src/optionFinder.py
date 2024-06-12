#OptionFinder is responsible for gathering and processing information about the current option market
#and creating a list of Option objects based on search params.

from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Use port 7497 for TWS

# Define the contract for an at-the-money (ATM) option for GME
atm_option_contract = Option('GME', '20240614', 30, 'C', 'SMART')

# Request market data for the ATM option
ticker = ib.reqTickers(atm_option_contract)

# Wait for the data to be received
ib.sleep(2)

# Get the last available price of the ATM option
last_price = ticker[0].marketPrice()

# Print the last available price of the ATM option
print("\nLast available price for ATM Option:")
print(f"Last price (Option): {last_price}")


class OptionFinder:
	def __init__(self):
		self.x = 1
		