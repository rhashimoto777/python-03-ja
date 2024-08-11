
# SQLとPython＋Chinookデータベース

import sqlite3
from pathlib import Path
import os

# chinook.dbデータベースに接続
os.chdir(Path(__file__).parent)
conn = sqlite3.connect('../data/chinook.db')
db = conn.cursor()

# アーティストの数
def number_of_artists(db):
    query = "SELECT COUNT(*) FROM artists"
    db.execute(query)
    results = db.fetchall()
    return results[0][0]
# print(number_of_artists(db))

# アーティストのリスト
def list_of_artists(db):
    query = "SELECT Name FROM artists ORDER BY Name ASC"
    db.execute(query)
    results = db.fetchall()
    return [e[0] for e in results]
# print(list_of_artists(db))

# 「愛」をテーマにしたアルバムのリスト
def albums_about_love(db):
    query = "SELECT Title FROM albums WHERE Title LIKE '%love%' ORDER BY Title ASC"
    db.execute(query)
    results = db.fetchall()
    return [e[0] for e in results]
# print(albums_about_love(db))

# 指定された再生時間よりも長い楽曲数
def tracks_longer_than(db, duration):
    query = f"SELECT COUNT(*) FROM tracks WHERE Milliseconds > {duration}"
    db.execute(query)
    results = db.fetchall()
    return results[0][0]
print(tracks_longer_than(db, 100))

# 最も楽曲数が多いジャンルのリスト
def genres_with_most_tracks(db):
    query = """
    SELECT genres.Name, count
    FROM 
    (
        SELECT GenreID, count(*) as count
        FROM tracks
        GROUP BY GenreID
    ) as track_group
    INNER JOIN genres ON track_group.GenreID = genres.GenreID
    ORDER BY count DESC
    """
    # SELECT columns FROM table1 INNER JOIN table2 ON table1.column = table2.column;
    db.execute(query)
    results = db.fetchall()
    return results
# print(genres_with_most_tracks(db))

# スクリプトの最後で必ずデータベース接続を閉じる
conn.close()
