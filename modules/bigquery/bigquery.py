from .config import *
from .constants import *
from ..file_operations import read_file
from ..dates import dt_now

import os
import pandas as pd
from typing import Tuple
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest


class BigQuery:
    def __init__(self, project: str = PROJECT):
        """Initializes client object"""
        self.project = project
        self.client = bigquery.Client(project=project)

    def _build_job_config(
        self, gcs_path: str, write_type: str, schema: list = None
    ) -> bigquery.LoadJobConfig:
        args = {}
        if schema:
            if type(schema[0]) == dict:
                args["schema"] = [bigquery.SchemaField(**d) for d in schema]
            elif type(schema[0]) == tuple:
                args["schema"] = [
                    bigquery.SchemaField(name=d[0], field_type=d[1], mode=d[2])
                    for d in schema
                ]
        else:
            args["autodetect"] = True

        args["source_format"] = SOURCE_FORMAT.get(os.path.splitext(gcs_path)[1])
        if args["source_format"] == bigquery.SourceFormat.CSV:
            args["skip_leading_rows"] = 1

        args["write_disposition"] = WRITE_DISPOSITION.get(write_type)
        lj = bigquery.LoadJobConfig(**args)
        return lj

    def run_query(
        self, query: str, query_kwargs: dict = None, return_to_df: bool = False
    ) -> Tuple[None, pd.DataFrame]:
        """Executes query in BigQuery.
        Params:
            query: query can be relative path to file or actual query text.
            query_kwargs: Kwargs can be used to format parameters in query file
            return_to_df: whether to return Pandas dataframe
        """
        if os.path.isfile(query):
            query = read_file(query, **query_kwargs)

        result = self.client.query(query)
        result.result()
        if return_to_df:
            return result.to_dataframe()

    def load_gcs_to_table(
        self,
        bucket: str,
        gcs_path: str,
        table_project: str,
        table_dataset: str,
        table_name: str,
        schema: list = None,
        write_type: str = WRITE_TYPE,
    ) -> None:
        """Loads file(s) from Google Cloud Storage to BigQuery
        Params:
            bucket: str of gcs bucket
            gcs_path: str path in gcs bucket (can use wildcard)
            table_project: str GCP project name
            table_dataset: str GCP dataset name
            table_name: str table name
            schema: list of tuples (column name, column type, column mode)
            write_type: truncate, append, replace
        """
        job_config = self._build_job_config(
            gcs_path=gcs_path, write_type=write_type, schema=schema
        )
        load_job = self.client.load_table_from_uri(
            source_uris=f"gs://{bucket}/{gcs_path}",
            destination=f"{table_project}.{table_dataset}.{table_name}",
            job_config=job_config,
        )
        try:
            load_job.result()
        except BadRequest as br:
            for err in br.errors:
                print(f"Error: {err}")

    def export_to_gcs(
        self,
        bucket: str,
        gcs_path: str,
        table_project: str,
        table_dataset: str,
        table_name: str,
    ) -> None:
        """
        Exports table to Google Cloud Storage
        Params:
            bucket: str of gcs bucket
            gcs_path: str path in gcs bucket (can use wildcard)
            table_project: str GCP project name
            table_dataset: str GCP dataset name
            table_name: str table name
        """
        if os.path.isdir(gcs_path):
            gcs_path = f"{gcs_path}/{table_project}_{table_dataset}_{table_name}_{dt_now(format_type='numeric_date')}.csv"

        dataset = bigquery.DatasetReference(
            project=table_project, dataset_id=table_dataset
        )
        source = dataset.table(table_name)
        destination_uris = f"gs://{bucket}/{gcs_path}"
        extract = self.client.extract_table(
            source=source, destination_uris=destination_uris
        )
        extract.result()
