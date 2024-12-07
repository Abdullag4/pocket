import streamlit as st
import pandas as pd

def show_add_income(finance_data, db_file):
    st.header("Add Income")
    with st.form("income_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Salary", "Investment"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Income")

    if submitted:
        new_data = {
            "Date": date.strftime("%Y-%m-%d"),
            "Type": "Income",
            "Category": category,
            "Amount": amount,
            "Notes": notes
        }
        finance_data = finance_data.append(new_data, ignore_index=True)
        finance_data.to_csv(db_file, index=False)  # Save to CSV
        st.success("Income added successfully!")
