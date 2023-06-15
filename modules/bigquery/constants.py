from google.cloud import bigquery

WRITE_DISPOSITION = {
    "truncate": bigquery.WriteDisposition.WRITE_TRUNCATE,
    "append": bigquery.WriteDisposition.WRITE_APPEND,
}

SOURCE_FORMAT = {
    ".csv": bigquery.SourceFormat.CSV,
    ".json": bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
}
