import streamlit as st
import pandas as pd
import plotly.express as px

def show_analysis(finance_data):
    st.markdown('<div class="section-title">Analyze Your Finances</div>', unsafe_allow_html=True)

    if finance_data.empty:
        st.info("No data available for analysis. Add some transactions first.")
        return

    # Expense Analysis
    st.subheader("💸 Expense Analysis")
    expense_data = finance_data[finance_data["Type"] == "Expense"]
    if not expense_data.empty:
        category_expense_data = expense_data.groupby("Category")["Amount"].sum(-)
        st.plotly_chart(px.pie(
            category_expense_data,
            values="Amount",
            names=category_expense_data.index,
            title="Expense Breakdown by Category"
        ))
    else:
        st.write("No expense data available.")

    # Income Analysis
    st.subheader("💰 Income Analysis")
    income_data = finance_data[finance_data["Type"] == "Income"]
    if not income_data.empty:
        category_income_data = income_data.groupby("Category")["Amount"].sum()
        st.plotly_chart(px.pie(
            category_income_data,
            values="Amount",
            names=category_income_data.index,
            title="Income Breakdown by Category"
        ))
    else:
        st.write("No income data available.")

    # Trends
    st.subheader("📈 Financial Trends")
    trend_data = finance_data.groupby(["Date", "Type"])["Amount"].sum().reset_index()
    if not trend_data.empty:
        st.plotly_chart(px.line(
            trend_data,
            x="Date",
            y="Amount",
            color="Type",
            title="Trends Over Time",
            labels={"Amount": "Amount ($)", "Date": "Date"}
        ))
    else:
        st.write("No trend data available.")
