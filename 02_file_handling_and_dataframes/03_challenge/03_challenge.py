"""
目的: 
    アイリスのデータセットの探索と拡張を通じて、
    Pandasを使用したデータ操作、特徴量エンジニアリング、分析について理解を深めます。

概要: 
    アイリスのデータセットは、機械学習や統計学の分野で従来から使われています。
    150種類のアイリスの花の観察結果 (ガクの長さ、ガクの幅、花弁の長さ、花弁の幅の測定値など) と、品種の分類で構成されています。
    品種には、アイリス・セトーサ (Iris Setosa)、アイリス・バーシコラー (Iris Versicolour)、アイリス・ヴァージニカ (Iris Virginica) などがあります。
"""

import pandas as pd
from sklearn import datasets
from pathlib import Path
import os
chap_num = 1

def chapter():
    global chap_num
    print(f'\n==================== [{chap_num}] =================')
    chap_num += 1

def section(msg):
    print(f"\n****** {msg} ******")

# _______________________________________________________________
# __/ __/ __/ __/ __/ 1. データの読み込み __/ __/ __/ __/ __/ __/ 
"""
アイリスのデータセットをDataFrameに読み込みます
"""
chapter()

# アイリスのデータセットを読み込み、DataFrameに変換する
iris = datasets.load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)

# 品種の列を追加し、0～2の番号を記入する (各番号が異なる品種を表す)
iris_df['species'] = iris.target
print(iris_df)

# _______________________________________________________________
# __/ __/ __/ __/ __/ 2. データのクリーニングと検証 __/ __/ __/ __/
"""
欠損値またはnull値の存在を確認します。
各列のデータ型を確認します (例: 測定値の場合は数値型)。
"""
chapter()
section("欠損値またはnull値の存在を確認")
print(iris_df.isnull().sum())

section("各列のデータ型を確認")
print(iris_df.dtypes)


# _______________________________________________________________
# __/ __/ __/ __/ __/ 3. 基本的な分析と基本統計量 __/ __/ __/ __/ 
"""
数値型の各特徴量について、基本統計量 (平均値、中央値、標準偏差) を計算します。
DataFrameを新規作成します。各行が1つの特徴量を表し、各列に計算した統計情報を格納するようにします。これをCSV形式で出力します。
"""
chapter()
section("数値型の各特徴量について、基本統計量 (平均値、中央値、標準偏差) を計算します。DataFrameを新規作成します。各行が1つの特徴量を表し、各列に計算した統計情報を格納するようにします。")
stats_df = pd.DataFrame({
    '平均値'    : iris_df.mean(),
    '中央値'    : iris_df.median(),
    '標準偏差'  : iris_df.std()
})
print(stats_df)

section("これをCSV形式で出力します。")
cur_dir = Path(__file__).parent
stats_df.to_csv(os.path.join(cur_dir, "statistics_df.csv"), index=True, encoding='utf-8-sig')

# _______________________________________________________________
# __/ __/ __/ __/ __/ 4. 特徴量エンジニアリング __/ __/ __/ __/ __/
"""
新しい列 sepal_area (ガクの面積) を追加します。この値は、ガクの長さ×ガクの幅で算出します。
別の列 petal_area (花弁の面積) も追加します。この値は、花弁の長さ×花弁の幅で算出します。
これらの新しい特徴量の基本統計量を算出し、統計情報のDataFrameに追加します。
"""
chapter()
section("「sepal_area (ガクの面積) 」「petal_area (花弁の面積)」の列追加")
iris_df["sepal_area"] = iris_df["sepal length (cm)"] * iris_df["sepal width (cm)"]
iris_df["petal_area"] = iris_df["petal length (cm)"] * iris_df["petal width (cm)"]
print(iris_df)

section("これらの新しい特徴量の基本統計量を算出し、統計情報のDataFrameに追加")
df_tmp = iris_df[["sepal_area", "petal_area"]]
df_add = pd.DataFrame({'平均値':df_tmp.mean(), '中央値':df_tmp.median(), '標準偏差':df_tmp.std()})
stats_df = pd.concat([stats_df, df_add])
del df_tmp, df_add
print(stats_df)

# _______________________________________________________________
# __/ __/ __/ __/ __/ 5. データのフィルタリング __/ __/ __/ __/ __/
"""
与えられた基準にもとづいてデータをフィルタリングする関数を書きます (例: ある列の値がしきい値を下回る行を除外する)。
"""
chapter()
def filter(df, column_name, thr_value):
    """
    指定された列が閾値を下回る行を除外したDataFrameを返す。
    """
    if column_name in df.columns:
        return df[df[column_name] >= thr_value]
    else:
        raise Exception(f'Column name "{column_name}" does not exist in the DataFrame.')

section("例として、sepal length (cm)が5.0以上のものを抽出する")
iris_df_filterd = filter(iris_df, "sepal length (cm)", 5.0)
print(iris_df_filterd)


# _______________________________________________________________
# __/ __/ __/ __/ __/ 6. データのエクスポート __/ __/ __/ __/ __/ __
"""
DataFrameをCSV形式で保存します。
このチャレンジの成果物は自動採点されませんが、GitHubにプッシュする際に自分のDataFrameを含めるようにしてください。
"""
iris_df.to_csv(os.path.join(cur_dir, "iris_df.csv"), index=True, encoding='utf-8-sig')
