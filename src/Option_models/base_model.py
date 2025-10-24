import numpy as np
from abc import ABC, abstractmethod

class OptionModel(ABC):
    def __init__(self, K, T, r, sigma):
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    # Force Call and put implementation for all subclasses
    @abstractmethod
    def call_price(self):
        pass

    @abstractmethod
    def put_price(self):
        pass

    # Create the d1 and d2 for the BS models. 
    def d1_d2(self, S):
        d1 = ((np.log(S/self.K)) + (self.r + 0.5*self.sigma**2)*self.T)/ (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return d1, d2
    
