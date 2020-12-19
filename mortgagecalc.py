
import pandas as pd
import numpy as np
import os

class MortgagePayment():
    """
    A class used to represent a Mortgage payment
    
    WARNING: this class is dependent on 30-year-fixed-mortgage-rate-chart.csv data.
    It must be located in the data directory

    Attributes
    ----------
    years : int or numpy.ndarray dtype=ints, must be same length as selling_prices
        a 4 digit number representing any year 1971-2020
    selling_prices : int or numpy.ndarray dtype=ints, must be same length as years
        the selling price of the house. For example 300000.
    D: float
        The downpayment percentage converted to decimal. For example, 20% downpayment is
         represented as 0.2
    n: int
        The number of periods to pay off mortgage, which should be in time units of Months.
        for example 30 year loan, is 360 Months (30 * 12).
    p_tax_r: float
        The decimal property tax percentage converted to decimal. For example 2.14%
        property tax is 0.0214.
    Ms: float or numpy.ndarray dtype=floats
        Calculated mortgage payment(s)
    p_tax: float
        Calculated dollars per month in property tax
    Ms_plus_p_tax:
        Added Ms + p_tax together to output a more realistic mortgage payment
    
    Methods
    -------
    findingAnnualPercentageRates()
        Based on the year finds the May property tax percentage
    monthlyMortgage()
        Finds mortage based on the formula
        M = P * r * (1 + r)**n  / ((1 + r)**n - 1)
        where
        M = Monthly Payment
        P = Selling price - the Downpayment
        r = is the Annual Percentage Rate converted to decimal divided by 12 (because of 12 months)
        n = is the number of periods in months
    """
    def __init__(self, years, selling_prices):
        """
        Parameters
        ----------
        years : int or 1D numpy.ndarray dtype=ints, must be same length as selling_prices
            a 4 digit number representing any year 1971-2020
        selling_prices : int or 1D numpy.ndarray dtype=ints, must be same length as years
            the selling price of the house. For example 300000.
        """
        self.years = years
        self.selling_prices = selling_prices
        self.D = 0.2
        self.n = 30 * 12
        self.p_tax_r = .02
        self.Ms = None
        self.p_tax = None
        self.Ms_plus_p_tax = None
        self.monthlyMortgage()

    def findingAnnualPercentageRates(self):
        """
        Based on the year finds the May property tax percentage
        """
        filename = os.path.join("data", "30-year-fixed-mortgage-rate-chart.csv")
        df = pd.read_csv(filename, index_col = 0, header = 8)
        df.rename(columns=lambda x: x.strip(), inplace=True) #stripping whitespace from column headers
        
        aprs = []

        if type(self.years) == int:
            date = "{}-05-01".format(self.years)
            apr = df['value'].xs(date)
            return apr
        if len(self.years) >1:
            for year in self.years:
                date = "{}-05-01".format(year)
                apr = df['value'].xs(date)
                aprs.append(apr)
            return np.array(aprs)

    def monthlyMortgage(self):
        """
        Finds mortage based on the formula
        M = P * r * (1 + r)**n  / ((1 + r)**n - 1)
        where
        M = Monthly Payment
        P = Selling price - the Downpayment
        r = is the Annual Percentage Rate converted to decimal divided by 12 (because of 12 months)
        n = is the number of periods in months
        """
        SPs = self.selling_prices
        Ps = SPs - self.D*SPs
        aprs = self.findingAnnualPercentageRates()
        rs = (aprs/100)/12
        self.Ms = Ps * rs * (1 + rs)**self.n  / ((1 + rs)**self.n - 1)
        self.p_tax = SPs*self.p_tax_r / 12

        self.Ms_plus_p_tax = self.Ms + self.p_tax


