import pandas as pd
from typing import Union


def replace_bad_vals(df: pd.DataFrame) -> pd.DataFrame:
    for col in [x for x in df.columns.values if df[x].dtype == "object"]:
        rowct = len(
            df[
                (df[col].str.contains(r"\n") == True)
                | (df[col].str.contains(r"\r") == True)
            ]
        )
        if rowct > 0:
            print(f"Bad values found in {col} -- {rowct}")
            df[col] = df[col].str.replace(r"\r", "", regex=True)
            df[col] = df[col].str.replace(r"\n", "", regex=True)

    return df


def col_to_datetime(df: pd.DataFrame, col: Union[str, list]) -> pd.DataFrame:
    if isinstance(col, str):
        col = [col]

    for c in col:
        df[c] = pd.to_datetime(df[c])

    return df


def limit_df_fields(
    df: pd.DataFrame, fields: list, default_cols: dict = None
) -> pd.DataFrame:
    cols_to_drop = [col for col in df.columns.values if col not in fields]
    df.drop(columns=cols_to_drop, inplace=True)
    if default_cols:
        for field in [
            (k, v) for k, v in default_cols.items() if k not in df.columns.values
        ]:
            df[field[0]] = field[1]
            print(f"Added field {field[0]} with default val {field[1]}")
    df = df[[f for f in fields]]
    return df
