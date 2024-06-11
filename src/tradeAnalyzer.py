from optionPricer import Option

#Analyzes the profit/loss for a trade on a given contract depending on changes in the underlying,
#time to expiration, and volatility. Transaction costs are taken into account, and profit/loss
#is given as a ratio of the purchase price + transaction costs of the contract
class TradeAnalyzer:
	def __init__(self, option, purchasePrice, transactionCost=0.65):
		#Set up class attributes
		self.option = option
		self.purchasePrice = purchasePrice
		self.transactionCost = transactionCost

	#returns the total cost to enter the trade. Transaction cost is multiplied by 2 to account for entry and exit costs of the trade.
	def getEntryCost(self):
		return self.purchasePrice + (2 * self.transactionCost)

	#returns the theoretical value of the option contract.
	def getExitValue(self):
		return self.option.europeanOption.NPV()*100	

	#updates the parameters of the option, and calculates the value gain ratio
	def getValueMultiplier(self, underlyingPrice=False, timeToValuation=False, newVolatility=False):
		self.option.updateParams(underlyingPrice=underlyingPrice, timeToValuation=timeToValuation, newVolatility=newVolatility)
		res = self.getExitValue()/self.getEntryCost()
		self.option.refreshOption(reset=True)
		return res


	


		
option = Option(0.9, 1, 0.01, 0, 3.2, 10, "call")
trade = TradeAnalyzer(option, option.europeanOption.NPV()*100)
for i in range(10):
	print(i, "--", trade.getValueMultiplier(timeToValuation = i))



