from typing import Any

import gspread
import pandas as pd
from pandas import DataFrame
import streamlit as st

from src.constants.constants import NUMBER, SETS, QUESTION, ANSWER, ANSWER_TYPE
from src.security.security import get_credentials


@st.experimental_singleton
def get_all_rows(key: str) -> DataFrame:
    return get_just_simple_rows_base(key).copy()


def refresh_questions():
    get_all_rows.clear()


def get_just_simple_rows_base(key: str) -> DataFrame:
    credentials = get_credentials(key)
    gc = gspread.service_account_from_dict(credentials)

    visible_files = gc.list_spreadsheet_files()
    print(f'Files: {visible_files}')
    spreadsheet = gc.open(title="Set Liga ITBA")
    print(f'Spreadsheet: {spreadsheet}')
    worksheet = spreadsheet.worksheet("Competencia Individual ")
    print(f'Worksheet: {worksheet}')
    raw_rows: list[list[str]] = worksheet.get_values()
    print(f'Values: {raw_rows[0]}')
    records: list[dict[str, Any]] = []
    sets_index = {idx: set_name for idx, set_name in enumerate(raw_rows[0][2:])}
    print(sets_index)
    for id, row in enumerate(raw_rows[1:]):
        sets = ["ALL"]
        if len(str(row[0])) is not 0 and len(str(row[1])) is not 0:
            for set_idx, set_presence in enumerate(row[2:]):
                if set_presence == "TRUE":
                    sets.append(sets_index[set_idx])

            record = {
                NUMBER: int(id),
                SETS: sets,
                QUESTION: str(row[0]),
                ANSWER: str(row[1]),
            }

            records.append(record)
    df = pd.DataFrame.from_records(records)
    return df

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
    # assert raw_rows[0][1] == SET
    # assert raw_rows[0][2] == SET_NUMBER
    assert raw_rows[0][3] == QUESTION
    assert raw_rows[0][4] == ANSWER
    assert raw_rows[0][5] == ANSWER_TYPE
    records: list[dict[str, Any]] = []
    for row in raw_rows[1:]:
        record = {
            NUMBER: int(row[0]),
            # SET: str(row[1]),
            # SET_NUMBER: str(row[2]),
            QUESTION: str(row[3]),
            ANSWER: str(row[4]),
            ANSWER_TYPE: str(row[5]),
        }
        records.append(record)
    df = pd.DataFrame.from_records(records)
    return df