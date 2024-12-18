import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_analysis(finance_data):
    st.header("Data Analysis")

    if finance_data.empty:
        st.warning("No data available to analyze. Please add some income or expenses.")
        return

    # Ensure numerical columns are integers
    finance_data["Amount"] = finance_data["Amount"].astype(int)

    # Total Income vs. Total Expenses
    total_income = finance_data[finance_data["Amount"] > 0]["Amount"].sum()
    total_expense = finance_data[finance_data["Amount"] < 0]["Amount"].sum()
    net_balance = total_income + total_expense

    st.subheader("Summary")
    st.metric("Total Income", f"${total_income}")
    st.metric("Total Expenses", f"${abs(total_expense)}")
    st.metric("Net Balance", f"${net_balance}")

    # Income vs. Expense Chart
    st.subheader("Income vs. Expense")
    fig, ax = plt.subplots()
    ax.bar(["Income", "Expenses"], [total_income, abs(total_expense)], color=["green", "red"])
    ax.set_ylabel("Amount ($)")
    st.pyplot(fig)

    # Category Breakdown
    st.subheader("Category Breakdown")
    category_data = finance_data.groupby("Category")["Amount"].sum().sort_values()
    fig, ax = plt.subplots()
    category_data.plot.pie(
        autopct='%1.1f%%', startangle=90, ax=ax, legend=False, ylabel="",
        colors=plt.cm.Paired.colors[:len(category_data)]
    )
    st.pyplot(fig)

    # Time Series Analysis
    st.subheader("Trends Over Time")
    finance_data["Date"] = pd.to_datetime(finance_data["Date"])
    time_series = finance_data.groupby("Date")["Amount"].sum()
    fig, ax = plt.subplots()
    time_series.plot(ax=ax, marker='o', linestyle='-', color='blue')
    ax.set_title("Daily Net Amount")
    ax.set_ylabel("Net Amount ($)")
    st.pyplot(fig)

    st.success("Analysis complete!")
