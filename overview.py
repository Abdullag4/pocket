import streamlit as st
import pandas as pd
from style import apply_styles

def show_overview(finance_data):
    st.header("Overview")

    # Ensure the Amount column is numeric
    finance_data['Amount'] = pd.to_numeric(finance_data['Amount'], errors='coerce').fillna(0)

    # Display Summary
    total_income = finance_data.loc[finance_data['Amount'] > 0, 'Amount'].sum()
    total_expense = -finance_data.loc[finance_data['Amount'] < 0, 'Amount'].sum()
    balance = total_income - total_expense

    st.subheader("Summary")
    st.write(f"**Total Income:** ${total_income:,.2f}")
    st.write(f"**Total Expense:** ${total_expense:,.2f}")
    st.write(f"**Current Balance:** ${balance:,.2f}")

    # Display finance data
    if not finance_data.empty:
        st.subheader("Transaction Data")
        st.dataframe(apply_styles(finance_data))
    else:
        st.info("No transactions available yet.")
