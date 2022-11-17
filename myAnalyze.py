import datetime
import csv
import json


class Analyze:

    def __init__(self):
        self._now = datetime.datetime.now()
        self._filename = './output/log_' + \
            self._now.strftime('%Y%m%d_%H%M%S') + '.csv'

    def writeRowToCSV(self, data: dict):
        pass

    def decode(self):
        pass
