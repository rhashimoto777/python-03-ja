import sqlite3
import pandas as pd
import re
from datetime import datetime

def f1(db):
    """
    1. 従業員の年齢分析
        目的: 従業員の年齢分布を分析してまとめます。

        データソース: NorthwindデータベースのEmployeesテーブル
        タスク
            各従業員の現在の年齢を計算します。
            従業員の年齢の平均値、中央値、最頻値、標準偏差を計算して表示します。
        主なスキル: データベースの操作、日付と時間の操作、統計分析
    """
    query = "SELECT BirthDate FROM Employees"
    df_age = pd.read_sql_query(query, db)
    df_age['Age'] = df_age['BirthDate'].apply(calc_age)

    mean = df_age['Age'].mean()
    median = df_age['Age'].median()
    mode = df_age['Age'].mode()[0] 
    std_dev = df_age['Age'].std()

    print("\n\n=================== 1. 従業員の年齢分析 ===================")
    print(f'平均値   : {mean}')
    print(f'中央値   : {median}')
    print(f'最頻値   : {mode}')
    print(f'標準偏差 : {std_dev:.1f}')

def calc_age(date_str):
    current_date = datetime.today()
    # 解1
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
    if date_pattern.match(date_str):
        try:
            values = date_str.split('-')
            birth_year = int(values[0])
            birth_month = int(values[1])
            birth_day = int(values[2])
            age = current_date.year - birth_year - ((current_date.month, current_date.day) < (birth_month, birth_day))
            return age
        except:
            pass
    return None

    # 解2（これを使う場合は独立関数にせずラムダ関数にした方が良いが，便宜上独立関数に書いておく）
    # dt = pd.to_datetime(date_str)
    # return current_date.year - dt.year - ((current_date.month, current_date.day) < (dt.month, dt.day))

def f2(db):
    """
    2. 顧客の所在国の分析
        目的: 顧客の所在国を調査します。

        データソース: NorthwindデータベースのCustomersテーブル
        タスク
            顧客を国別にグループ化します。
            各国の顧客数の合計を計算して表示します。
            顧客数が最大の国と最小の国を特定します。
        主なスキル: データベースのクエリ、データのグループ化、基本的なデータ分析
    """
    # 解1
    # query = """
    # SELECT Country, COUNT(*)
    # FROM Customers
    # GROUP BY Country
    # ORDER BY COUNT(*) DESC;
    # """
    # country_counts = db.execute(query)
    # country_counts = country_counts.fetchall()

    # max_count = country_counts[0][1]
    # min_count = country_counts[-1][1]

    # print(country_counts[0])
    # print(country_counts[-1])

    # print("\n\n=================== 2. 顧客の所在国の分析 ===================")
    # indent = 11
    # print("各国の顧客数の合計 : ")
    # for elem in country_counts:
    #     print(f' - {elem[0].ljust(indent)} : {elem[1]}')
        
    # print("顧客数が最大の国 : ")
    # for elem in [x for x in country_counts if x[1] == max_count]:
    #     print(f' - {elem[0].ljust(indent)} : {elem[1]}')
        
    # print("顧客数が最小の国 : ")
    # for elem in [x for x in country_counts if x[1] == min_count]:
    #     print(f' - {elem[0].ljust(indent)} : {elem[1]}')

    # 解2
    df = pd.read_sql_query("SELECT * FROM Customers", db)
    country_counts = df.groupby('Country').size()
    max_count = country_counts.max()
    min_count = country_counts.min()

    print("\n\n=================== 2. 顧客の所在国の分析 ===================")
    print("各国の顧客数:")
    print(country_counts)

    indent = 11
    print("\n顧客数が最大の国:")
    for country, customers in country_counts.items():
        if customers == max_count:
            print(f'{country.ljust(indent)} : {customers}')

    print("\n顧客数が最小の国:")
    for country, customers in country_counts.items():
        if customers == min_count:
            print(f'{country.ljust(indent)} : {customers}')

def f3(db):
    """
    3. 注文の間隔に関するインサイト
        目的: 注文の間隔に関するインサイトを取得します。

        データソース: NorthwindデータベースのOrdersテーブル
        タスク
            注文の日付をdatetime形式に変換します。
            注文の間隔 (例: 前回の注文から今回の注文までの期間) の平均を計算します。
            注文の日付に関する基本統計量を提示します。
        主なスキル: 時系列分析、基本統計量の取得
    """
    query = "SELECT OrderDate FROM Orders"
    df_orders = pd.read_sql_query(query, db)

    df_orders['OrderDate'] = pd.to_datetime(df_orders['OrderDate'])
    order_date_stats = df_orders['OrderDate'].describe(datetime_is_numeric=True)

    df_orders = df_orders.sort_values(by='OrderDate', ascending = True)
    df_orders['OrderInterval'] = df_orders['OrderDate'].diff().dt.days
    order_intervals = df_orders['OrderInterval'].dropna()

    print("\n\n=================== 3. 注文の間隔に関するインサイト ===================")
    print(f'注文の間隔の平均             : {order_intervals.mean():.2f}日')
    print(f'\n注文の日付に関する基本統計量 : ')
    print(order_date_stats)

def f4(db):
    """
    4. サプライヤーの商品価格の比較
        目的: サプライヤー間で商品価格を比較して分析します。

        データソース: NorthwindデータベースのProductsテーブルとSuppliersテーブル
        タスク
            SupplierIDにもとづいて2つのテーブルをマージします。
            サプライヤーごとに商品の平均価格を計算します。
            平均価格を表示してパターンや傾向を特定します。
        主なスキル: データのマージ、集計、比較分析
    """
    # 解1
    # query = '''
    # SELECT SupplierName, AVG(Price)
    # FROM Products
    # JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID
    # GROUP BY SupplierName
    # ORDER BY AVG(Price) DESC

    # '''
    # results = db.execute(query)
    # results = results.fetchall()

    # print("\n\n=================== 4. サプライヤーの商品価格の比較 ===================")
    # for elem in results:
    #     print(f'{elem[0].ljust(45)}{elem[1]:.2f}')

    # 解2
    df_products = pd.read_sql_query("SELECT * FROM Products", db)
    df_suppliers = pd.read_sql_query("SELECT * FROM Suppliers", db)
    df_merged = df_products.merge(df_suppliers, on='SupplierID')

    average_price_per_supplier = df_merged.groupby('SupplierName')['Price'].mean().sort_values(ascending=False)

    print("\n\n=================== 3. 注文の間隔に関するインサイト ===================")
    print(average_price_per_supplier)

def f5(db):
    """
    5. 比較分析: 注文日と注文数の関係
        目的: 注文日と注文数の関係を調べます。

        データソース: NorthwindデータベースのOrdersテーブルとOrderDetailsテーブル
        タスク
            OrderIDにもとづいて両テーブルのデータをマージします。
            各月や各年の平均注文数など、注文日と注文数の関係を分析します。
        主なスキル: データのマージ、日時分析、相関分析
    """
    query = '''
    SELECT OrderDate
    FROM Orders
    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
    '''
    df = pd.read_sql_query(query, db)

    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['Year'] = df['OrderDate'].dt.year
    df['Month'] = df['OrderDate'].dt.month

    monthly_order_counts = df.groupby(['Year', 'Month']).size().reset_index(name='OrderCount')
    yearly_order_counts = df.groupby('Year').size().reset_index(name='OrderCount')

    monthly_avg_order_counts = monthly_order_counts.groupby('Month')['OrderCount'].mean().reset_index(name='AverageOrderCount')
    yearly_avg_order_counts = yearly_order_counts.groupby('Year')['OrderCount'].mean().reset_index(name='AverageOrderCount')

    print("\n\n=================== 5. 比較分析: 注文日と注文数の関係 ===================")
    print("全ての月の注文数一覧:")
    print(monthly_order_counts)

    print("\n月ごとの平均注文数:")
    print(monthly_avg_order_counts)

    print("\n年ごとの平均注文数:")
    print(yearly_avg_order_counts)

def main():
    with sqlite3.connect('./04_sql_and_python/data/northwind.db') as conn:
        f1(conn)
        f2(conn)
        f3(conn)
        f4(conn)
        f5(conn)


if __name__ == "__main__":
    main()

