# PLC Memory Log (MCProtocol udp)
#

import time
from datetime import datetime

# https://github.com/OkitaSystemDesign/MC-Protocol
import mcp

# シーケンサのIPアドレスとポート
host = '192.168.0.41'
port = 4999

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
        data = plc.read('D0', 20)           # 読み出すデバイスのアドレスとワード数

        # 日時
        now = datetime.now()
        f.write(now.strftime('%Y/%m/%d %H:%M:%S.') + "%03d" % (now.microsecond // 1000) + ',')

        # 16ビット*2 (D0-1)
        dataWordToBin = plc.WordToBin(data[:4])
        f.write(','.join(list(dataWordToBin.rjust(32,"0"))) + ',')
        
        # INT16 (D2,D3)
        data16 = plc.toInt16(data[4:8])
        datastr = [str(n) for n  in data16]
        f.write(','.join(datastr) + ',')

        # UINT16 (D4)
        data16 = plc.toUInt16(data[8:10])
        datastr = [str(n) for n  in data16]
        f.write(','.join(datastr) + ',')

        # INT32 (D5,D7)
        data32 = plc.toInt32(data[10:18])
        datastr = [str(n) for n  in data32]
        f.write(','.join(datastr) + ',')
        
        # UINT32 (D9)
        data32 = plc.toUInt32(data[18:22])
        datastr = [str(n) for n  in data32]
        f.write(','.join(datastr) + ',')

        # FLOAT (D11)
        dataFloat = plc.toFloat(data[22:26])
        datastr = [str(n) for n  in dataFloat]
        f.write(','.join(datastr) + ',')

        # DOUBLE (D13)
        dataDouble = plc.toDouble(data[26:34])
        datastr = [str(n) for n  in dataDouble]
        f.write(','.join(datastr) + ',')

        # STRING (D17)
        dataStr = plc.toString(data[34:40])
        f.write(dataStr + '\n')

if __name__ == "__main__":
    memlogMCP(0.1, 100, 'log')
