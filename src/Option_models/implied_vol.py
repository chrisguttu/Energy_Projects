from scipy.optimize import brentq,  minimize_scalar
import numpy as np
from typing import List, Union


    
def implied_vol(price: float,
                model_class: type,
                option_class: str ="Call",
                lower_limit: float =1e-6,
                upper_limit: float =5.0,
                **kwargs) -> Union[float, List[float]]:
    """
    Computes implied volatility for one or more option prices using a specified model.

    Parameters
    ----------
    price : float or list of floats
        Observed market price(s) of the option(s).
    model_class : type
        Option pricing model class (must implement call_price() and/or put_price()).
    option_class : str
        "Call" or "Put".
    lower_limit : float
        Lower bound for volatility search.
    upper_limit : float
        Upper bound for volatility search.
    **kwargs : dict
        Arguments to initialize the model (e.g., F, K, T, r).

    Returns
    -------
    float or list of floats
        Implied volatility(ies).
    """
    # check if model name is Bachelier as the sigma is different.
    vol_key = "sigma_n" if model_class.__name__ == "Bachelier" else "sigma"
    # increase the upper limit as simga_n is absolute price deviation.
    if vol_key == "sigma_n":
        upper_limit = upper_limit * 100

    def objective(vol):
        model = model_class(**{**kwargs, vol_key: vol})
        model_price = model.call_price() if option_class == "Call" else model.put_price()
        return model_price - price

    def single_implied_vol(p):
        try:
            f_low = objective(lower_limit)
            f_high = objective(upper_limit)
            if f_low * f_high > 0:
                raise ValueError("Root not switching sign")
            return brentq(objective, lower_limit, upper_limit)
        except ValueError:
            # Fallback to minimize_scalar
            result = minimize_scalar(
                lambda vol: abs(objective(vol)),
                bounds=(lower_limit, upper_limit),
                method='bounded'
            )
            if result.success:
                return result.x
            else:
                raise RuntimeError("Implied vol calculation failed")

    if isinstance(price, (list, np.ndarray)):
        return [single_implied_vol(p) for p in price]
    else:
        return single_implied_vol(price)