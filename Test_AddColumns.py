from __future__ import print_function

import math
import os
import csv
import psutil
from guppy import hpy

with open('GMB_End_Keyword_SearchTimes.csv', 'r', newline='') as csv_file:
    r = csv.reader(csv_file)
    data = [line for line in r]

with open('GMB_End_Keyword_SearchTimes.csv', 'w', newline='') as csv_file:
    w = csv.writer(csv_file)
    w.writerow(['Keywords', 'Values', 'Location', 'Location group', 'URL'])
    w.writerows(data)

# print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
psutil.virtual_memory()
dict(psutil.virtual_memory()._asdict())
print(psutil.virtual_memory().percent)
print(round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total, 1))
print(psutil.Process().memory_info().peak_wset)
h = hpy()
print(h.heap())
# print(math.ceil(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))

# print("Memory % used: ", psutil.virtual_memory()[2])
# print("CPU % used: ", psutil.cpu_percent())
# print(psutil.virtual_memory())