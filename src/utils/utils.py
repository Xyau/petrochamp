import io

from pandas import DataFrame

def get_dataframe_info(df: DataFrame) -> str:
    info = io.StringIO()
    df.info(verbose=True, buf=info)
    return info.getvalue()