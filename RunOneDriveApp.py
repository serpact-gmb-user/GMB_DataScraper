import os.path
import pathlib
import time
from datetime import datetime, timedelta, date
from dateutil.parser import parse
import maya

"""
def main(one_drive_path):
    os.startfile(one_drive_path)


if __name__ == "__main__":
    main(r'C:\Program Files (x86)\Microsoft OneDrive\OneDrive.exe')
"""


# Extract date time of a specified file in a folder/path
def main():
    fileName = pathlib.Path(
        r'C:\Users\ststoyan\Documents\UiPath\ARIBA_CIG_TRANSACTION_MONITORING\SAPAribaProject\Data\Config.xlsx')
    file_lastModified = time.ctime(os.path.getmtime(fileName))
    date_last_modified = file_lastModified[4:-5]
    dt = maya.parse(date_last_modified).datetime()
    list_date = [str(dt.date().strftime('%d-%m-%Y')), str(dt.time())]
    result_date = ' '.join(list_date)
    # print(result_date)
    current_date_time = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    est_date = date.today() - timedelta(days=90)
    print(est_date)
    # print(current_date_time[:10])


if __name__ == "__main__":
    main()
