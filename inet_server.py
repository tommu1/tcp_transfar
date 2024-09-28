# このプログラムは、ネットワーク経由でファイルを受信するサーバーを実装しています。

# 主な機能：
# 1. ソケットを作成し、指定されたアドレスとポートでlistenします。
# 2. クライアントからの接続を受け付けます。
# 3. クライアントから送信されたヘッダー情報を解析します。
# 4. ファイル名を受信し、デコードします。
# 5. ファイルデータを受信し、指定されたディレクトリに保存します。

# 詳細説明：
# - サーバーは0.0.0.0（すべてのネットワークインターフェース）の9001ポートでリッスンします。
# - 受信したファイルは'temp'ディレクトリに保存されます（ディレクトリが存在しない場合は作成されます）。
# - ヘッダーには、ファイル名の長さ、JSONデータの長さ（現在は使用されていません）、ファイルデータの長さが含まれています。
# - 各接続ごとに、ファイルの受信処理が行われます。
# - 受信したデータは4096バイトずつ書き込まれます。


import socket
import os
from pathlib import Path

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '0.0.0.0'
server_port = 9001

dpath = 'temp'
if not os.path.exists(dpath):
    os.makedirs(dpath)


print('Starint up on {} port {} '.format(server_address, server_port))

sock.bind((server_address, server_port))

sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        header = connection.recv(8)

        filename_length = int.from_bytes(header[:1], "big")
        json_length = int.from_bytes(header[1:3], "big")
        data_length = int.from_bytes(header[4:8], "big")

        stream_rate = 4096

        print('Recive header from client. Byte length: Title length {}, JSON length {}, data length {}'.format(filename_length, json_length, data_length))

        filename = connection.recv(filename_length).decode('utf-8')

        print('FIlename: {}'.format(filename))

        if json_length != 0:
            raise Exception('JSON dta is not currently supported.')
        
        if data_length == 0:
            raise Exception('No data toread from client.')
        
        with open(os.path.join(dpath, filename), 'wb+') as f:
            while data_length > 0:
                data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                f.write(data)

                print('recieved {} bytes'.format(len(data)))
                data_length -= len(data)

        print('recieved {} bytes in total'.format(data_length))

    except Exception as e:
        print('Error: ' + str(e))

    finally:
        print("Closing current connection.")
        connection.close()