import os
from typing import Optional, List
from airtable import airtable
import pandas as pd


def load_df_to_airtable(
    df: pd.DataFrame,
    table_name: str,
    unique_keys: List[str],
    base_key: Optional[str] = os.environ["AIRTABLE_BASE_KEY"],
    api_key: Optional[str] = os.environ["AIRTABLE_API_KEY"],
) -> None:
    """idempotent insert of csv rows to airtable"""

    # get all airtable records
    at = airtable.Airtable(base_key, api_key)
    existing = []
    for rec in at.iterate(table_name):
        od = rec["fields"]
        od.update({"id": rec["id"]})
        existing.append(od)
    existing_df = pd.DataFrame(existing)

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
