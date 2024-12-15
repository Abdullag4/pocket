import streamlit as st
import pandas as pd

def show_overview(finance_data):
    """
    Display the overview page with a summary of finances.
    """
    st.title("Overview")

    # Ensure 'Amount' column is numeric to avoid calculation errors
    finance_data["Amount"] = pd.to_numeric(finance_data["Amount"], errors="coerce")

    # Check if finance_data has any data
    if finance_data.empty:
        st.write("No data available.")
        return

    # Display the data table
    st.subheader("Financial Records")
    st.dataframe(finance_data.style.highlight_max(axis=0))

    # Summarize total income and expenses
    income = finance_data[finance_data["Amount"] > 0]["Amount"].sum()
    expenses = finance_data[finance_data["Amount"] < 0]["Amount"].sum()

    st.subheader("Summary")
    col1, col2 = st.columns(2)
    col1.metric("Total Income", f"${income:.2f}")
    col2.metric("Total Expenses", f"${expenses:.2f}")

    # Grouped bar chart by category
    st.subheader("Category-wise Breakdown")
    category_summary = finance_data.groupby("Category")["Amount"].sum()
    st.bar_chart(category_summary)
