import streamlit as st
import pandas as pd
from style import apply_styles

def show_overview(finance_data):
    st.header("Overview")

    # Ensure Amount column is numeric
    if 'Amount' in finance_data.columns:
        finance_data['Amount'] = pd.to_numeric(finance_data['Amount'], errors='coerce').fillna(0)
    else:
        st.error("Error: 'Amount' column not found in data.")
        return

    # Summary Section
    total_income = finance_data.loc[finance_data['Amount'] > 0, 'Amount'].sum()
    total_expense = -finance_data.loc[finance_data['Amount'] < 0, 'Amount'].sum()
    balance = total_income - total_expense

    st.subheader("Summary")
    st.write(f"**Total Income:** ${total_income:,.2f}")
    st.write(f"**Total Expense:** ${total_expense:,.2f}")
    st.write(f"**Current Balance:** ${balance:,.2f}")

    # Styled Data Display
    if not finance_data.empty:
        st.subheader("Transaction Data")
        try:
            st.dataframe(apply_styles(finance_data))
        except Exception as e:
            st.error("Error applying styles to data.")
            st.write(f"Error details: {e}")
            st.write(finance_data)  # Show raw data for debugging
    else:
        st.info("No transactions available yet.")
