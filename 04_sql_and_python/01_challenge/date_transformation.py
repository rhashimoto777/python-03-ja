import sqlite3
import pandas as pd
import re

def transform_date_format(date_str):
    """
    日付文字列の形式を 'YYYY-MM-DD' から 'DD/MM/YYYY' に変換する
    入力が想定された形式と異なる場合は、元の文字列を返す
    
    引数:
    date_str (文字列): 'YYYY-MM-DD' 形式の日付文字列

    戻り値:
    文字列: 'DD/MM/YYYY' 形式に変換した日付文字列、または元の文字列 (形式が無効だった場合)
    """
    # 日付形式を変換するロジックを実装してください
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
    if date_pattern.match(date_str):
        try:
            values = date_str.split('-')
            month = int(values[1])
            day = int(values[2])
            if 1 <= month <= 12 and 1 <= day <= 31:
                values.reverse()
                return '/'.join(values)
        except:
            pass
    return date_str


def apply_date_transformation(db_path, table_name, column_name):
    """
    SQLiteテーブルの指定した列にtransform_date_format関数を適用する

    引数:
    db_path (文字列): SQLiteデータベースへのパス
    table_name (文字列): データベース内のテーブル名
    column_name (文字列): 日付形式の変換を適用する列名

    戻り値:
    DataFrame: 変換した列のデータを含むPandas DataFrame
    """
    with sqlite3.connect(db_path) as conn:
        # 指定したテーブルをDataFrameに読み込んでください
        # 指定した列にtransform_date_format関数を適用してください
        # 変更後のDataFrameを返してください
        query = f"SELECT {column_name} FROM {table_name}"
        df = pd.read_sql(query, conn)
        return df.applymap(transform_date_format)


# 使用例 (受講者はこれを変更してください)
if __name__ == "__main__":
    db_path = '../data/northwind.db'
    table_name = 'Orders' # 受講者はこれを確認するか変更してください
    column_name = 'OrderDate' # 受講者はこれを確認するか変更してください
    transformed_df = apply_date_transformation(db_path, table_name, column_name)
    print(transformed_df.head())
