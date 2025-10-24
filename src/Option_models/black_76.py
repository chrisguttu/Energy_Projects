import numpy as np
from scipy.stats import norm
from .base_model import OptionModel
from typing import Union

class Black76(OptionModel):
    """ 
    Black Scholes 76 taking forward/future as underlying.
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
    
