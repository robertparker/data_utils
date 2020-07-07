from unittest.mock import MagicMock
import mock
import pandas as pd


def test_load_only_diffs():
    """test that the load diffs correctly"""

    from_df = pd.DataFrame([{"key_col": 1, "not_key_col": 2, "col1": "one"}])

    to_df = pd.DataFrame(
        [
            {"key_col": 1, "not_key_col": 2, "col1": "one"},
            {"key_col": 2, "not_key_col": 2, "col1": "two"},
            {"key_col": 3, "not_key_col": 3, "col1": "three"},
        ]
    )
    # flake8: noqa E501
    with mock.patch("data_utils.airtable_utils.df_from_airtable", return_value=from_df):
        from data_utils.airtable_utils import df_to_airtable

        mock_con = MagicMock()
        df_to_airtable(to_df, "airtable_table", ["key_col"], con=mock_con)
        assert mock_con.create.call_count == 2


def test_env_args_are_passed_to_airtable_con(monkeypatch):
    """test that env args as passed"""
    monkeypatch.setenv("AIRTABLE_BASE_KEY", "base1")
    monkeypatch.setenv("AIRTABLE_API_KEY", "key1")

    from data_utils.airtable_utils import conn

    con = conn()
    assert con.url == "https://api.airtable.com/v0/base1"
    assert con.headers == {"Authorization": "Bearer key1"}

    # assert arguments passed are prioritized over env
    con2 = conn(base_key="base2", api_key="key2")
    assert con2.base_url == "https://api.airtable.com/v0/base2"
    assert con2.headers == {"Authorization": "Bearer key2"}
