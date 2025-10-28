# Energy Trading Quantitative Research Framework

**In Progress** – A personal quantitative research framework for energy markets, including **power, gas, carbon, and oil**.  

This project is my personal playground to explore, learn, and implement models and techniques that interest me in energy trading and quantitative finance. The repository focuses on building **tools, models, and analysis pipelines** that can be applied to real-world energy trading scenarios.

---

## 🔹 Key Focus Areas

- **Options Pricing:** Implementing and comparing models such as Black–Scholes, Black–76, Bachelier, and spread approximations for energy derivatives.  
- **Volatility Analysis:** Historical, realized, and implied volatility estimation; constructing volatility surfaces and smiles.  
- **Energy Fundamentals:** Analyzing forward curves, fuel spreads, calendar spreads, and correlations across markets (power, gas, carbon, oil).  
- **Trading & Risk Analytics:** Developing tools for portfolio analytics, hedging, and assessing risk metrics like Greeks and Value at Risk.  
- **Research & Experimentation:** Using the framework as a sandbox to test strategies, option models, and market hypotheses.

---

## 🔹 Current Project Structure

- `src/option_pricing/`: Pricing models, Greeks, spread approximations, and implied volatility calculators.  
- `src/data_loader.py`: Functions to collect, clean, and align market data (forwards, spot, historical prices).  
- `src/correlation_vol.py`: Tools to calculate correlations, volatilities, and exponential weighting.  
- `src/portfolio.py`: Portfolio-level analytics and aggregation of exposures.  
- `notebooks/`: Exploratory analysis, model testing, and visualizations.  

---

## 🔹 Goals

1. Build a **modular, reusable, and extensible framework** for energy derivatives and volatility modeling.  
2. Learn and implement **option pricing, risk analytics, and advanced quantitative techniques** in energy markets.  
3. Explore **cross-commodity relationships**, spreads, and the impact of market fundamentals.  
4. Gradually develop towards **volatility trading strategies** and scenario analysis.  

---

## 🔹 Notes

This is a **personal project**; the focus is on learning, experimentation, and research. Some code may be exploratory, and real-world trading applications should always be tested carefully.
