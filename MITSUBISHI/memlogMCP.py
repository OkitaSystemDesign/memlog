# PLC Memory Log (MCProtocol udp)
#

import time
from datetime import datetime

# https://github.com/OkitaSystemDesign/MC-Protocol
import mcp

# シーケンサのIPアドレスとポート
host = '192.168.0.41'
port = 4999

# モニタ登録
# False: 連続アドレスで読み出す場合
# True: モニタ登録して読み出す場合
monitor = False

# 連続アドレスで読み出すデバイスアドレス
deviceAddress = 'D0'
readSize = 20
# モニタ登録して読み出すデバイスアドレス
monitorWORDdevice = 'M0,M16,D0,D10,D12'             # ワード読出し
monitorDWORDdevice = 'D100,D102,D105,D110,D120,D122,D130,D132'   # ダブルワード読出し

### memlogMCP ###
# interval: 収集周期
# recnum: 収集個数
# logpath: 収集ファイル出力ディレクトリ
def memlogMCP(interval, recnum, logpath):
    BaseTime = time.perf_counter()
    RecCnt = 0

    now = datetime.now()
    prevET = 0
    filename = logpath + '/log' + now.strftime('%Y%m%d_%H%M') + '.csv'

    if monitor:
        plc = mcp.MCProtcol3E(host, port)
        res = plc.MonitorSet(monitorWORDdevice, monitorDWORDdevice)

    try:
        while True:
            logwrite(filename)

            now = time.perf_counter()
            ET = now - BaseTime
            if interval > (ET - prevET):
                rem = ET % interval
                time.sleep(interval - rem)
            
            prevET = ET

            if recnum > 0:
                RecCnt += 1
                if RecCnt >= recnum:
                    break

    except KeyboardInterrupt:
        print()


def logwrite(filename):
    plc = mcp.MCProtcol3E(host, port)

    with open(filename,'a') as f:

        # データ読出し
        if monitor == False:
            data = plc.read(deviceAddress, readSize)           # 読み出すデバイスのアドレスとワード数
        else:
            data = plc.MonitorGet()

        # 日時
        now = datetime.now()
        f.write(now.strftime('%Y/%m/%d %H:%M:%S.') + "%03d" % (now.microsecond // 1000) + ',')

        # ---- 以下 読み出したバイト列をデータ型に合わせて変換しながらファイル出力 ----
        # 16ビット*2
        dataWordToBin = plc.WordToBin(data[:4])
        f.write(','.join(list(dataWordToBin.rjust(32,"0"))) + ',')
        
        # INT16
        data16 = plc.toInt16(data[4:8])
        datastr = [str(n) for n  in data16]
        f.write(','.join(datastr) + ',')

        # UINT16
        data16 = plc.toUInt16(data[8:10])
        datastr = [str(n) for n  in data16]
        f.write(','.join(datastr) + ',')

        # INT32
        data32 = plc.toInt32(data[10:18])
        datastr = [str(n) for n  in data32]
        f.write(','.join(datastr) + ',')
        
        # UINT32
        data32 = plc.toUInt32(data[18:22])
        datastr = [str(n) for n  in data32]
        f.write(','.join(datastr) + ',')

        # FLOAT
        dataFloat = plc.toFloat(data[22:26])
        datastr = [str(n) for n  in dataFloat]
        f.write(','.join(datastr) + ',')

        # DOUBLE
        dataDouble = plc.toDouble(data[26:34])
        datastr = [str(n) for n  in dataDouble]
        f.write(','.join(datastr) + ',')

        # STRING
        dataStr = plc.toString(data[34:40])
        f.write(dataStr + '\n')

if __name__ == "__main__":
    memlogMCP(0.1, 100, 'log')
