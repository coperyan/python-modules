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

    def set_project(self, project: str) -> None:
        self.project = project
        self.client = bigquery.Client(project=project)

    def _build_job_config(
        self, gcs_path: str, write_type: str, schema: list = None
    ) -> bigquery.LoadJobConfig:
        """Build BigQuery LoadJobConfig

        Parameters
        ----------
            gcs_path : str
                path within google_cloud_storage bucket, used to identify file extension
            write_type : str
                truncate, append, create
            schema (list, optional): list, default None
                list of tuple or list of dict
                    ex. `[("colname","coltype","colmode")]` OR
                    ex. `[{"name":"colname","type":"STRING","mode":"NULLABLE"}]`

        Returns
        -------
            bigquery.LoadJobConfig
                Load job config used in method `load_gcs_to_table`
        """
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
        self, query: str, query_kwargs: dict = {}, return_to_df: bool = False
    ) -> Tuple[None, pd.DataFrame]:
        """Run Query in BigQuery

        Parameters
        ----------
            query : str
                Str of SQL Query OR path to file w/ query str
            query_kwargs (dict, optional): dict, default {}
                ex. query `SELECT {col} FROM table LIMIT 500;`
                ex. kwargs `{col : colname}`
            return_to_df (bool, optional): bool, default False
                return to dataframe? else just run query

        Returns
        -------
            Tuple[None, pd.DataFrame]
                None if return_to_df = false otherwise pd.DataFrame of results
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
        """Load File(s) from Google Cloud Storage to BigQuery Table

        Parameters
        ----------
            bucket : str
                google_cloud_storage bucket name
            gcs_path : str
                google_cloud_storage bucket sub-path
                    can be direct path: ex. `bucketFolder/bucketSubFolder/file.csv`
                    can be wildcard path: ex `bucketFolder/bucketSubFolder/.*json`
            table_project : str
                bigquery project name
            table_dataset : str
                bigquery dataset name
            table_name : str
                bigquery table name
            schema (list, optional): list, default None
                list of tuple or list of dict
                    ex. `[("colname","coltype","colmode")]` OR
                    ex. `[{"name":"colname","type":"STRING","mode":"NULLABLE"}]`
            write_type (str, optional): str, default WRITE_TYPE
                truncate, append, create
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
        """Export BigQuery Table to Google Cloud Storage

        Parameters
        ----------
            bucket : str
                google_cloud_storage bucket name
            gcs_path : str
                bucket sub-path to store file in
            table_project : str
                bigquery project name
            table_dataset : str
                bigquery dataset name
            table_name : str
                bigquery table name
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
