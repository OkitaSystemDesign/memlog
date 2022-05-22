# PLC Memory Log (KV HostLink UDP)
#

import time
from datetime import datetime

# https://github.com/OkitaSystemDesign/kvHostLink
import kvhostlink

# PLCのIPアドレス
host = '192.168.0.31'

# モニタ登録
# False: 連続アドレスで読み出す場合
# True: モニタ登録して読み出す場合
monitor = False

# 連続アドレスで読み出すデバイスアドレス
deviceAddress = 'D0.H'
readSize = 20
# モニタ登録して読み出すデバイスアドレス
monitorAddresses = 'DM0.H DM1.S DM2.L DM4.U DM5.D'


### memlogKV ###
# interval: 収集周期
# recnum: 収集個数
# logpath: 収集ファイル出力ディレクトリ
def memlogKV(interval, recnum, logpath):
    BaseTime = time.perf_counter()
    ECnt = 0

    now = datetime.now()
    filename = logpath + '/log' + now.strftime('%Y%m%d_%H%M') + '.csv'

    if monitor:
        plc = kvhostlink.kvHostLink(host)
        res = plc.mws(monitorAddresses)

    try:
        while True:
            logwrite(filename)

            now = time.perf_counter()
            ET = now - BaseTime
            rem = ET % interval
            time.sleep(interval - rem)

            if recnum > 0:
                ECnt += 1
                if ECnt >= recnum:
                    break

    except KeyboardInterrupt:
        print()


def logwrite(filename):
    plc = kvhostlink.kvHostLink(host)

    with open(filename,'a') as f:

        # データ読出し
        if monitor == False:
            data = plc.reads(deviceAddress, readSize)
        else:
            data = plc.mwr()

        datastr = data.decode().replace('\r\n', '')
        datas = datastr.split(" ")

        # 日時
        now = datetime.now()
        f.write(now.strftime('%Y/%m/%d %H:%M:%S.') + "%03d" % (now.microsecond // 1000) + ',')

        # 1つ目の文字列を16ビットに変換して出力
        dataB = bin(int(datas[0],16))[2:].zfill(16)
        f.write(','.join(list(dataB)) + ',')
        
        # 残りはそのままカンマ(,)でつなぐ
        f.write(','.join(datas[1:]) + '\n')



if __name__ == "__main__":
    memlogKV(0.1, 100, 'log')
