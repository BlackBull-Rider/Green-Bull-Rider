from backend.database.connection import get_connection


def get_stock_data(symbol):

    conn = get_connection()

    query = """
    SELECT *
    FROM stock_master sm
    LEFT JOIN fundamental_data fd
        ON sm.symbol = fd.symbol
    LEFT JOIN latest_indicators li
        ON sm.symbol = li.symbol
    WHERE sm.symbol = ?
    """

    row = conn.execute(query, (symbol,)).fetchone()

    if not row:
        return None

    columns = [x[0] for x in conn.execute(query, (symbol,)).description]

    conn.close()

    return dict(zip(columns, row))
