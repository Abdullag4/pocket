import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_analysis(finance_data):
    st.title("Analyze Your Finances")

    # Separate expenses and incomes
    expenses = finance_data[finance_data["Type"] == "Expense"]
    incomes = finance_data[finance_data["Type"] == "Income"]

    # Summary Statistics
    st.subheader("Summary Statistics")
    total_expense = expenses["Amount"].sum()
    total_income = incomes["Amount"].sum()
    balance = total_income + total_expense  # Expenses are negative

    st.metric("Total Income", f"${total_income:,.2f}")
    st.metric("Total Expense", f"${total_expense:,.2f}")
    st.metric("Balance", f"${balance:,.2f}")

    # Pie Charts
    st.subheader("Category Distribution")

    # Expense Categories
    if not expenses.empty:
        st.write("Expense Categories")
        category_expense_data = expenses.groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        category_expense_data.plot.pie(
            autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors, ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)

    # Income Categories
    if not incomes.empty:
        st.write("Income Categories")
        category_income_data = incomes.groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        category_income_data.plot.pie(
            autopct="%1.1f%%", startangle=90, colors=plt.cm.Set3.colors, ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)

    # Trends Over Time
    st.subheader("Trends Over Time")
    if not finance_data.empty:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"])
        trend_data = finance_data.groupby(["Date", "Type"])["Amount"].sum().unstack().fillna(0)
        st.line_chart(trend_data)

    st.info("This page provides insights into your financial data, showing category distributions and trends.")

