import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def show_analysis(finance_data):
    st.title("📊 Analyze Your Finances")

    tab1, tab2, tab3 = st.tabs(["📉 Expense Analysis", "💹 Income Analysis", "📈 Trends Overview"])

    with tab1:
        st.subheader("Expenses Breakdown")
        # Add your expense charts and insights here

    with tab2:
        st.subheader("Income Breakdown")
        # Add your income charts and insights here

    with tab3:
        st.subheader("Trends and Summary")
        # Add trend analysis charts and data

def show_analysis(finance_data):
    st.title("Analyze Your Data")

    # Separate data
    expense_data = finance_data[finance_data["Type"] == "Expense"]
    income_data = finance_data[finance_data["Type"] == "Income"]

    # Pie Chart for Expenses
    st.subheader("Expense Analysis")
    if not expense_data.empty:
        category_expense_data = expense_data.groupby("Category")["Amount"].sum()
        category_expense_data = category_expense_data[category_expense_data > 0]  # Exclude negative values
        if not category_expense_data.empty:
            fig1, ax1 = plt.subplots()
            category_expense_data.plot.pie(
                autopct="%1.1f%%", startangle=90, ax=ax1, ylabel=""
            )
            st.pyplot(fig1)
        else:
            st.info("No valid expense data available for the pie chart.")
    else:
        st.info("No expense data available.")

    # Pie Chart for Incomes
    st.subheader("Income Analysis")
    if not income_data.empty:
        category_income_data = income_data.groupby("Category")["Amount"].sum()
        category_income_data = category_income_data[category_income_data > 0]  # Exclude negative values
        if not category_income_data.empty:
            fig2, ax2 = plt.subplots()
            category_income_data.plot.pie(
                autopct="%1.1f%%", startangle=90, ax=ax2, ylabel=""
            )
            st.pyplot(fig2)
        else:
            st.info("No valid income data available for the pie chart.")
    else:
        st.info("No income data available.")

    # Trends Chart
    st.subheader("Trends Over Time")
    if not finance_data.empty:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors='coerce')
        trends_data = finance_data.groupby(["Date", "Type"])["Amount"].sum().unstack(fill_value=0)
        trends_data = trends_data.clip(lower=0)  # Ensure no negative values in trends
        if not trends_data.empty:
            st.line_chart(trends_data)
        else:
            st.info("No valid data for trends.")
    else:
        st.info("No data available for trends.")
