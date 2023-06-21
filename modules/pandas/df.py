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
