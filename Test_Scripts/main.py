from googleapiclient import sample_tools
from googleapiclient.http import build_http
import sys
import simplejson as json
import pandas as pd
import csv
from pandas.io.json import json_normalize
from datetime import datetime, timedelta
import pyLINQ
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import httplib2

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', ['https://www.googleapis.com'
                                                                                       '/auth/analytics.readonly'])

http = credentials.authorize(httplib2.Http())
service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com'
                                                                   '/$discovery/rest'))

discovery_doc = "gmb_discovery.json"

df = []

outfile = open("gmb_batchreviews.csv", "w", newline='')
writer = csv.writer(outfile)


def main(argv):
    # Use the discovery doc to build a service that we can use to make
    # MyBusiness API calls, and authenticate the user so we can access their
    # account
    service, flags = sample_tools.init(argv, "mybusiness", "v4", __doc__, __file__,
                                       scope="https://www.googleapis.com/auth/business.manage",
                                       discovery_filename=discovery_doc)

    # Get the list of accounts the authenticated user has access to
    output = service.accounts().list().execute()
    print("List of Accounts:\n")
    print(json.dumps(output, indent=2) + "\n")

    firstAccount = output["accounts"][0]["name"]

    # Get the list of locations for the first account in the list
    print("List of Locations for Account " + firstAccount)
    body = {
        "locationNames": [
            "accounts/XXXXXX/locations/XXXXX",
            "accounts/XXXXXX/locations/XXXXX"
        ]
    }
    locationsList = service.accounts().locations().batchGetReviews(name=firstAccount, body=body).execute()
    print(json.dumps(locationsList, indent=2))
    with open('gmb_batchreviews.json', 'w') as json_file:
        json.dump(locationsList, json_file)
    # load json object
    with open('gmb_batchreviews.json') as f:
        d = json.load(f)
    # Normalize the nested json file
    df = json_normalize(d['locationReviews'])
    df.to_csv('gmb_batchreviews.csv')
    outfile.close()


if __name__ == "__main__":
    main(sys.argv)

# filter results by time
df2 = pd.read_csv('gmb_batchreviews.csv')
df2 = df2.drop(['Unnamed: 0'], axis=1)
df2['review.createTime'] = pd.to_datetime(df2['review.createTime'])
df2 = df2.set_index(['review.createTime'])
end_range = datetime.now().date()
d = d = datetime.today() - timedelta(days=30)
start_range = d.date()
df3 = df2[end_range:start_range]
# df3 = df2[end_range:'2019-05-01']

# clean dataframe
df3 = df3.drop(columns=['review.name', 'review.reviewId', 'review.reviewer.profilePhotoUrl'])
df3.columns = ['location', 'comment', 'reply', 'reply_date', 'reviewer', 'star_rating', 'date']
export_name = 'gmb_reviews_export_' + str(end_range) + '.xlsx'
df3.to_excel(export_name, index=False)