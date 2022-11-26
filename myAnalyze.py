import datetime
import time
import csv
import json
import os


class Analyze:

    def __init__(self):
        self._startTime = time.time()
        self._filename = './output/log_' + \
            datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
        if os.path.exists('./output'):
            pass
        else:
            os.mkdir('./output')
        with open(self._filename, 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['DataTime', 'DeltaTime', 'Pressure',
                            'FlowRate'])
        self._f = open(self._filename, 'a', encoding="utf-8", newline='')
        self._writer = csv.writer(self._f)

    def writeRowToCSV(self, data: dict):
        self._writer.writerow(
            [time.time() - self._startTime, data['d'], 0, data['F']])

    def editCSV(self):
        pass

    def decode(self):
        pass

    def __del__(self):
        self._f.close()
