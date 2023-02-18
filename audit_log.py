import pandas as pd
import csv
import os.path
from datetime import datetime

from common import *

DATABASE_FILE = "audit_data.csv"


def read_audit_log() -> pd.DataFrame:
    """Reads the audit log from the CSV file

    Returns:
        pd.DataFrame: Dataframe containing the CVS data
    """
    if os.path.isfile(DATABASE_FILE) is False:
        with open(DATABASE_FILE, "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(AUDIT_HEADERS)

    audit_log = pd.read_csv(DATABASE_FILE)
    df = pd.DataFrame(audit_log)

    return df


def write_audit_log(df: pd.DataFrame, data: dict):
    """Writes a new row to the audit log

    Args:
        df (pd.DataFrame): The current dataframe object
        data (dict): The new json data from the latest request
    """
    row = [
        data["date"],
        data["info"]["rate"],
        data["query"]["amount"],
        data["query"]["from"],
        data["query"]["to"],
        data["result"],
    ]

    if os.path.isfile(DATABASE_FILE):
        # add the new row to the dataframe
        df.loc[len(df)] = row

        # writing into the file
        df.to_csv(DATABASE_FILE, index=False)
