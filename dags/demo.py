
import json
import pandas as pd
import pendulum

from airflow.decorators import dag, task
import requests
from airflow.operators.python import PythonOperator


@dag(
    dag_id="demo",
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 6, 4, tz="UTC"),
    catchup=False,
    tags=['demo'],
)
def demo_taskflow_api_etl(url):
    @task()
    def extract(url):
        """
        Load data from data portal by API
        """
        response = requests.get(url).json()
        data = response["result"]["records"]
        print("===================")
        print(data)
        return data

    @task(multiple_outputs=True)
    def transform(data: list):
        """
        #### Transform task
        Transform data to DataFrame. And compute total expenditure.
        """
        data_df = pd.DataFrame(data)
        data_df = data_df[["sector", "ministry", "amount"]]
        data_df["amount"] = data_df["amount"].apply(pd.to_numeric)
        sector_total = data_df[["sector", "amount"]].groupby(by="sector").sum().to_dict()["amount"]
        ministry_total = data_df[["ministry", "amount"]].groupby(by="ministry").sum().to_dict()["amount"]
        return {"sector_total": sector_total, "ministry_total": ministry_total}

    @task()
    def load(expenditure_total_dict: dict, column):
        """
        "save sector total and ministry total in .csv file
        """
        total_df = pd.DataFrame(
            [{column: key, "expenditure_total": value} for key, value in expenditure_total_dict.items()])
        total_df.to_csv(f"{column}_total.csv", index=False)

    # [START main_flow]
    data = extract(url)
    expenditure_totals = transform(data)
    load(expenditure_totals["sector_total"], "sector")
    load(expenditure_totals["ministry_total"], "ministry")
    # [END main_flow]


url = "https://data.gov.sg/api/action/datastore_search?resource_id=7b4af397-3e8f-40de-9208-90d168afc810&limit=32000"
demo_dag = demo_taskflow_api_etl(url=url)
