import streamlit as st
import pandas as pd
from style import apply_styles

def show_overview(db_file):
    st.title("Overview")
    try:
        # Load data
        finance_data = pd.read_csv(db_file)
        finance_data['Amount'] = pd.to_numeric(finance_data['Amount'], errors='coerce')

        # Display overview
        st.subheader("Financial Data")
        st.dataframe(apply_styles(finance_data))

        # Summary
        total_income = finance_data[finance_data['Amount'] > 0]['Amount'].sum()
        total_expense = finance_data[finance_data['Amount'] < 0]['Amount'].sum()
        net_balance = total_income + total_expense

        st.subheader("Summary")
        st.write(f"**Total Income:** ${total_income:.2f}")
        st.write(f"**Total Expense:** ${abs(total_expense):.2f}")
        st.write(f"**Net Balance:** ${net_balance:.2f}")

    except Exception as e:
        st.error("Failed to load data.")
        st.write(f"Error details: {e}")
