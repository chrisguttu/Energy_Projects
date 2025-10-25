import numpy as np
from scipy.stats import norm
from .base_model import OptionModel
from typing import Union, Dict

class Black76(OptionModel):
    """ 
    Black Scholes 76 taking forward/future as underlying. 
    Also with the usual greeks
    Parameters:
    ----------
    F : float
        Forward/Futures as underlying
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate
    sigma : float
        Annualized volatility (standard deviation)
    """
    def __init__(self, F: Union[float, np.ndarray], K: float, T: float, r: float, sigma: float):
        super().__init__(K, T, r, sigma)
        self.F = F

    def call_price(self) -> float:
        "Call price for a forward/future as underlying. That is why r is gone as it is accounted for in the underlying"
        d1 = (np.log(self.F / self.K) + 0.5 * self.sigma**2 * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return np.exp(self.r * -self.T) * (self.F * norm.cdf(d1) - self.K * norm.cdf(d2))
    
    def put_price(self) -> float:
        "Put price for a forward/future as underlying. That is why r is gone as it is accounted for in the underlying"
        d1 = (np.log(self.F / self.K) + 0.5 * self.sigma**2 * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return np.exp(self.r * -self.T) * (self.K * norm.cdf(d2) - self.F * norm.cdf(d1))
    
    # Intuition: d1 is the moneyness of the option, the distance betwenn forward and strike.
    # Think the risk adjusted probability that the option will be exercised under the risk neutral measure.
    # d2 is the probability that the option will be exercised under the risk neutral measure. 
    #
    # This makes N(d1) * F the expected value of recieving the asset, and N(d2) * K is the expected Cost of paying the strike

    #TODO: Add greeks
    def delta(self, option_type: str = "Call") -> float:
        """ Delta for Call and Put using Black76 """
        d1, d2 = self.d1_d2(self.F)
        if option_type == "Call":
            return np.exp(-self.r * self.T) * norm.cdf(d1)
        elif option_type == "Put":
            return np.exp(-self.r * self.T) * norm.cdf(-d1)
        else:
            print("Option Type needs to be either Call or Put")
    

    def gamma(self) -> float:
        """ Gamma for Black76, Sensitivity to changes in Delta"""
        d1, d2 = self.d1_d2()
        return (np.exp(-self.r * self.T) * norm.pdf(d1)) / (self.F * self.sigma * np.sqrt(self.T))
    

    def vega(self) -> float: 
        """ Vega for Black76, sensitivity to volatility"""
        d1, d2 = self.d1_d2()
        return self.F * np.exp(-self.r * self.T) * norm.pdf(d1) * np.sqrt(self.T)
    
    def theta(self, option_type: str = "Call") -> float:
        """ Theta for Black76, sensitivity to time"""
        if option_type == "Call":
            d1, d2 = self.d1_d2()
        elif option_type == "Put":
            d1, d2 = -self.d1_d2()
        else: 
            print(" Choose option_type either Call or Put")
        t1 = - ((self.F * np.exp(-self.r * self.T) * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T)))
        t2 = self.r * np.exp(-self.r * self.T) * (self.K * norm.cdf(d2) - self.F * norm.cdf(d1))
        return t1 + t2
    
    def rho(self, option_type: str = "Call") -> float: 
        d1, d2 = self.d1_d2()
        if option_type == "Call":
            return self.T * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif option_type == "Put":
            return -self.T * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        else:
            print("Choos option_type either Call or Put")


    def greeks(self, option_type: str = "Call") -> Dict:
        return {
            "Delta": round(self.delta(option_type), 5),
            "Gamma": round(self.gamma(), 5),
            "Vega": round(self.vega(), 5),
            "Theta": round(self.theta(option_type), 5),
            "Rho": round(self.rho(option_type), 5)
        }





    
