from google.cloud import bigquery
import pandas as pd
import pytz
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ststoyan\MyBusiness_API_Project\service_account.json"
client = bigquery.Client()
table_id = "serpact-tool.test_dataset.GMB_Test_Table"
bgq_records = [
    {
        "Search_query": "Dummy",
        "Volume": "Dummy",
        "Date": "Dummy",
        "Project": "Dummy",
        "Group": "Dummy"
    },
]
df = pd.DataFrame(bgq_records, columns=["Search_query", "Volume", "Date", "Project", "Group"])
job_config = bigquery.LoadJobConfig(schema=[
    bigquery.SchemaField("Search_query", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("Volume", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("Date", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("Project", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("Group", bigquery.enums.SqlTypeNames.STRING)
])

job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
job.result()

table_bqg = client.get_table(table_id)
print(f"Loaded data from BigQuery: rows {table_bqg.num_rows}\n columns: {len(table_bqg.schema)}\n table name: {table_id}")
