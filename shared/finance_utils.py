"""
Shared financial utilities for the 100 Apps Challenge.
Usage:
    from shared.finance_utils import get_stock_data, get_portfolio_value
"""


def get_stock_data(ticker, period="1y"):
    """Fetch stock data using yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        raise ImportError("Install yfinance: pip install yfinance")

    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    info = stock.info
    return hist, info


def get_multiple_tickers(tickers, period="6mo"):
    """Fetch data for multiple tickers at once."""
    try:
        import yfinance as yf
    except ImportError:
        raise ImportError("Install yfinance: pip install yfinance")

    return yf.download(tickers, period=period)


def calculate_portfolio_value(holdings):
    """
    Calculate current portfolio value.
    holdings: list of dicts with 'ticker', 'shares', 'cost_basis'
    Returns: list of dicts with added 'current_price', 'market_value', 'gain_loss'
    """
    try:
        import yfinance as yf
    except ImportError:
        raise ImportError("Install yfinance: pip install yfinance")

    results = []
    for h in holdings:
        ticker = yf.Ticker(h["ticker"])
        price = ticker.info.get("currentPrice") or ticker.info.get(
            "regularMarketPrice", 0)
        market_value = price * h["shares"]
        cost_total = h["cost_basis"] * h["shares"]
        results.append({
            **h,
            "current_price":
            price,
            "market_value":
            market_value,
            "gain_loss":
            market_value - cost_total,
            "gain_loss_pct": ((market_value - cost_total) / cost_total *
                              100) if cost_total else 0,
        })
    return results
