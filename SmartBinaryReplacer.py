import os
import re
import tkinter as tk
from tkinter import filedialog
import logging

# プログラム名: SmartBinaryReplacer

# ロギングの設定
log_handler = logging.FileHandler('smart_binary_replacer.log', encoding='utf-8')
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

# GUIを使用してディレクトリパスを選択
root = tk.Tk()
root.withdraw()
directory_path = filedialog.askdirectory(title="ディレクトリを選択")

if not directory_path:
    logger.error("ディレクトリが選択されませんでした。プログラムを終了します。")
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
    'three_digit': {
        'path': os.path.join(directory_path, 'x=100.pl3'),
        'old_value': b'x=100.txp'
    },
    'decimal_one_digit': {
        'path': os.path.join(directory_path, 'x=0.5.pl3'),
        'old_value': b'x=0.5.txp'
    },
    'decimal_two_digit': {
        'path': os.path.join(directory_path, 'x=10.5.pl3'),
        'old_value': b'x=10.5.txp'
    },
    'decimal_three_digit': {
        'path': os.path.join(directory_path, 'x=100.5.pl3'),
        'old_value': b'x=100.5.txp'
    }
}

# ファイルの読み込み関数
def read_file_content(file_path):
    try:
        if not os.path.exists(file_path):
            logger.warning(f"ファイルが見つかりません: {file_path}")
            return None
        with open(file_path, 'rb') as file:
            content = file.read()
            logger.info(f"元ファイルの内容を読み込みました: {file_path}")
            return content
    except FileNotFoundError:
        logger.error(f"ファイルが見つかりません: {file_path}")
    except PermissionError:
        logger.error(f"ファイルの読み込み許可がありません: {file_path}")
    except Exception as e:
        logger.error(f"ファイルの読み込み中にエラーが発生しました: {file_path} - {str(e)}")
    return None

# 各元ファイルの内容を読み込む
file_contents = {}
for key, info in files_info.items():
    content = read_file_content(info['path'])
    if content is not None:
        file_contents[key] = content

# ディレクトリ内のすべてのファイルをリスト表示
try:
    all_files = os.listdir(directory_path)
    logger.info(f"ディレクトリ内のファイル一覧を取得しました: {all_files}")
except FileNotFoundError:
    logger.error("ディレクトリが見つかりませんでした。")
    print("ディレクトリが見つかりませんでした。プログラムを終了します。")
    exit()
except PermissionError:
    logger.error("ディレクトリの読み取り許可がありません。")
    print("ディレクトリの読み取り許可がありません。プログラムを終了します。")
    exit()
except Exception as e:
    logger.error(f"ディレクトリ内のファイル一覧を取得中にエラーが発生しました: {str(e)}")
    print("ディレクトリ内のファイル一覧を取得中にエラーが発生しました。プログラムを終了します。")
    exit()

# ファイル名から一桁、二桁、三桁、小数点を含む一桁、二桁、三桁の数字を抽出し、対応する値に置き換える
for filename in all_files:
    if filename in [os.path.basename(info['path']) for info in files_info.values()]:
        logger.info(f"元ファイルをスキップしました: {filename}")
        continue

    try:
        match_one_digit = re.match(r'x=(\d)\.pl3', filename)  # 一桁の数字にマッチ
        match_two_digit = re.match(r'x=(\d{2})\.pl3', filename)  # 二桁の数字にマッチ
        match_three_digit = re.match(r'x=(\d{3})\.pl3', filename)  # 三桁の数字にマッチ
        match_decimal_one_digit = re.match(r'x=(\d\.\d)\.pl3', filename)  # 小数点を含む一桁の数字にマッチ
        match_decimal_two_digit = re.match(r'x=(\d{2}\.\d)\.pl3', filename)  # 小数点を含む二桁の数字にマッチ
        match_decimal_three_digit = re.match(r'x=(\d{3}\.\d)\.pl3', filename)  # 小数点を含む三桁の数字にマッチ

        if match_one_digit and 'one_digit' in file_contents:
            number = match_one_digit.group(1)
            logger.info(f"ファイル名から抽出した一桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['one_digit']['old_value']
            new_value = f'x={number}.txp'.encode()
            new_binary_value = f'%Ix@%N%F = {number} mm'.encode()

            # 'x=0.txp' を 'x=一桁の数字.txp' に置き換える
            new_content = file_contents['one_digit'].replace(old_value, new_value)
            # バイナリデータ内の文字列を置換
            new_content = new_content.replace(b'%Ix@%N%F = 0 mm', new_binary_value)
            logger.info(f"置き換え完了: {old_value} -> {new_value}, %Ix@%N%F = 0 mm -> {new_binary_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            logger.info(f"新しいファイルを作成しました: {new_file_path}")

        elif match_two_digit and 'two_digit' in file_contents:
            number = match_two_digit.group(1)
            logger.info(f"ファイル名から抽出した二桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['two_digit']['old_value']
            new_value = f'x={number}.txp'.encode()
            new_binary_value = f'%Ix@%N%F = {number} mm'.encode()

            # 'x=10.txp' を 'x=二桁の数字.txp' に置き換える
            new_content = file_contents['two_digit'].replace(old_value, new_value)
            # バイナリデータ内の文字列を置換
            new_content = new_content.replace(b'%Ix@%N%F = 10 mm', new_binary_value)
            logger.info(f"置き換え完了: {old_value} -> {new_value}, %Ix@%N%F = 10 mm -> {new_binary_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            logger.info(f"新しいファイルを作成しました: {new_file_path}")

        elif match_three_digit and 'three_digit' in file_contents:
            number = match_three_digit.group(1)
            logger.info(f"ファイル名から抽出した三桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['three_digit']['old_value']
            new_value = f'x={number}.txp'.encode()
            new_binary_value = f'%Ix@%N%F = {number} mm'.encode()

            # 'x=100.txp' を 'x=三桁の数字.txp' に置き換える
            new_content = file_contents['three_digit'].replace(old_value, new_value)
            # バイナリデータ内の文字列を置換
            new_content = new_content.replace(b'%Ix@%N%F = 100 mm', new_binary_value)
            logger.info(f"置き換え完了: {old_value} -> {new_value}, %Ix@%N%F = 100 mm -> {new_binary_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            logger.info(f"新しいファイルを作成しました: {new_file_path}")

        elif match_decimal_one_digit and 'decimal_one_digit' in file_contents:
            number = match_decimal_one_digit.group(1)
            logger.info(f"ファイル名から抽出した小数点を含む一桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['decimal_one_digit']['old_value']
            new_value = f'x={number}.txp'.encode()
            new_binary_value = f'%Ix@%N%F = {number} mm'.encode()

            # 'x=0.5.txp' を 'x=小数点を含む一桁の数字.txp' に置き換える
            new_content = file_contents['decimal_one_digit'].replace(old_value, new_value)
            # バイナリデータ内の文字列を置換
            new_content = new_content.replace(b'%Ix@%N%F = 0.5 mm', new_binary_value)
            logger.info(f"置き換え完了: {old_value} -> {new_value}, %Ix@%N%F = 0.5 mm -> {new_binary_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            logger.info(f"新しいファイルを作成しました: {new_file_path}")

        elif match_decimal_two_digit and 'decimal_two_digit' in file_contents:
            number = match_decimal_two_digit.group(1)
            logger.info(f"ファイル名から抽出した小数点を含む二桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['decimal_two_digit']['old_value']
            new_value = f'x={number}.txp'.encode()
            new_binary_value = f'%Ix@%N%F = {number} mm'.encode()

            # 'x=10.5.txp' を 'x=小数点を含む二桁の数字.txp' に置き換える
            new_content = file_contents['decimal_two_digit'].replace(old_value, new_value)
            # バイナリデータ内の文字列を置換
            new_content = new_content.replace(b'%Ix@%N%F = 10.5 mm', new_binary_value)
            logger.info(f"置き換え完了: {old_value} -> {new_value}, %Ix@%N%F = 10.5 mm -> {new_binary_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            logger.info(f"新しいファイルを作成しました: {new_file_path}")

        elif match_decimal_three_digit and 'decimal_three_digit' in file_contents:
            number = match_decimal_three_digit.group(1)
            logger.info(f"ファイル名から抽出した小数点を含む三桁の数字: {number}")

            # 置き換える新しい値を作成
            old_value = files_info['decimal_three_digit']['old_value']
            new_value = f'x={number}.txp'.encode()
            new_binary_value = f'%Ix@%N%F = {number} mm'.encode()

            # 'x=100.5.txp' を 'x=小数点を含む三桁の数字.txp' に置き換える
            new_content = file_contents['decimal_three_digit'].replace(old_value, new_value)
            # バイナリデータ内の文字列を置換
            new_content = new_content.replace(b'%Ix@%N%F = 100.5 mm', new_binary_value)
            logger.info(f"置き換え完了: {old_value} -> {new_value}, %Ix@%N%F = 100.5 mm -> {new_binary_value}")

            # 変更後のデータを新しいファイルに書き込む
            new_file_path = os.path.join(directory_path, f'x={number}.pl3')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            logger.info(f"新しいファイルを作成しました: {new_file_path}")

        else:
            logger.info(f"数字を含まないファイル、または条件に合わないファイルをスキップしました: {filename}")
    except FileNotFoundError:
        logger.error(f"ファイルが見つかりません: {filename}")
    except PermissionError:
        logger.error(f"ファイルの処理許可がありません: {filename}")
    except Exception as e:
        logger.error(f"ファイル処理中にエラーが発生しました: {filename} - {str(e)}")

print("処理が完了しました。詳細はログファイル 'smart_binary_replacer.log' を確認してください。")
