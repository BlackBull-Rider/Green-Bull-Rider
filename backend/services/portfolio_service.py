from backend.user_database.connection import get_user_connection


def buy_stock(user_id, symbol, qty, price):

    conn = get_user_connection()

    holding = conn.execute(
        """
        SELECT id, qty, avg_price
        FROM portfolios
        WHERE user_id=?
        AND symbol=?
        """,
        (user_id, symbol)
    ).fetchone()

    if holding:

        holding_id = holding[0]
        old_qty = holding[1]
        old_avg = holding[2]

        new_qty = old_qty + qty

        new_avg = (
            (old_qty * old_avg) +
            (qty * price)
        ) / new_qty

        conn.execute(
            """
            UPDATE portfolios
            SET qty=?,
                avg_price=?
            WHERE id=?
            """,
            (
                new_qty,
                new_avg,
                holding_id
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO portfolios
            (
                user_id,
                symbol,
                qty,
                avg_price
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                symbol,
                qty,
                price
            )
        )

    conn.execute(
        """
        INSERT INTO transactions
        (
            user_id,
            symbol,
            action,
            qty,
            price
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            symbol,
            "BUY",
            qty,
            price
        )
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Buy Added"
    }


def sell_stock(user_id, symbol, qty, price):

    conn = get_user_connection()

    holding = conn.execute(
        """
        SELECT id, qty
        FROM portfolios
        WHERE user_id=?
        AND symbol=?
        """,
        (user_id, symbol)
    ).fetchone()

    if not holding:

        conn.close()

        return {
            "success": False,
            "message": "Stock Not Found"
        }

    holding_id = holding[0]
    current_qty = holding[1]

    if qty > current_qty:

        conn.close()

        return {
            "success": False,
            "message": "Insufficient Qty"
        }

    remaining = current_qty - qty

    if remaining == 0:

        conn.execute(
            """
            DELETE FROM portfolios
            WHERE id=?
            """,
            (holding_id,)
        )

    else:

        conn.execute(
            """
            UPDATE portfolios
            SET qty=?
            WHERE id=?
            """,
            (
                remaining,
                holding_id
            )
        )

    conn.execute(
        """
        INSERT INTO transactions
        (
            user_id,
            symbol,
            action,
            qty,
            price
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            symbol,
            "SELL",
            qty,
            price
        )
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Sell Added"
    }


def get_holdings(user_id):

    conn = get_user_connection()

    rows = conn.execute(
        """
        SELECT
            symbol,
            qty,
            avg_price
        FROM portfolios
        WHERE user_id=?
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    holdings = []

    for row in rows:

        holdings.append({
            "symbol": row[0],
            "qty": row[1],
            "avg_price": row[2]
        })

    return {
        "count": len(holdings),
        "holdings": holdings
    }


def get_transactions(user_id):

    conn = get_user_connection()

    rows = conn.execute(
        """
        SELECT
            symbol,
            action,
            qty,
            price,
            created_at
        FROM transactions
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    transactions = []

    for row in rows:

        transactions.append({
            "symbol": row[0],
            "action": row[1],
            "qty": row[2],
            "price": row[3],
            "created_at": row[4]
        })

    return {
        "count": len(transactions),
        "transactions": transactions
    }
