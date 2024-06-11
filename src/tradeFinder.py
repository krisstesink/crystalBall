from tradeAnalyzer import TradeAnalyzer
#TradeFinder takes a list of options, and constructs lists for rewards and risk corresponding
#to entering a trade into each corresponding option. Tradefinder can take a predicted pricepoint
#within a specific timeframe, and find the potential risks and rewards of entring a trade given 
#those predictions. risks and rewards are calculated as multiplicitve factors of the purchase price
#of the option in current market conditions.
class TradeFinder:
	def __init__(self, options):
		self.options = options
		self.trades = []
		self.rewards = []
		self.risks = []
		self.rewardToRisks = []

		#create a list of TradeAnalyzer objects for each option in the options list
		for option in self.options:
			self.trades.append(TradeAnalyzer(option, option.europeanOption.NPV()*100))

#method for updating the risks list given a timeframe and maximum predicted downswing.
	def updateRisks(self, timeToValuation, maxUnderlyingDownswing=0.05):
		for trade in trades:
			if(trade.option.optionType == "call"):
				underlyingPrice = trade.option.originalPrice*(1-maxUnderlyingDownswing)
			else:
				underlyingPrice = trade.option.originalPrice*(1+maxUnderlyingDownswing)

			risks.append(trade.getValueMultiplier(underlyingPrice=underlyingPrice, timeToValuation=timeToValuation))

#method for updating rewards list given a timeframe, a price target, and a volatility target.
	def updateRewards(self, timeToValuation, priceTarget, newVolatility=False):
		for trade in trades:
			rewards.append(trade.getValueMultiplier(underlyingPrice=priceTarget, timeToValuation=timeToValuation, newVolatility=newVolatility))

#method for updating the rewardToRisks list given a certain timeframe, price targer, maximum downswing, and newVolatility.
	def updateRewardToRisks(self, timeToValuation, priceTarget, newVolatility=False, maxUnderlyingDownswing=0.05):
		self.updateRisks(timeToValuation, maxUnderlyingDownswing=maxUnderlyingDownswing)
		self.updateRewards(timeToValuation, priceTarget, newVolatility=newVolatility)

		for i in range(len(trades)):
			risk = abs(self.risks[i] - 1)
			reward = self.rewards[1] - 1

			self.rewardToRisks.append(reward/risk)




