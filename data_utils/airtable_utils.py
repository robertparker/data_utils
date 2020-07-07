import os
from typing import Optional, List
from airtable import airtable
import pandas as pd


def conn(
    base_key: Optional[str] = None, api_key: Optional[str] = None,
) -> airtable.Airtable:
    base_key = base_key or os.environ.get("AIRTABLE_BASE_KEY")
    api_key = api_key or os.environ.get("AIRTABLE_API_KEY")
    return airtable.Airtable(base_key, api_key)


def df_from_airtable(table_name: str, con: Optional[airtable.Airtable]) -> pd.DataFrame:
    """receives a dataframe from airtable"""
    at = con or conn()

    results = []
    for rec in at.iterate(table_name):
        od = rec["fields"]
        od.update({"id": rec["id"]})
        results.append(od)
    df = pd.DataFrame(results)
    return df


# flake8: noqa E501
def df_to_airtable(
    df: pd.DataFrame,
    table_name: str,
    unique_keys: List[str],
    con: Optional[airtable.Airtable],
) -> None:
    """idempotent insert of csv rows to airtable"""

    at = con or conn()
    existing_df = df_from_airtable(table_name, con=at)

    # TODO: assert column names match
    #       there appears to be an airtable.py bug
    #       in which not all columns can be pulled.

    # figure out which records in the df already exist
    existing_ids_df = existing_df[unique_keys]
    merge_df = df.merge(existing_ids_df, how="outer", indicator=True)
    insert_df = merge_df[merge_df["_merge"].isin(["left_only"])].copy()
    del insert_df["_merge"]

    print(f"inserting {len(insert_df)} rows into {table_name}.")
    insert_dict = insert_df.to_dict("records")
    for d in insert_dict:
        at.create(table_name, d)
