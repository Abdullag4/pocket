import streamlit as st
import pandas as pd
from datetime import date

def show_add_income(finance_data, db_file):
    st.title("➕ Add Income")

    # Add Income Form
    with st.form("add_income_form"):
        income_date = st.date_input("Date", value=date.today())  # Default to today
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Income")

        if submitted:
            # Validate inputs
            if not category or amount <= 0:
                st.warning("Please fill in all required fields with valid values.")
            else:
                new_income = {
                    "Date": income_date.strftime("%Y-%m-%d"),  # Format date properly
                    "Category": category,
                    "Amount": amount,
                    "Type": "Income",
                    "Notes": notes,
                }
                # Append the new income and save to the CSV file
                st.session_state["finance_data"] = st.session_state["finance_data"].append(new_income, ignore_index=True)
                st.session_state["finance_data"].to_csv(db_file, index=False)
                st.success("Income added successfully!")
                st.experimental_rerun()  # Refresh the page to display changes

    # Display Updated Table
    st.subheader("Updated Incomes")
    st.dataframe(finance_data[finance_data["Type"] == "Income"])
