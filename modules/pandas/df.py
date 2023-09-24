import pandas as pd
import builtins
from typing import Union, List, Dict


def replace_bad_vals(df: pd.DataFrame) -> pd.DataFrame:
    """Replace newline characters in dataframe

    Parameters
    ----------
        df : pd.DataFrame

    Returns
    -------
        pd.DataFrame
    """
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
    """Format pandas column(s) as datetime

    Parameters
    ----------
        df : pd.DataFrame
        col : Union[str, list]
            str or list of str (column names)

    Returns
    -------
        pd.DataFrame
    """
    if isinstance(col, str):
        col = [col]

    for c in col:
        df[c] = pd.to_datetime(df[c])

    return df


def limit_df_fields(
    df: pd.DataFrame, fields: list, default_cols: dict = None
) -> pd.DataFrame:
    """Standardize fields in dataframe

    Parameters
    ----------
        df : pd.DataFrame
        fields : list
            list of fields to keep
        default_cols (dict, optional): dict, default None
            dictionary of columns & default values to add if missing
            ex. `{col:default_val}`

    Returns
    -------
        pd.DataFrame
    """
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


def nested_dict_to_df(
    raw_data: Union[List, Dict],
    remove_value_types: list = None,
    df_params: dict = None,
    rename_cols: dict = None,
    delete_fields: list = None,
    index_cols: dict = None,
    rename_patterns: dict = None,
    add_fields: dict = None,
) -> pd.DataFrame:
    """Parses a nested array of dict to a pandas dataframe

    Parameters
    ----------
        raw_data : Union[List, Dict]
        remove_value_types (list, optional): list, default None
            types to remove from nested dictionaries ex. `list`
        df_params (dict, optional): dict, default None
            parameters to pass to pd.json_normalize
            https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
        rename_cols (dict, optional): dict, default None
            dict of column renames
            ex. `{oldname:newname}`
        delete_fields (list, optional): list, default None
            fields to drop from the df entirely
        index_cols (dict, optional): dict, default None
            list of cols to be considered 'index' -- move to front of order
        rename_patterns (dict, optional): dict, default None
            dictionary of rename_patterns to apply to column names
            ex. `{'dict.col':'col'} would rename dict.col.name to col.name`
        add_fields (dict, optional): dict, default None
            dictionary of columns & default values to add if missing
            ex. `{col:default_val}`

    Returns
    -------
        pd.DataFrame
    """
    if type(df_params) == list:
        df = raw_data.copy()
        for df_param in df_params:
            if type(df) == pd.DataFrame:
                df = df.to_dict(orient="records")
            df = pd.json_normalize(df, **df_param)

    elif remove_value_types:
        remove_value_types = [getattr(builtins, x) for x in remove_value_types]
        df = pd.json_normalize(
            [
                {k: v for k, v in d.items() if type(v) not in remove_value_types}
                for d in raw_data
            ],
            **df_params,
        )
    else:
        df = pd.json_normalize(raw_data, **df_params)

    if rename_cols:
        df = df.rename(columns=rename_cols)

    if add_fields:
        for k, v in add_fields.items():
            df[k] = v

    if delete_fields:
        df = df.drop(columns=delete_fields)

    if index_cols:
        df = df[
            index_cols + [col for col in df.columns.values if col not in index_cols]
        ]
    if rename_patterns:
        for k, v in rename_patterns.items():
            df = df.rename(columns={k: v})

    return df
