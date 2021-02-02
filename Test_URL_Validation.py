import re
import csv

GMB_Business_Accounts = 'GMB_Account_Data.csv'
regex = re.compile(r'^(?:http|ftp)s?://'  
                   r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                   r'localhost|'
                   r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                   r'(?::\d+)?'
                   r'(?:/?|[/?]\S+)$', re.IGNORECASE)

csv_reader = csv.reader(open(GMB_Business_Accounts))
csv_dict = {}
for row in csv_reader:
    key = row[0]
    if key in csv_dict:
        pass
    csv_dict[key] = row[1:]
    # Skipping .csv GMB Accounts header row.
    if row[1] == 'GMB Accounts':
        continue
    if re.match(regex, row[1]) is None:
        print(re.match(regex, row[1]) is None)
        raise Exception
    else:
        print(re.match(regex, row[1]) is not None)
        continue
    # print(re.match(regex, row[1]) is not None)
