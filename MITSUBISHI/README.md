# 三菱のMCプロトコルでデバイスの値をロギング

## 環境
Python3.9  
Frame3E UDP/IP connection

## 実行例
```
memlogMCP(0.1, 100, 'log')
```
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
### まずシーケンサのD0から20ワードにロギングするデータを下表のように揃えてあると想定します

| D0,1 | 2 | 3 | 4 | 5,6 | 7,8 | 9,10 | 11,12 | 13.14,15,16 | 17,18,19 |  
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| BitData | INT16 | INT16 | UINT16 | INT32 | INT32 | UINT32 | FLOAT | DOUBLE | STRING |


### 読み出すデバイスのアドレスはlogwrite()のここで指定します
```
data = plc.read('D0', 20)           # 読み出すデバイスのアドレスとワード数
```

### 次に書き込むデータを順番に作っていきます  
最初の列には読み出した日付時刻
```
now = datetime.now()
f.write(now.strftime('%Y/%m/%d %H:%M:%S.') + "%03d" % (now.microsecond // 1000) + ',')
```

次はビットデータ32ビット (0-3 byte目)
```
dataWordToBin = plc.WordToBin(data[:4])
f.write(','.join(list(dataWordToBin.rjust(32,"0"))) + ',')
```

次はINT16データ2個 (4-7 byte目)
```
data16 = plc.toInt16(data[4:8])
datastr = [str(n) for n  in data16]
f.write(','.join(datastr) + ',')
```

次はUINT16データ1個 (8-9 byte目)
```
data16 = plc.toUInt16(data[8:10])
datastr = [str(n) for n  in data16]
f.write(','.join(datastr) + ',')
```

次はINT32データ2個(10-18 byte目)
```
data32 = plc.toInt32(data[10:18])
datastr = [str(n) for n  in data32]
f.write(','.join(datastr) + ',')
```

次はUINT32データ1個 (18-21 byte目)        
```
data32 = plc.toUInt32(data[18:22])
datastr = [str(n) for n  in data32]
f.write(','.join(datastr) + ',')
```

次は単精度浮動小数点1個 (22-25 byte目)
```
dataFloat = plc.toFloat(data[22:26])
datastr = [str(n) for n  in dataFloat]
f.write(','.join(datastr) + ',')
```

次は倍精度浮動小数点1個 (26-33 byte目)
```
dataDouble = plc.toDouble(data[26:34])
datastr = [str(n) for n  in dataDouble]
f.write(','.join(datastr) + ',')
```

最後に文字列6文字 (34-39 byte目)
```
dataStr = plc.toString(data[34:40])
f.write(dataStr + '\n')  
```
最後には'\n'で改行を入れます

### 出力データ例
```
2022/05/20 17:05:07.803,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,-1,3,4,-5,7,268435455,0.10999999940395355,-0.13,ABCD12
2022/05/20 17:05:07.902,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,-1,3,4,-5,7,268435455,0.10999999940395355,-0.13,ABCD12
2022/05/20 17:05:08.004,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,-1,3,4,-5,7,268435455,0.10999999940395355,-0.13,ABCD12
2022/05/20 17:05:08.012,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,-1,3,4,-5,7,268435455,0.10999999940395355,-0.13,ABCD12
```
