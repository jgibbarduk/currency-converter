import streamlit as st
import requests
import json
import arrow
import pandas as pd
import csv
import os.path
from datetime import datetime

from common import *
from api import *
from audit_log import *

CURRENCY_LIST = ["GBP", "EUR", "USD", "ISK"]


#############################
# Top Section
#############################

st.title("Currency Converter")

# define columns
col1, col2 = st.columns(2, gap="medium")
# initial read of the audit log
audit_log = read_audit_log()

#############################
# Column 1 - Inputs
#############################

with col1:
    st.title("Inputs")
    from_currency = st.selectbox(
        "What currency would you like to convert FROM?", CURRENCY_LIST
    )

    to_currency = st.selectbox(
        "What currency would you like to convert TO?", CURRENCY_LIST
    )

    amount = st.number_input("Insert an amount", 1.00)

#############################
# Column 1 - Details
#############################

with col2:
    st.title("Details")
    st.write("Amount to convert: ", amount)
    st.success(f"Convert from {from_currency} to {to_currency}")
    data = {}
    if st.button("Convert Currency"):
        with st.spinner("Working on it..."):
            # get data from API
            data = get_data(from_currency, to_currency, amount)

        if "Error" in data:
            st.error(data)
        else:
            # show metric with converted amount
            st.metric(label=f"Currency in {to_currency}", value=data["result"])
            # write api data to the audit log
            write_audit_log(df=audit_log, data=data)

#############################
# Audit Section
#############################

st.title("Audit")

# get the date of the first entry of the audit log, so that it always shows some data
first_audit_log_date = audit_log.loc[0]["date"]

# set the start date to the first audit log entry
start = st.date_input("Start Date:", arrow.get(first_audit_log_date).datetime)

# set the end date 2 days out from the first audit log entry
end = st.date_input(
    "End Date:", arrow.get(first_audit_log_date).shift(days=+2).datetime
)

# create the filter for the audit log from the dates selected
filter = (audit_log["date"] >= arrow.get(start).format("YYYY-MM-DD")) & (
    audit_log["date"] <= arrow.get(end).format("YYYY-MM-DD")
)

# show the audit log, filtered on the date range
st.dataframe(audit_log.loc[filter], use_container_width=True)
