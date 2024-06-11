import QuantLib as ql

class Option:
    def __init__(self, underlyingPrice, strikePrice, riskFreeRate, dividendYield, volatility, timeToMaturity, optionType):
        self.originalPrice = underlyingPrice
        self.originalTimeToMaturity = timeToMaturity
        self.originalVolatility = volatility
        self.optionType = optionType
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
        self.spotHandle = ql.QuoteHandle(ql.SimpleQuote(underlyingPrice))
        self.rateHandle = ql.YieldTermStructureHandle(ql.FlatForward(self.valuationDate, ql.QuoteHandle(ql.SimpleQuote(riskFreeRate)), ql.Actual360()))
        self.dividendHandle = ql.YieldTermStructureHandle(ql.FlatForward(self.valuationDate, ql.QuoteHandle(ql.SimpleQuote(dividendYield)), ql.Actual360()))
        self.volHandle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(self.valuationDate, self.calendar, ql.QuoteHandle(ql.SimpleQuote(volatility)), ql.Actual360()))

        # Set up the Black-Scholes-Merton process
        self.bsmProcess = ql.BlackScholesMertonProcess(self.spotHandle, self.dividendHandle, self.rateHandle, self.volHandle)

        # Set the pricing engine
        self.europeanOption.setPricingEngine(ql.AnalyticEuropeanEngine(self.bsmProcess))

    def refreshOption(self, reset=False):
        if(reset==True):
            self.maturityDate = self.valuationDate + int(self.originalTimeToMaturity)
            self.exercise = ql.EuropeanExercise(self.maturityDate)
            self.europeanOption = ql.VanillaOption(self.payoff, self.exercise)

            self.spotHandle = ql.QuoteHandle(ql.SimpleQuote(self.originalPrice))
            self.bsmProcess = ql.BlackScholesMertonProcess(self.spotHandle, self.dividendHandle, self.rateHandle, self.volHandle)
            self.europeanOption.setPricingEngine(ql.AnalyticEuropeanEngine(self.bsmProcess))
            return

        self.exercise = ql.EuropeanExercise(self.maturityDate)
        self.europeanOption = ql.VanillaOption(self.payoff, self.exercise)
        self.bsmProcess = ql.BlackScholesMertonProcess(self.spotHandle, self.dividendHandle, self.rateHandle, self.volHandle)
        self.europeanOption.setPricingEngine(ql.AnalyticEuropeanEngine(self.bsmProcess))

    def value(self):
        return self.europeanOption.NPV() 

    def updateParams(self, underlyingPrice=False, timeToValuation=False, newVolatility=False):
        # Check each param and update values if needed
        if(underlyingPrice!=False):
            print("underlying = ", underlyingPrice)
            self.spotHandle = ql.QuoteHandle(ql.SimpleQuote(underlyingPrice))

        if(timeToValuation!=False):
            self.valuationDate = ql.Date.todaysDate() + int(timeToValuation)
            if(newVolatility==False):
                self.volHandle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(self.valuationDate, self.calendar, ql.QuoteHandle(ql.SimpleQuote(self.originalVolatility)), ql.Actual360()))

        if(newVolatility!=False):
            self.volHandle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(self.valuationDate, self.calendar, ql.QuoteHandle(ql.SimpleQuote(newVolatility)), ql.Actual360()))

        self.refreshOption()

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

