import QuantLib as ql

class OptionPricer:
    def __init__(self, spotPrice, strikePrice, riskFreeRate, dividendYield, volatility, timeToMaturity, optionType):
		# Set up QuantLib dates
        self.calendar = ql.UnitedStates(ql.UnitedStates.NYSE)
        self.valuationDate = ql.Date.todaysDate()
        self.maturityDate = self.valuationDate + int(timeToMaturity)

        # Set evaluation date
        ql.Settings.instance().evaluationDate = self.valuationDate

        # Construct the option payoff and exercise
        if optionType.lower() == 'call':
            self.payoff = ql.PlainVanillaPayoff(ql.Option.Call, strikePrice)
        else:
            self.payoff = ql.PlainVanillaPayoff(ql.Option.Put, strikePrice)

        self.exercise = ql.EuropeanExercise(self.maturityDate)
        self.europeanOption = ql.VanillaOption(self.payoff, self.exercise)

        # Set up market data
        self.spotHandle = ql.QuoteHandle(ql.SimpleQuote(spotPrice))
        self.rateHandle = ql.YieldTermStructureHandle(ql.FlatForward(self.valuationDate, ql.QuoteHandle(ql.SimpleQuote(riskFreeRate)), ql.Actual360()))
        self.dividendHandle = ql.YieldTermStructureHandle(ql.FlatForward(self.valuationDate, ql.QuoteHandle(ql.SimpleQuote(dividendYield)), ql.Actual360()))
        self.volHandle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(self.valuationDate, self.calendar, ql.QuoteHandle(ql.SimpleQuote(volatility)), ql.Actual360()))

        # Set up the Black-Scholes-Merton process
        self.bsmProcess = ql.BlackScholesMertonProcess(self.spotHandle, self.dividendHandle, self.rateHandle, self.volHandle)

        # Set the pricing engine
        self.europeanOption.setPricingEngine(ql.AnalyticEuropeanEngine(self.bsmProcess))

    def getOptionValue(self, newSpotPrice):
        # Update the spot price
        self.spotHandle = ql.QuoteHandle(ql.SimpleQuote(newSpotPrice))
        # Calculate and return the option price
        return self.europeanOption.NPV()

    def getImpliedVolatility(self, marketPrice):
   	    return self.europeanOption.impliedVolatility(marketPrice, self.bsmProcess)

    def getDelta(self):
   		return self.europeanOption.delta()

    def getGamma(self):
   		return self.europeanOption.gamma()

    def getTheta(self):
   		return self.europeanOption.theta()

    def getVega(self):
   		return self.europeanOption.vega()

    def getRho(self):
   		return self.europeanOption.rho()


optionPricer = OptionPricer(0.9, 1, 0.01, 0, 3.2, 5, "call")
print(optionPricer.getOptionValue(0.8))

# Example usage:
# print(calculate_option_value(100, 105, 0.01, 0.02, 0.25, 1, 'call'))
# print(calculate_implied_volatility_and_greeks(100, 105, 0.01, 0.02, 1, 'call', 10))