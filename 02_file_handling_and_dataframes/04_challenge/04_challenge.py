import pandas as pd
from sklearn.datasets import load_wine

wine_data = load_wine()

wine_df = pd.DataFrame(
    data=wine_data.data,
    columns=wine_data.feature_names,
)
wine_df["target"] = wine_data.target
print(wine_df.head(10))

def chapter(m1, m2):
    print(f'\n\n================== {m1} ==================')
    if m2 is not None:
        print(f'**** {m2} *****')


chapter("Show row DataFrame", None)
print(wine_df.head())

#########################################################################
# __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ 
chapter("1. カスタムインデックスの設定", 
        "データから有用なインサイトを得るために、カスタムインデックスを設定します。")
wine_df_indexed = wine_df.set_index("alcohol").sort_index(ascending=False)
print(wine_df_indexed.head())
del wine_df_indexed

#########################################################################
# __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ 
chapter("2. 複雑なフィルタリング", 
        "複数列の条件指定や範囲指定クエリのような複雑なフィルタリング操作のための関数を作成します。")
def filter(df : pd.DataFrame, target_column : str, thr : int|float, is_gt : bool, is_e : bool):
    if target_column not in df.columns:
        print(f'"{target_column}" does not exist in the wine-DataFrame')
        return None
    if is_gt:
        if is_e:
            return df[df[target_column] >= thr]
        else:
            return df[df[target_column] > thr]
    else:
        if is_e:
            return df[df[target_column] <= thr]
        else:
            return df[df[target_column] < thr]
        
wine_df_filtered = filter(wine_df, "alcohol", 12.0, is_gt=False, is_e=True)
print(wine_df_filtered.head())
del wine_df_filtered

#########################################################################
# __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ 
chapter("3. データ変換", 
        "データ変換を適用します (例: 有益な観察情報や基本統計量を保存する新しい列を作成する)。")
wine_df["magnesium_to_flavanoids"] = wine_df["magnesium"] / wine_df["flavanoids"]

#########################################################################
# __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ __/ 
chapter("4. データの要約", 
        "データをより深く理解するために、データのグループ化、集計、ピボット処理を行います。")
summary_stats = wine_df.groupby("target").agg(
    {"alcohol": ["mean", "std"], "malic_acid": ["mean", "std"]}
)
print(summary_stats)