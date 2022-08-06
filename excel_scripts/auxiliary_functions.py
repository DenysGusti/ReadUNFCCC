from time import perf_counter
from pathlib import Path
import pandas as pd
import logging


def calculateTime(func):
    def wrapper(*args, **kwargs):
        t: float = perf_counter()
        returned_value = func(*args, **kwargs)
        print(f'time spent in {func.__name__}: {perf_counter() - t}s')
        return returned_value

    return wrapper


def writeFile(destination: Path, sheet_df_dict: dict[str, pd.DataFrame]) -> None:
    try:
        with pd.ExcelWriter(destination, engine='openpyxl') as writer:
            for sheet, df in sheet_df_dict.items():
                df.to_excel(writer, sheet_name=sheet, index=False)

    except PermissionError:
        logging.exception('\n\nClose destination xlsx files!\n\n')


def clearStr(str_in: str) -> str:
    str_out = str_in.replace('\n', '')
    for i in range(1, 10):
        str_out = str_out.replace(f'({i})', '')
    return str_out.rstrip(' .,')
