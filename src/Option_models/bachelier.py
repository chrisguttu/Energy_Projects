import numpy as np
from scipy.stats import norm
from .base_model import OptionModel
from typing import Dict

class Bachelier(OptionModel):
    """ 
    Bachelier normal model (can handle negative prices)
    With the usual greeks
    Parameters: 
    ----------
        F: Float
            Forward price
        K: Float
            Strike
        T: Float
            Time to maturity (in years)
        r: Float
            Risk-free rate
        sigma_n: Float
            Normal volatility (absolute price units)
    """    
    def __init__(self, F: float, K: float, T:float, r: float, sigma_n: float):
        super().__init__(K, T, r, sigma_n)
        self.F = F
        self.sigma_n = sigma_n


    def d(self) -> float:
        return (self.F - self.K) / (self.sigma_n * np.sqrt(self.T))
    

    def call_price(self) -> float:
        """Call price under the Bachelier model."""
        d = self.d()
        return np.exp(-self.r * self.T) * ( (self.F - self.K) * norm.cdf(d) + self.sigma_n * np.sqrt(self.T) * norm.pdf(d) )


    def put_price(self) -> float:
        """Put price under the Bachelier model."""
        d = self.d()
        return np.exp(-self.r * self.T) * ( (self.K - self.F) * norm.cdf(-d) + self.sigma_n * np.sqrt(self.T) * norm.pdf(d) )

    # Greeks for the Bachelier
    def delta(self, option_type: str = "Call") -> float:
        """ Delta for both a call and a put under Bachelier"""
        d = self.d()
        if option_type == "Call":
            return (np.exp(-self.r * self.T) * norm.cdf(d))
        elif option_type == "Put":
            return (np.exp(-self.r * self.T) * (norm.cdf(d) - 1))
        else:
            print("Choose option_type, either Call or Put")


    def gamma(self) -> float:
        """ Gamma under Bachelier"""
        d = self.d()
        return (np.exp(-self.r * self.T) * (norm.pdf(d) / (self.sigma_n * np.sqrt(self.T))))
    

    def vega(self): 
        """ Vega under Bachelier """
        d = self.d()
        return np.exp(-self.r * self.T) * ( np.sqrt(self.T * norm.pdf(d)))  
    

    def theta(self, option_type: str = "Call") -> float: 
        d = self.d()
        if option_type == "Call":
            C = self.call_price()
            t1 = (-self.r * C)
        elif option_type == "Put":
            P = self.put_price()
            t1 = (-self.r * P)
        t2 = - np.exp(-self.r * self.T) * ((self.sigma_n * norm.pdf(d)) / (2 * np.sqrt(self.T)))
        return t1 + t2
    
    
    def rho(self, option_type: str = "Call") -> float:
        d = self.d()
        if option_type == "Call":
            term = ( (self.F - self.K)* norm.cdf(d)) + (self.sigma_n * np.sqrt(self.T) * norm.pdf(d))
        elif option_type == "Put":
            term = ( (self.K - self.F)* norm.cdf(-d)) + (self.sigma_n * np.sqrt(self.T) * norm.pdf(d))
        return (-self.T * np.exp(-self.r * self.T) ) * term
    
 
    def greeks(self, option_type: str = "Call") -> Dict:
        """Dictionary with all the Greeks rounded to 5 decimals."""
        return {
            "Delta": round(self.delta(option_type), 5),
            "Gamma": round(self.gamma(), 5),
            "Vega": round(self.vega(), 5),
            "Theta": round(self.theta(option_type), 5),
            "Rho": round(self.rho(option_type), 5)
        }
