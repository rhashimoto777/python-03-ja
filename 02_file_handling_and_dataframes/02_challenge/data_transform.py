import csv
import json
import os

import logging

# ログの設定
logging.basicConfig(level=logging.DEBUG,
                    format='LOG_%(levelname)s [%(asctime)s][%(name)s][%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[
                        logging.StreamHandler()  # コンソール出力
                    ])

# ロガーの取得
logger = logging.getLogger(__name__)

#----------------------------------------------------------------------------------------
def read_csv(file_path):
    """
    CSVファイルを読み取り、その内容を辞書のリストで返す

    :引数 file_path: 文字列 - CSVファイルへのパス
    :戻り値: リスト - CSVの列を表す辞書のリスト
    """
    # 「CSVの列を表す辞書」のリスト であることから、単純に list(csv.reader(f)) する課題ではないと解釈する。

    ##### 書き方 1パターン目 #####
    with open(file_path, 'r') as f:   
        reader = csv.reader(f)
        ret1 = []
        header = []
        for i, row in enumerate(reader):
            dict = {}
            if i == 0:
                for elem in row:
                    header.append(elem)
            else:
                for j, elem in enumerate(row):
                    dict[header[j]] = elem
                ret1.append(dict)
        logger.info(f'ret1 : {ret1}')

    ##### 書き方 2パターン目 ##### 
    with open(file_path, 'r') as f:   
        reader = csv.reader(f)
        reader_l = list(reader)
        header = []
        for elem in reader_l[0]:
            header.append(elem)
            
        ret2 = []
        for row in reader_l[1:]:
            dict = {}
            for i, elem in enumerate(row):
                dict[header[i]] = elem
            ret2.append(dict)
        logger.info(f'ret2 : {ret2}')

    ##### 書き方 3パターン目 #####
    with open(file_path, 'r') as f:   
        reader = csv.reader(f)
        reader_l = list(reader)
        header = reader_l[0]
        ret3 = [{h:d for h, d in zip(header, row)} for row in reader_l[1:]]
        logger.info(f'ret3 : {ret3}')
    return ret1
                
# filepath = "./02_file_handling_and_dataframes/02_challenge/sample.csv"
# read_csv(filepath)

#----------------------------------------------------------------------------------------
def csv_to_json(csv_data):
    """
    CSVデータ (辞書のリスト) を受け取り、それをJSON形式 (文字列) に変換する

    :引数 csv_data: リスト - 辞書のリストで表したCSVデータ
    :戻り値: 文字列 - JSON形式で表したデータ
    """
    logger.info(f'in : {csv_data}')
    ret = json.dumps(csv_data)
    logger.info(f'ret : {ret}')
    return ret

# filepath = "./02_file_handling_and_dataframes/02_challenge/sample.csv"
# data = read_csv(filepath)
# csv_to_json(data)

#----------------------------------------------------------------------------------------
def write_json(json_data, file_path):
    """
    JSONデータをファイルに書き込む

    :param json_data: 文字列 - 書き込むJSONデータ
    :param file_path: 文字列 - JSONファイルへのパス
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            logger.info(f'in : {json_data}')
            json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True)
            logger.info("Success")
    except Exception as e:
        logger.error(e)
        raise Exception(e)

#----------------------------------------------------------------------------------------
def read_json(file_path):
    """
    JSONファイルを読み取ってその内容を返す

    :引数 file_path: 文字列 - JSONファイルへのパス
    :戻り値: JSONファイルの内容
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            logger.info(f'the data is below\n{data}')
            return data
    except Exception as e:
        logger.error(e)
        raise Exception(e)

def json_to_csv(json_data):
    """
    JSONデータを受け取り (通常は辞書のリスト)、それをCSV形式 (文字列) に変換する

    :引数 json_data: JSONデータ
    :戻り値: 文字列 - CSV形式で表したデータ
    """
    csv = ""
    for i, row in enumerate(json_data):
        if i == 0:
            csv += ",".join(row.keys()) + "\n"
        d = [str(e) for e in row.values()]
        csv += ",".join(d) + "\n"
    logger.info(f'the data is below\n{csv}')
    
    # csv = []
    # header = []
    # for i, row in enumerate(json_data):
    #     if i == 0:
    #         header = [k for k in row.keys()]
    #         csv.append(header)
    #     csv.append([row[k] for k in header])
    # logger.info(f'the data is below\n{csv}')
    return csv

# filepath = "./02_file_handling_and_dataframes/02_challenge/sample.json"
# data = read_json(filepath)
# json_to_csv(data)

#----------------------------------------------------------------------------------------
def write_csv(csv_data, file_path):
    """
    CSVデータをファイルに書き込む

    :引数 csv_data: 文字列 - 書き込むCSVデータ
    :引数 file_path: 文字列 - CSVファイルへのパス
    """
    try:
        with open(file_path, 'w', newline='') as f:
            logger.info(f'in : {csv_data}')
            writer = csv.writer(f)
            writer.writerows(csv_data)
            logger.info("Success")
    except Exception as e:
        logger.error(e)
        raise Exception(e)

#----------------------------------------------------------------------------------------
def validate_data(data, data_type):
    """
    データの整合性を確認する (例: CSVの列数に一貫性があること)

    :引数 data: 検証対象のデータ
    :引数 data_type: 文字列 - データ型 ('CSV' または 'JSON')
    :戻り値: bool - データが有効な場合はTrue、無効な場合はFalse
    """
    if data_type == 'CSV':
        # 「CSVのデータ」が辞書型で送られるのか、文字列で送られてくるのかの自由度があるが、
        #  本関数のtestファイルを見る限り「行ごとの辞書のリスト」で渡されるものと想定する。
        try:
            first_row = None
            ret = True
            for i, row in enumerate(data):
                if i == 0:
                    first_row = row
                else:
                    if sorted(first_row.keys()) != sorted(row.keys()):
                        ret = False
                        break
            logger.info("CSV, Success")
            return ret
        except Exception as e:
            logger.error(e)
            raise Exception(e)
    elif data_type == 'JSON':
        # 「JSONのデータ」が辞書型なのか文字列型なのか自由度があるが、
        # csvに倣って「行ごとの辞書リスト」で渡されるとする。（そうするとCSVと処理が同一になるが…）
        try:
            first_row = None
            ret = True
            for i, row in enumerate(data):
                if i == 0:
                    first_row = row
                else:
                    if sorted(first_row.keys()) != sorted(row.keys()):
                        ret = False
                        break
            logger.info("JSON, Success")
            return ret
        except Exception as e:
            logger.error(e)
            raise Exception(e)
    else:
        e = "Invalid data_type"
        logger.error(e)
        raise Exception(e)

#----------------------------------------------------------------------------------------
def process_directory(directory_path):
    """
    指定されたディレクトリにあるすべてのCSVまたはJSONファイルを確認し、適切に変換する

    :引数 directory_path: 文字列 - 処理対象のディレクトリへのパス
    """
    fnames = os.listdir(directory_path)
    converted_prefix = "CONVERTED_"
    csv_fnames  = [f for f in fnames if (".csv" in f) and (converted_prefix not in f)]
    json_fnames = [f for f in fnames if (".json" in f) and (converted_prefix not in f)]
    for cname in csv_fnames:
        cpath = os.path.join(directory_path, cname)
        cdata = read_csv(cpath)

        jdata = json.loads(csv_to_json(cdata))
        jname = converted_prefix + cname.rstrip(".csv") + ".json"
        jpath = os.path.join(directory_path, jname)
        write_json(jdata, jpath)
        logger.info(f'')
    del cname, cpath, cdata, jdata, jname, jpath
    
    for jname in json_fnames:
        jpath = os.path.join(directory_path, jname)
        jdata = read_json(jpath)

        cdata = json_to_csv(jdata)
        cname = converted_prefix + jname.rstrip(".json") + ".csv"
        cpath = os.path.join(directory_path, cname)
        with open(cpath, 'w') as f:
            f.write(cdata)
    return

dirpath = "./02_file_handling_and_dataframes/02_challenge/"
process_directory(dirpath)

#----------------------------------------------------------------------------------------
# スクリプトを実行するmain関数
def main():
    # 使用例
    # try:
    #     directory = "path_to_directory"
    #     process_directory(directory)
    # except Exception as e:
    #     print("An error occurred:", e)
    pass

if __name__ == "__main__":
    main()