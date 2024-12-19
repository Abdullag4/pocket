import streamlit as st
import pandas as pd

def show_overview(finance_data):
    st.title("Overview")

    # Display current financial data
    st.subheader("Financial Data")
    try:
        st.dataframe(
            finance_data.style.format({"Amount": "${:,.2f}"})
                             .highlight_min(axis=0, subset=["Amount"], color="lightcoral")
                             .highlight_max(axis=0, subset=["Amount"], color="lightgreen")
        )
    except Exception as e:
        st.error("Error displaying overview table.")
        st.text(str(e))

    # Summary Statistics
    st.subheader("Summary")
    total_expense = finance_data.loc[finance_data["Type"] == "Expense", "Amount"].sum()
    total_income = finance_data.loc[finance_data["Type"] == "Income", "Amount"].sum()
    balance = total_income + total_expense  # Expenses are negative

    st.metric("Total Income", f"${total_income:,.2f}")
    st.metric("Total Expense", f"${total_expense:,.2f}")
    st.metric("Balance", f"${balance:,.2f}")

    st.success("Overview loaded successfully!")
