from typing import Any

import gspread
import pandas as pd
from pandas import DataFrame
import streamlit as st

from src.constants.constants import NUMBER, SET, SET_NUMBER, QUESTION, ANSWER, ANSWER_TYPE
from src.security.security import get_credentials

#
# def get_all_rows(key: str, cached: bool) -> DataFrame:
#     if cached:
#         return get_all_rows_cached(key)
#     else:
#         return get_all_rows_base(key)

@st.experimental_singleton
def get_all_rows(key: str) -> DataFrame:
    return get_all_rows_base(key).copy()

def refresh_questions():
    get_all_rows.clear()

def get_all_rows_base(key: str) -> DataFrame:
    credentials = get_credentials(key)
    gc = gspread.service_account_from_dict(credentials)

    visible_files = gc.list_spreadsheet_files()
    print(f'Files: {visible_files}')
    spreadsheet = gc.open(title="Dataset preguntas")
    print(f'Spreadsheet: {spreadsheet}')
    worksheet = spreadsheet.worksheet("questions")
    print(f'Worksheet: {worksheet}')
    raw_rows: list[list[str]] = worksheet.get_values()
    print(f'Values: {raw_rows[0]}')
    assert raw_rows[0][0] == NUMBER
    assert raw_rows[0][1] == SET
    assert raw_rows[0][2] == SET_NUMBER
    assert raw_rows[0][3] == QUESTION
    assert raw_rows[0][4] == ANSWER
    assert raw_rows[0][5] == ANSWER_TYPE
    records: list[dict[str, Any]] = []
    for row in raw_rows[1:]:
        record = {
            NUMBER: int(row[0]),
            SET: str(row[1]),
            SET_NUMBER: int(row[2]),
            QUESTION: str(row[3]),
            ANSWER: str(row[4]),
            ANSWER_TYPE: str(row[5]),
        }
        records.append(record)
    df = pd.DataFrame.from_records(records)
    return df