import streamlit as st
import pandas as pd

def show_add_expense(finance_data, db_file):
    st.header("Add Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Clothes", "Electric"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = {
            "Date": date.strftime("%Y-%m-%d"),
            "Type": "Expense",
            "Category": category,
            "Amount": -amount,
            "Notes": notes
        }
        finance_data = finance_data.append(new_data, ignore_index=True)
        finance_data.to_csv(db_file, index=False)  # Save to CSV
        st.success("Expense added successfully!")
