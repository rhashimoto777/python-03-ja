# queries.py

import sqlite3

def query_orders(db):
    """
    Ordersテーブルからすべての注文を取得し、OrderIDの昇順で並べ替えるように
    このメソッドを実装する

    引数:
        db: データベース接続オブジェクト

    戻り値:
        注文を表すタプルのリスト
    """
    query = "SELECT * FROM Orders ORDER BY OrderID ASC"  # ここにSQLクエリを書いてください
    results = db.execute(query)
    results = results.fetchall()
    return results


def get_orders_range(db, date_from, date_to):
    """
    date_fromからdate_toの期間に発生したすべての注文を取得し、OrderDateの昇順で
    並べ替えるようにこのメソッドを実装する。date_toに発生した注文を含めるが、
    date_fromに発生した注文は除外する
        
    引数:
        db: データベース接続オブジェクト
        date_from: 開始日 (この日は含めない)
        date_to: 開始日 (この日を含める)

    戻り値:
        注文を表すタプルのリスト
    """
    query = f" SELECT * FROM Orders WHERE ('{date_from}' < OrderDate) AND (OrderDate <= '{date_to}') ORDER BY OrderDate ASC"  # ここにSQLクエリを書いてください
    results = db.execute(query)
    results = results.fetchall()
    return results


def get_order_details(db):
    """
    各注文の詳細情報 (商品名や注文数など) を取得し、OrderIDの昇順で並べ替えるように
    このメソッドを実装する

    引数:
        db: データベース接続オブジェクト

    戻り値:
        注文の詳細情報を表すタプルのリスト
    """
    query = """ SELECT OrderDetails.OrderID, Products.ProductName, OrderDetails.Quantity
                FROM OrderDetails
                LEFT JOIN Products ON Products.ProductID = OrderDetails.ProductID
                ORDER BY OrderID ASC"""  # ここにSQLクエリを書いてください
    results = db.execute(query)
    results = results.fetchall()
    return results

def main():
    # SQLiteデータベースに接続
    conn = sqlite3.connect('../data/northwind.db')

    # query_orders関数のテスト
    print("All Orders:")
    # 必要に応じて出力の形式を変更してください
    for order in query_orders(conn):
        print(order)

    # get_orders_range関数のテスト
    print("\nOrders in a specified date range:")
    # データベースにある実際の日付に置き換えてください
    for order in get_orders_range(conn, '1996-07-04', '1996-07-10'):
        print(order)

    # get_order_details関数のテスト
    print("\nOrder Details:")
    # 必要に応じて出力の形式を変更してください
    for detail in get_order_details(conn):
        print(detail)

    # データベース接続を閉じる
    conn.close()

if __name__ == "__main__":
    main()
