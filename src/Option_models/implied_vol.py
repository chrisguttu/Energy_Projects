from scipy.optimize import brentq


# TODO: Implement for vectors 
def implied_vol(price: float,
                model_class: type,
                option_class: str = "Call", 
                lower_limit: float = 1e-6,
                upper_limit: float = 5.0,
                **kwargs) -> float:
    """
    Computes the implied volatility for a given option price using a specified model.

    Parameters
    ----------
    price : float
        The observed market price of the option.
    model_class : Type
        The class of the option pricing model (must implement call_price() and put_price()).
    option_class : str, optional
        Type of option: "Call" or "Put". Default is "Call".
    **kwargs : dict
        Additional keyword arguments required to initialize the model (e.g., S0, K, T, r).

    Returns
    -------
    float
       
    """
    def objective(sigma: float) -> float:
        model = model_class(**{**kwargs, "sigma": sigma})
        model_price = model.call_price() if option_class == "Call" else model.put_price()
        return model_price - price
    return brentq(objective, lower_limit, upper_limit)
