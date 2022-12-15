from asyncio.windows_events import NULL
import datetime
import time
import csv
import json
import os


class CSV:

    def __init__(self):
        self._f = NULL
        if os.path.exists('./output'):
            pass
        else:
            os.mkdir('./output')

    def MakeFile(self, Pressure, DeltaTime) -> str:
        self._startTime = time.time()
        filename = './output/log_' + \
            datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + \
            '_dt' + str(DeltaTime) + '_p' + str(Pressure) + '.csv'
        with open(filename, 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['DataTime', 'DeltaTime', 'Pressure',
                            'LowFlowRate', 'HighFlowRate', 'DangomushiposX', 'DangomushiposY', 'NozleDangomushiDistance'])
        self._f = open(filename, 'a', encoding="utf-8", newline='')
        self._writer = csv.writer(self._f)
        return filename

    def IsFileOpened(self) -> bool:
        if self._f.closed:
            return False
        else:
            return True

    def CloseFile(self):
        if self._f != NULL:
            self._f.close()

    def AddRow(self, data: dict, DangomushiposX, DangomushiposY, NozleDangomushiDistance):
        self._writer.writerow(
            [time.time() - self._startTime, data['d'], 0, data['LF'], data['HF'], DangomushiposX, DangomushiposY, NozleDangomushiDistance])

    def editCSV(self):
        pass

    def decode(self):
        pass

    def __del__(self):
        if self._f != NULL:
            self._f.close()
