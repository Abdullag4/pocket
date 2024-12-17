import streamlit as st
import pandas as pd
from style import apply_styles

def save_data(finance_data, db_file):
    try:
        finance_data['Amount'] = pd.to_numeric(finance_data['Amount'], errors='coerce')
        finance_data.to_csv(db_file, index=False)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def show_add_income(finance_data, db_file):
    st.header("Add Income")
    with st.form("income_form"):
        date = st.date_input("Date")
        category = st.text_input("Category")
        amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Income")
    
        if submitted:
            # Append new data
            new_data = {"Date": str(date), "Category": category, "Amount": amount, "Notes": notes}
            finance_data = finance_data.append(new_data, ignore_index=True)
            save_data(finance_data, db_file)
            st.success("Income added successfully.")
            st.dataframe(apply_styles(finance_data))  # Display updated table
    
    return finance_data
