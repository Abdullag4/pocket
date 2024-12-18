import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_analysis(finance_data):
    st.title("Financial Analysis")
    
    # Separate data for Expense and Income
    expense_data = finance_data[finance_data["Type"] == "Expense"]
    income_data = finance_data[finance_data["Type"] == "Income"]

    # Section 1: Expense Analysis
    st.header("Expense Analysis")
    if not expense_data.empty:
        st.subheader("Category Distribution for Expenses")
        category_expense_data = expense_data.groupby("Category")["Amount"].sum()
        fig1, ax1 = plt.subplots()
        category_expense_data.plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            ax=ax1,
            labels=category_expense_data.index,
            colors=plt.cm.Paired.colors
        )
        ax1.set_ylabel("")
        st.pyplot(fig1)

        st.subheader("Monthly Expense Trend")
        expense_data["Month"] = pd.to_datetime(expense_data["Date"]).dt.to_period("M")
        monthly_expense_trend = expense_data.groupby("Month")["Amount"].sum()
        st.line_chart(monthly_expense_trend)
    else:
        st.info("No expense data available for analysis.")

    # Section 2: Income Analysis
    st.header("Income Analysis")
    if not income_data.empty:
        st.subheader("Category Distribution for Incomes")
        category_income_data = income_data.groupby("Category")["Amount"].sum()
        fig2, ax2 = plt.subplots()
        category_income_data.plot.pie(
            autopct='%1.1f%%',
            startangle=90,
            ax=ax2,
            labels=category_income_data.index,
            colors=plt.cm.Set2.colors
        )
        ax2.set_ylabel("")
        st.pyplot(fig2)

        st.subheader("Monthly Income Trend")
        income_data["Month"] = pd.to_datetime(income_data["Date"]).dt.to_period("M")
        monthly_income_trend = income_data.groupby("Month")["Amount"].sum()
        st.line_chart(monthly_income_trend)
    else:
        st.info("No income data available for analysis.")

    # Section 3: Overall Analysis
    st.header("Overall Analysis")
    if not finance_data.empty:
        st.subheader("Expense vs. Income")
        total_expense = expense_data["Amount"].sum()
        total_income = income_data["Amount"].sum()
        overall_data = pd.DataFrame({
            "Type": ["Expense", "Income"],
            "Amount": [total_expense, total_income]
        })
        fig3, ax3 = plt.subplots()
        overall_data.set_index("Type")["Amount"].plot.bar(ax=ax3, color=["red", "green"])
        ax3.set_ylabel("Amount")
        ax3.set_title("Expense vs Income")
        st.pyplot(fig3)
    else:
        st.info("No financial data available for overall analysis.")
