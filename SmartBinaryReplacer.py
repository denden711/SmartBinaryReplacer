import os
import re
import tkinter as tk
from tkinter import filedialog

# プログラム名: SmartBinaryReplacer

# GUIを使用してディレクトリパスを選択
root = tk.Tk()
root.withdraw()
directory_path = filedialog.askdirectory(title="ディレクトリを選択")

if not directory_path:
    print("ディレクトリが選択されませんでした。プログラムを終了します。")
    exit()

# 元ファイルのパスとold_valueを変数として定義
files_info = {
    'one_digit': {
        'path': os.path.join(directory_path, 'x=0.pl3'),
        'old_value': b'x=0.txp'
    },
    'two_digit': {
        'path': os.path.join(directory_path, 'x=10.pl3'),
        'old_value': b'x=10.txp'
    },
    'decimal_one_digit': {
        'path': os.path.join(directory_path, 'x=0.5.pl3'),
        'old_value': b'x=0.5.txp'
    },
    'decimal_two_digit': {
        'path': os.path.join(directory_path, 'x=10.5.pl3'),
        'old_value': b'x=10.5.txp'
    }
}

# ファイルの読み込み関数
def read_file_content(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"ファイルが見つかりません: {file_path}")
            return None
        else:
            with open(file_path, 'rb') as file:
                content = file.read()
                print(f"元ファイルの内容を読み込みました: {file_path}")
                return content
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")
        return None

# 各元ファイルの内容を読み込む
file_contents = {}
for key, info in files_info.items():
    content = read_file_content(info['path'])
    if content is not None:
        file_contents[key] = content

# ディレクトリ内のすべてのファイルをリスト表示
all_files = os.listdir(directory_path)
print("ディレクトリ内のファイル一覧:", all_files)

# ファイル名から一桁、二桁、小数点を含む一桁、二桁の数字を抽出し、対応する値に置き換える
for filename in all_files:
    if filename in [os.path.basename(info['path']) for info in files_info.values()]:
        print(f"元ファイルをスキップしました: {filename}")
        continue

    try:
        match_one_digit = re.match(r'x=(\d)\.pl3', filename)  # 一桁の数字にマッチ
        match_two_digit = re.match(r'x=(\d{2})\.pl3', filename)  # 二桁の数字にマッチ
        match_decimal_one_digit = re.match(r'x=(\d\.\d)\.pl3', filename)  # 小数点を含む一桁の数字にマッチ
        match_decimal_two_digit = re.match(r'x=(\d{2}\.\d)\.pl3', filename)  # 小数点を含む二桁の数字にマッチ

        if match_one_digit and 'one_digit' in file_contents:
            number = match_one_digit.group(1)
            print(f"ファイル名から抽出した一桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['one_digit']['old_value']
            new_value = f'x={number}.txp'.encode()

            # 'x=0.txp' を 'x=一桁の数字.txp' に置き換える
            new_content = file_contents['one_digit'].replace(old_value, new_value)
            print(f"置き換え完了: {old_value} -> {new_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            print(f"新しいファイルを作成しました: {new_file_path}")

        elif match_two_digit and 'two_digit' in file_contents:
            number = match_two_digit.group(1)
            print(f"ファイル名から抽出した二桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['two_digit']['old_value']
            new_value = f'x={number}.txp'.encode()

            # 'x=10.txp' を 'x=二桁の数字.txp' に置き換える
            new_content = file_contents['two_digit'].replace(old_value, new_value)
            print(f"置き換え完了: {old_value} -> {new_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            print(f"新しいファイルを作成しました: {new_file_path}")

        elif match_decimal_one_digit and 'decimal_one_digit' in file_contents:
            number = match_decimal_one_digit.group(1)
            print(f"ファイル名から抽出した小数点を含む一桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['decimal_one_digit']['old_value']
            new_value = f'x={number}.txp'.encode()

            # 'x=0.5.txp' を 'x=小数点を含む一桁の数字.txp' に置き換える
            new_content = file_contents['decimal_one_digit'].replace(old_value, new_value)
            print(f"置き換え完了: {old_value} -> {new_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            print(f"新しいファイルを作成しました: {new_file_path}")

        elif match_decimal_two_digit and 'decimal_two_digit' in file_contents:
            number = match_decimal_two_digit.group(1)
            print(f"ファイル名から抽出した小数点を含む二桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['decimal_two_digit']['old_value']
            new_value = f'x={number}.txp'.encode()

            # 'x=10.5.txp' を 'x=小数点を含む二桁の数字.txp' に置き換える
            new_content = file_contents['decimal_two_digit'].replace(old_value, new_value)
            print(f"置き換え完了: {old_value} -> {new_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            print(f"新しいファイルを作成しました: {new_file_path}")

        else:
            print(f"数字を含まないファイル、または条件に合わないファイルをスキップしました: {filename}")
    except Exception as e:
        print(f"ファイル処理中にエラーが発生しました: {filename} - {str(e)}")
