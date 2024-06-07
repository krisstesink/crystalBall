from optionPricer import OptionPricer
from scipy import stats



class NormalAnalyzer:
	def __init__(self, option, targetPrice):
		#Set up class attributes
		self.option = option
		self.targetPrice = targetPrice

		#Sample from a normal distribution around the price target
		normDist = stats.norm(loc = targetPrice, scale = standardDev)
		samples = normDist.rvs(size = samples)
		samples.sort()

		#Calculate theoretical option value for each sample
		self.optionValues = []
		for price in samples:
			optionValue = option.getOptionValue(price)
			self.optionValues.append(optionValue)


	def getMean(self):
		return sum(self.optionValues)/len(self.optionValues)

	


		
option = OptionPricer(0.9, 1, 0.01, 0, 3.2, 10, "call")
for i in range(10):
	option.updateParams(timeToValuation = i)
	print("npv = ", option.europeanOption.NPV())
	print("theta = ", option.getTheta())



