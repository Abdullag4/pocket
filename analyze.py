import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_analysis(finance_data):
    st.title("Analyze Your Data")

    # Separate data
    expense_data = finance_data[finance_data["Type"] == "Expense"]
    income_data = finance_data[finance_data["Type"] == "Income"]

    # Pie Chart for Expenses
    st.subheader("Expense Analysis")
    if not expense_data.empty:
        category_expense_data = expense_data.groupby("Category")["Amount"].sum()
        fig1, ax1 = plt.subplots()
        category_expense_data.plot.pie(
            autopct="%1.1f%%", startangle=90, ax=ax1, ylabel=""
        )
        st.pyplot(fig1)
    else:
        st.info("No expense data available.")

    # Pie Chart for Incomes
    st.subheader("Income Analysis")
    if not income_data.empty:
        category_income_data = income_data.groupby("Category")["Amount"].sum()
        fig2, ax2 = plt.subplots()
        category_income_data.plot.pie(
            autopct="%1.1f%%", startangle=90, ax=ax2, ylabel=""
        )
        st.pyplot(fig2)
    else:
        st.info("No income data available.")

    # Trends Chart
    st.subheader("Trends Over Time")
    if not finance_data.empty:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"])
        trends_data = finance_data.groupby(["Date", "Type"])["Amount"].sum().unstack(fill_value=0)
        st.line_chart(trends_data)
    else:
        st.info("No data available for trends.")
