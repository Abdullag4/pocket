import streamlit as st
import pandas as pd

def show_add_expense(finance_data, db_file):
    st.header("Add Expense")
    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Clothes", "Electric"])
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            new_data = pd.DataFrame({
                "Date": [date],
                "Type": ["Expense"],
                "Category": [category],
                "Amount": [-amount],  # Expense amounts are stored as negative
                "Notes": [notes]
            })
            
            # Use pd.concat instead of append
            finance_data = pd.concat([finance_data, new_data], ignore_index=True)
            finance_data.to_csv(db_file, index=False)  # Save to CSV
            st.success("Expense added successfully!")
