import numpy as np
from scipy.stats import norm
from .base_model import OptionModel
from typing import Union

class BlackScholes(OptionModel):
    """ 
    Traditional Black-Scholes model using spot price as underlying.
    Parameters:
    ----------
    S0 : Union[float, np.ndarray] ( can be spot or array of spots to price multiples at same time.)
        Spot price of the underlying asset
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate
    sigma : float
        Annualized volatility (standard deviation)
    """
    def __init__(self, S0: Union[float, np.ndarray], K: float, T: float, r: float, sigma: float):
        super().__init__(K, T, r, sigma)

        self.S0 = S0
        
    def call_price(self) -> float:
        " Call price using stock spot as underlying. Remeber not to discount S0"
        d1, d2 = self.d1_d2(self.S0)
        return (self.S0 * norm.cdf(d1) - (np.exp(-self.r * self.T) * self.K * norm.cdf(d2)))
    
    def put_price(self)-> float:
        " Put price using stock spot as underlying. Remeber not to discount S0"
        d1, d2 = self.d1_d2(self.S0)
        return (np.exp(-self.r * self.T) * self.K * norm.cdf(d2)) - (self.S0 * norm.cdf(d1))
    
    # Intuition: d1 is the moneyness of the option, the distance betwenn forward and strike.
    # Think the risk adjusted probability that the option will be exercised under the risk neutral measure.
    # d2 is the probability that the option will be exercised under the risk neutral measure. 
    #
    # This makes N(d1) * F the expected value of recieving the asset, and N(d2) * K is the expected Cost of paying the strike

    #TODO: Add greeks
