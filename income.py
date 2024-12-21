import streamlit as st
import pandas as pd
from datetime import date

def show_add_income(finance_data, db_file):
    st.title("➕ Add Income")

    with st.form("income_form"):
        income_date = st.date_input("Date", value=date.today())  # Default to today
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Income")

        if submitted:
            new_income = {
                "Date": income_date.strftime("%Y-%m-%d"),  # Ensure date is formatted as string
                "Category": category,
                "Amount": amount,
                "Type": "Income",
                "Notes": notes,
            }
            finance_data = finance_data.append(new_income, ignore_index=True)
            finance_data.to_csv(db_file, index=False)
            st.success("Income added successfully!")

    st.subheader("Current Incomes")
    st.dataframe(finance_data)
    return finance_data
