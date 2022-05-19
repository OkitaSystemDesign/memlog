# 三菱のMCプロトコルでデバイスの値をロギング

## 環境
Python3.9  
Frame3E UDP/IP connection

## ファンクション
### memlogMCP(interval, recnum, logpath)
定周期でlogwriteを実行します

#### interval : 収集周期
収集する周期を入力します 単位は秒  
例：0.1

#### recnum : 収集個数
設定した個数を収集するとプログラムを終了してファイルを閉じます

#### logpath : 収集ファイル出力ディレクトリ
ロギングするファイルの出力先です
ここで指定したディレクトリの下にファイル名は"logYYYYMMDD_HHSS.csv"で出力します

### logwrite(filename)
デバイスの値を読み出してcsvファイルに出力します

#### filename
出力先のファイル名

## 収集するデバイスの設定方法
読み出すデバイスのアドレスはlogwrite()のここを変更します
```
data = plc.read('D0', 20)           # 読み出すデバイスのアドレスとワード数
```
読み出したデータはバイト配列になっているのでデータ型を変換してファイルに書き出していきます

