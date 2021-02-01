from google.cloud import bigquery
import pandas as pd
import pytz
import os

"""
# Testing.
list_one = df_search_queries_volume['Search_query'].astype(str).values.tolist()
list_two = df_search_queries_volume['Volume'].astype(str).values.tolist()
list_three = df_search_queries_volume['Date'].astype(str).values.tolist()
list_four = df_search_queries_volume['Project_ID'].astype(str).values.tolist()
list_five = df_search_queries_volume['Group'].astype(str).values.tolist()

"""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.dirname(os.path.abspath(__file__)) + "\service_account.json"
client = bigquery.Client()
table_id = "test_dataset.GMB_DataTable"
bgq_records = [
    {
        "Search_query": "Life of Brian",
        "Volume": "128",
    }
]
df = pd.DataFrame(bgq_records, columns=["Search_query", "Volume"], index=pd.Index([u"1", u"2"], name="Search_query"))
job_config = bigquery.LoadJobConfig(schema=[bigquery.SchemaField("Search_query", bigquery.enums.SqlTypeNames.STRING),
                                            bigquery.SchemaField("Volume", bigquery.enums.SqlTypeNames.STRING),
])

job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
job.result()

table_bqg = client.get_table(table_id)
print(f"Loaded data from BigQuery: rows {table_bqg.num_rows}\n columns: {len(table_bqg.schema)}\n table name: {table_id}")

# Working logic.
"""for i in range(0, index[-1]):
    bgq_records = [
        {
            "Search_query": df_search_queries_volume['Search_query'][i],
            "Volume": df_search_queries_volume['Volume'][i],
            "Date": df_search_queries_volume['Date'][i],
            "Project_ID": df_search_queries_volume['Project_ID'][i],
            "Group": df_search_queries_volume['Group'][i]
        },
    ]

    df = pd.DataFrame(bgq_records, columns=["Search_query", "Volume", "Date", "Project_ID", "Group"], index=pd.Index([index[-1]], name="Search_query"))
    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("Search_query", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("Volume", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("Date", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("Project_ID", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("Group", bigquery.enums.SqlTypeNames.STRING)
    ])

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    table_bqg = client.get_table(table_id)
    # print(f"Loaded data from BigQuery: rows {table_bqg.num_rows}\n columns: {len(table_bqg.schema)}\n table name: {table_id}")
    end_time = datetime.datetime.now()
    print(f'Process duration: {end_time - start_time}')
# Closing active web browser.
driver.quit()
"""