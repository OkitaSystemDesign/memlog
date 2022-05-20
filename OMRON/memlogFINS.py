# PLC Memory Log (Fins udp)
#

import time
from datetime import datetime

# https://github.com/OkitaSystemDesign/FinsCommand
import finsudp

# シーケンサのIPアドレスとFINSアドレス（送信元と送信先）
host = '192.168.0.21'
srcFinsAdr = '0.21.0'
dstFinsAdr = '0.10.0'

### memlogFINS ###
# interval: 収集周期
# recnum: 収集個数
# logpath: 収集ファイル出力ディレクトリ
def memlogFINS(interval, recnum, logpath):
    BaseTime = time.perf_counter()
    RecCnt = 0

    now = datetime.now()
    filename = logpath + '/log' + now.strftime('%Y%m%d_%H%M') + '.csv'

    try:
        while True:
            logwrite(filename)

            now = time.perf_counter()
            ET = now - BaseTime
            rem = ET % interval
            time.sleep(interval - rem)

            if recnum > 0:
                RecCnt += 1
                if RecCnt >= recnum:
                    break

    except KeyboardInterrupt:
        print()


def logwrite(filename):
    plc = finsudp.fins(host, srcFinsAdr, dstFinsAdr)

    with open(filename,'a') as f:

        # データ読出し
        data = plc.read('D1000', 20)        # 読み出すメモリのアドレスとワード数

        # 日時
        now = datetime.now()
        f.write(now.strftime('%Y/%m/%d %H:%M:%S.') + "%03d" % (now.microsecond // 1000) + ',')

        # 32ビット
        f.write(','.join(list(plc.toBin(data[:4]).rjust(16,"0"))) + ',')
        
        # INT16 * 2
        data16 = plc.toInt16(data[4:8])
        datastr = [str(n) for n  in data16]
        f.write(','.join(datastr) + ',')

        # UINT16
        data32 = plc.toUInt16(data[8:10])
        datastr = [str(n) for n  in data32]
        f.write(','.join(datastr) + ',')
        
        # INT32 * 2
        data64 = plc.toInt32(data[10:18])
        datastr = [str(n) for n  in data64]
        f.write(','.join(datastr) + ',')

        # UINT32
        dataU16 = plc.toUInt32(data[18:22])
        datastr = [str(n) for n  in dataU16]
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
        datastr = plc.toString(data[34:40])
        f.write(datastr + '\n')



if __name__ == "__main__":
    memlogFINS(0.1, 100, 'log')
