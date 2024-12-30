import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import json
import os
from localization import _

SETTINGS_FILE = "expense_settings.json"

# Load classification settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    else:
        # Default fallback settings if file doesn't exist
        return {
            "grades": {
                "Most to Do": 50,
                "Good to Do": 30,
                "Nice to Do": 15,
                "Saving Target": 5,
            },
            "categories": {}
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
    st.subheader(_("💹 Financial Summary"))
    col1, col2, col3 = st.columns(3)
    col1.metric(label="💰 Total Income", value=f"${total_income:,.2f}")
    col2.metric(label="💸 Total Expenses", value=f"${total_expenses:,.2f}")
    col3.metric(label="📊 Net Balance", value=f"${net_balance:,.2f}")

    # Load settings for classifications
    settings = load_settings()

    # Classification-based expense summary
    if "categories" in settings and "grades" in settings:
        st.subheader("📊 Expense Breakdown by Classification")

        # Filter expense rows
        expense_data = finance_data[finance_data['Type'] == "Expense"]

        # Summarize expenses by classification
        classified_expenses = {grade: 0 for grade in settings["grades"]}
        for _, row in expense_data.iterrows():
            category = row.get("Category", "Unclassified")
            classification = settings["categories"].get(category, "Unclassified")
            if classification in classified_expenses:
                classified_expenses[classification] += row["Amount"]

        # Display classification summary
        for grade, percentage in settings["grades"].items():
            allocated_budget = (percentage / 100) * total_income
            spent = classified_expenses.get(grade, 0)
            remaining = allocated_budget - spent

            if grade == "Saving Target":
                # Calculate savings
                savings = net_balance  # Remaining balance after all spending
                savings_target = (percentage / 100) * total_income
                remaining_tolerance = savings_target - savings

                if savings < savings_target:
                    st.error(
                        f"⚠️ {savings:,.2f} saved, target {savings_target:,.2f} "
                        f"(remaining tolerance {remaining_tolerance:,.2f})."
                    )
                else:
                    st.success(
                        f"✅ {savings:,.2f} saved, target {savings_target:,.2f} "
                        f"(exceeding target by {abs(remaining_tolerance):,.2f})."
                    )
            else:
                st.markdown(
                    f"### {grade}: {spent:,.2f} spent, "
                    f"budgeted {allocated_budget:,.2f} "
                    f"(remaining {remaining:,.2f})"
                )

                if remaining < 0:
                    st.warning(f"⚠️ You've overspent on {grade} by {-remaining:,.2f}.")
                elif remaining > 0:
                    st.info(f"✅ You have {remaining:,.2f} left in your {grade} budget.")
