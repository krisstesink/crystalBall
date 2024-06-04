from optionPricer import OptionPricer
from scipy import stats

option = OptionPricer(0.9, 1, 0.01, 0, 3.2, 5, "call")

class NormalAnalyzer:
	def __init__(self, option, targetPrice, standardDev, samples):
		#Set up class attributes
		self.option = option
		self.targetPrice = targetPrice
		self.standardDev = standardDev
		originalPrice = option.europeanOption.NPV()

		#Sample from a normal distribution around the price target
		normDist = stats.norm(loc = targetPrice, scale = standardDev)
		samples = normDist.rvs(size = samples)
		samples.sort()

		#Calculate theoretical option value for each sample
		self.optionValues = []
		for price in samples:
			optionValue = option.getOptionValue(price)
			self.optionValues.append(optionValue)

		#Return option to its original price
		self.option.getOptionValue(originalPrice)


		

na = NormalAnalyzer(option, 1.1, 0.1, 500)

