import numpy as np
from scipy.stats import norm
from .base_model import OptionModel

class Bachelier(OptionModel):
    """ 
    Bachelier normal model (can handle negative prices)
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
