from backend.database.queries import get_stock_data
from backend.engines.ai_engine import analyze_stock


def analyze_symbol(symbol):

    data = get_stock_data(symbol)

    if not data:
        return None

    return analyze_stock(data)
