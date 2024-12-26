import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import json
import os

SETTINGS_FILE = "expense_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    else:
        # Default settings in case the settings file is not available
        return {
            "grades": {
                "Most to Do": 50,
                "Good to Do": 30,
                "Nice to Do": 15,
                "Saving Target": 5,
            },
            "categories": {},
        }

def show_overview(finance_data):
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

    if finance_data.empty:
        st.info("No data available. Start adding expenses and incomes.")
    else:
        # Ensure the Date column is properly formatted
        if "Date" in finance_data.columns:
            finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

        st.subheader("📋 All Transactions")
        
        # Use AgGrid for displaying transactions with custom options
        grid_options = GridOptionsBuilder.from_dataframe(finance_data)
        grid_options.configure_pagination(paginationAutoPageSize=True)
        grid_options.configure_default_column(wrapText=True, autoHeight=True)
        grid_options.configure_column("Amount", type=["numericColumn"], precision=2)
        grid_options.configure_column("Date", type=["dateColumn", "customDateTimeFormat"], custom_format_string="yyyy-MM-dd")
        AgGrid(finance_data, gridOptions=grid_options.build(), height=400)

    # Calculate Metrics
    total_income = finance_data.loc[finance_data['Type'] == "Income", "Amount"].sum()
    total_expenses = finance_data.loc[finance_data['Type'] == "Expense", "Amount"].sum()
    net_balance = total_income - total_expenses

    # Display Metrics
    st.subheader("💹 Financial Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="💰 Total Income", value=f"${total_income:,.2f}")
    col2.metric(label="💸 Total Expenses", value=f"${total_expenses:,.2f}")
    col3.metric(label="📊 Net Balance", value=f"${net_balance:,.2f}")

    # Load settings for grade-based spending
    settings = load_settings()
    st.subheader("🚦 Spending by Grade")
    for grade, percentage in settings["grades"].items():
        grade_limit = total_income * (percentage / 100)
        grade_categories = [
            cat for cat, g in settings["categories"].items() if g == grade
        ]
        grade_expense = finance_data[
            finance_data["Category"].isin(grade_categories)
        ]["Amount"].sum() if grade_categories else 0.0

        st.metric(
            f"{grade} Spending",
            f"${grade_expense:,.2f}",
            f"Limit: ${grade_limit:,.2f}",
        )
        if grade_expense > grade_limit:
            st.warning(f"⚠️ You're overspending on '{grade}' categories!")

    # Display recommendations based on spending
    st.subheader("📝 Recommendations")
    for grade, percentage in settings["grades"].items():
        grade_limit = total_income * (percentage / 100)
        grade_categories = [
            cat for cat, g in settings["categories"].items() if g == grade
        ]
        grade_expense = finance_data[
            finance_data["Category"].isin(grade_categories)
        ]["Amount"].sum() if grade_categories else 0.0

        if grade_expense > grade_limit:
            st.write(f"- Reduce spending on '{grade}' categories such as {', '.join(grade_categories)}.")
        elif grade == "Saving Target" and grade_expense < grade_limit:
            st.write("- Increase contributions to your savings targets to meet your goals!")
