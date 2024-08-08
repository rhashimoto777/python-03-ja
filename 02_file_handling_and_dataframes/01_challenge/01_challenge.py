import os
import shutil
from pathlib import Path

def f01_file_operation():
    """
    ファイルの操作: 
        最初のスクリプトでは、書籍の名前が付いたすべてのファイルをPythonの辞書にインポートし、
        それを1つのテキストファイルに保存します。Chapter_x.txt という名前のファイルは含めないようにしてください。
    """
    current_path = Path(__file__).resolve().parent
    filedir = os.path.join(current_path, 'data', 'text_files')

    # 書籍の名前が付いたすべてのファイルをPythonの辞書にインポートし...
    book_dict = {}
    for file in os.listdir(filedir):
        if ("Chapter_" in file) and (".txt" in file):
            # Chapter_x.txt という名前のファイルは含めない
            pass
        else:
            open_file_path = os.path.join(filedir, file)
            with open(open_file_path, 'r', encoding='utf-8') as f:
                book_dict[file] = f.read()

    # それを1つのテキストファイルに保存します
    out_file_path = os.path.join(current_path, "output_file.txt")
    with open(out_file_path, 'w', encoding='utf-8') as f:
        for title, content in book_dict.items():
            msg = f'{title}\n"-------"\n{content}\n\n\n'
            f.write(msg)


def f02_directory_operation():
    """
    ディレクトリの設定: 
        data フォルダー内にディレクトリ library を新規作成するスクリプトを作成します。
        data フォルダーに含まれる10個の Chapter_x.txt ファイルをすべてこのディレクトリに保存します。
        その後、pathlib を使用してこのディレクトリに移動し、すべてのファイルとサイズを一覧表示します。
    """
    # data フォルダー内にディレクトリ library を新規作成するスクリプトを作成します。
    current_path = Path(__file__).resolve().parent
    data_dir = os.path.join(current_path, 'data')
    library_dir = os.path.join(data_dir, "library")
    if os.path.exists(library_dir):
        # 「ディレクトリ libraryを新規生成する」が指示であるため、既に存在する場合は一旦削除する。
        shutil.rmtree(library_dir)
        print(f'既にフォルダが存在するため、一旦フォルダを削除します')
    os.mkdir(library_dir)

    # data フォルダーに含まれる10個の Chapter_x.txt ファイルをすべてこのディレクトリに保存します。
    path = Path(data_dir)
    for org_file_path in path.rglob('Chapter_*.txt'): 
        # rglobの引数は正規表現ではない。*は任意の文字"列"を表す。そのため例えばChapter_ABC.txtなども抽出可能。
        tar_file_path = os.path.join(library_dir, org_file_path.name)
        # ファイルコピー処理
        shutil.copyfile(org_file_path, tar_file_path)
    
    # その後、pathlib を使用してこのディレクトリに移動し、すべてのファイルとサイズを一覧表示します。
    p = Path(library_dir)
    for path in p.iterdir():
        size = path.stat().st_size
        print(f'{path}\n{size} bytes')

# f01_file_operation()
f02_directory_operation()