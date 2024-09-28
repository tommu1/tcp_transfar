# このプログラムは、ネットワーク経由でファイルを送信するクライアントを実装しています。

# 主な機能：
# 1. ソケットを作成し、指定されたサーバーのアドレスとポートに接続します。
# 2. ファイルを読み込み、ヘッダーを送信します。
# 3. ファイル名を送信します。
# 4. ファイルデータを送信します。

# 詳細説明：
# - ユーザーにサーバーのアドレスとアップロードするファイルのパスを入力してもらいます。
# - サーバーのポートは9001に固定されています。
# - ファイルサイズが2GB未満であることを確認します。
# - ヘッダーには、ファイル名の長さ、JSONデータの長さ（現在は使用されていません）、ファイルデータの長さが含まれています。
# - ファイルは4096バイトずつ読み込まれ、サーバーに送信されます。
# - 送信中は進捗状況を表示します。

# サンプル引数：
# python inet_client.py localhost /path/to/file.txt
# localhost: サーバーのIPアドレス
# /path/to/file.txt: アップロードするファイルのパス

import socket
import sys
import os

def protocol_header(filename_length, json_length, data_length):
    return filename_length.to_bytes(1, 'big') + json_length.to_bytes(3, 'big') + data_length.to_bytes(4, 'big')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = input("Type in the server's address to connect to:  ")
server_port = 9001

print('Connecting to {}'.format(server_address, server_port))

try:
    sock.connect((server_address, server_port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    filepath = input("Type in a file to upload: ")
    
    with open(filepath, 'rb') as f:
        f.seek(0, os.SEEK_END)
        filesize = f.tell()
        f.seek(0,0)

        if filesize > pow(2,32):
            raise Exception('File must be below 2GB')
        
        filename = os.path.basename(f.name)

        filename_bits = filename.encode('utf-8')

        header = protocol_header(len(filename_bits), 0, filesize)

        sock.send(header)

        sock.send(filename_bits)

        data = f.read(4096)

        while data:
            print("Sending...")
            sock.send(data)
            data = f.read(4096)

finally:
    print("Closing socket.")
    sock.close()