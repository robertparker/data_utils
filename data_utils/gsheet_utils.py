import os
import pygsheets
import logging as logger
from typing import Optional, Dict, Union, List, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    # pylint: disable=ungrouped-imports
    from pygsheets.spreadsheet import Spreadsheet
    from pygsheets.worksheet import Worksheet
    from pygsheets.client import Client
    from pandas import DataFrame


class GSheet(object):
    def __init__(self, url: Optional[str] = None):
        self.client: "Client" = self._client()
        # if url is None:
        # url = self.config.gsheets.url
        self.url = url
        self.spreadsheet: "Spreadsheet" = self._spreadsheet()

    def _client(self):
        # with tempfile.NamedTemporaryFile(suffix='.json', prefix='rohitparulkar', mode='w',) as f:
        #     f.write(self.config.gcs.gcloud_creds)
        #     f.flush()
        pygsheets_client = pygsheets.authorize(
            service_account_file=os.environ["GSHEETS_CREDS"]
        )
        return pygsheets_client

    def _spreadsheet(self):
        return self._client().open_by_url(self.url)

    @classmethod
    def worksheet_as_df(cls, worksheet: "Worksheet") -> "DataFrame":
        """this exists so it can be overriden with custom logic in child classes"""
        return worksheet.get_as_df()

    def delete_rows_by_criteria(  # type: ignore
        self, row_criteria: Dict, worksheet: "Worksheet", header_row: Optional[int] = 1,
    ) -> Union[None, Callable]:
        """
        Recursively deletes rows matching given criteria.
        This is needed because deletion happens on the basis of row_number,
        but row_number changes after each delete.
        """
        # refresh the spreadsheet object to account for previous row deletions
        self.spreadsheet = self._spreadsheet()
        worksheet_df = self.worksheet_as_df(worksheet=worksheet)

        query = " & ".join(
            ["`{}`.astype('str') == '{}'".format(k, v) for k, v in row_criteria.items()]
        )
        duplicate_rows_df = worksheet_df[worksheet_df.eval(query)]
        logger.info(
            "found existing spreadsheet rows for query",
            num_rows=len(duplicate_rows_df),
            query=query,
        )
        if len(duplicate_rows_df) == 0:
            return None

        duplicate_rows_idx = [
            idx + header_row + 1 for idx in duplicate_rows_df.index.tolist()
        ]
        row_num = duplicate_rows_idx[0]
        logger.info(
            "deleting existing row in sheet", row_num=row_num, worksheet=worksheet.title
        )
        worksheet.delete_rows(row_num)
        self.delete_rows_by_criteria(row_criteria, worksheet, header_row=header_row)

    def add_rows_to_sheet(
        self,
        rows: List[Dict],
        worksheet_name: str,
        header_row: Optional[int] = 1,
        dedupe_by: Optional[List] = None,
    ):
        """adds rows to a sheet and upserts if asked. Works only if the worksheet
        in questions is purely tabular.

        rows: rows being upserted, where each key is a header in the Google Sheet.
            Keys can be incomplete.
        worksheet_name: title of the worksheet
        header_row: row_number of the tabular data. Default to 1.
        dedupe_by: list of columns to dedupe by.  If True, then before inserting
            will delete all existing Gsheet rows matching the column's values in the
            first row of the rows arg (assumes these are uniform).

        """
        worksheet = self.spreadsheet.worksheet_by_title(worksheet_name)
        if dedupe_by is not None:
            # de-duplicate based on values in row
            row_criteria = {k: v for k, v in rows[0].items() if k in dedupe_by}
            self.delete_rows_by_criteria(row_criteria, worksheet, header_row=header_row)

        worksheet = self.spreadsheet.worksheet_by_title(worksheet_name)
        for row in rows:
            header = worksheet.get_row(header_row)
            insert_row = []
            for col in header:
                insert_val = row.get(col) or ""
                insert_row.append(insert_val)
            cells = worksheet.get_all_values(
                include_tailing_empty_rows=False,
                include_tailing_empty=False,
                returnas="matrix",
            )
            last_row = len(cells)
            worksheet.append_table(
                values=insert_row, start="A{}".format(str(last_row + 1))
            )
