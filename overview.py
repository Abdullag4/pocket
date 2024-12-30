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
    st.markdown(f'<div class="section-title">{_("Overview")}</div>', unsafe_allow_html=True)

    if finance_data.empty:
        st.info(_("No data available. Start adding expenses and incomes."))
    else:
        if "Date" in finance_data.columns:
            finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

        st.subheader(_("📋 All Transactions"))
        
        grid_options = GridOptionsBuilder.from_dataframe(finance_data)
        grid_options.configure_pagination(paginationAutoPageSize=True)
        grid_options.configure_default_column(wrapText=True, autoHeight=True)
        grid_options.configure_column("Amount", type=["numericColumn"], precision=2)
        grid_options.configure_column("Date", type=["dateColumn", "customDateTimeFormat"], custom_format_string="yyyy-MM-dd")
        AgGrid(finance_data, gridOptions=grid_options.build(), height=400)

    total_income = finance_data.loc[finance_data['Type'] == "Income", "Amount"].sum()
    total_expenses = finance_data.loc[finance_data['Type'] == "Expense", "Amount"].sum()
    net_balance = total_income - total_expenses

    st.subheader(_("💹 Financial Summary"))
    col1, col2, col3 = st.columns(3)
    col1.metric(label=_("💰 Total Income"), value=f"${total_income:,.2f}")
    col2.metric(label=_("💸 Total Expenses"), value=f"${total_expenses:,.2f}")
    col3.metric(label=_("📊 Net Balance"), value=f"${net_balance:,.2f}")

    settings = load_settings()

    if "categories" in settings and "grades" in settings:
        st.subheader(_("📊 Expense Breakdown by Classification"))

        expense_data = finance_data[finance_data['Type'] == "Expense"]
        classified_expenses = {grade: 0 for grade in settings["grades"]}
        for _, row in expense_data.iterrows():
            category = row.get("Category", _("Unclassified"))
            classification = settings["categories"].get(category, _("Unclassified"))
            if classification in classified_expenses:
                classified_expenses[classification] += row["Amount"]

        for grade, percentage in settings["grades"].items():
            allocated_budget = (percentage / 100) * total_income
            spent = classified_expenses.get(grade, 0)
            remaining = allocated_budget - spent

            if grade == _("Saving Target"):
                savings = net_balance
                savings_target = (percentage / 100) * total_income
                remaining_tolerance = savings_target - savings

                if savings < savings_target:
                    st.error(
                        _("⚠️ {saved:,.2f} saved, target {target:,.2f} "
                          "(remaining tolerance {tolerance:,.2f}).").format(
                              saved=savings, target=savings_target, tolerance=remaining_tolerance
                        )
                    )
                else:
                    st.success(
                        _("✅ {saved:,.2f} saved, target {target:,.2f} "
                          "(exceeding target by {exceed:,.2f}).").format(
                              saved=savings, target=savings_target, exceed=abs(remaining_tolerance)
                        )
                    )
            else:
                st.markdown(
                    _("### {grade}: {spent:,.2f} spent, "
                      "budgeted {budgeted:,.2f} "
                      "(remaining {remaining:,.2f})").format(
                          grade=grade, spent=spent, budgeted=allocated_budget, remaining=remaining
                    )
                )

                if remaining < 0:
                    st.warning(_("⚠️ You've overspent on {grade} by {overspent:,.2f}.").format(
                        grade=grade, overspent=-remaining))
                elif remaining > 0:
                    st.info(_("✅ You have {remaining:,.2f} left in your {grade} budget.").format(
                        grade=grade, remaining=remaining))
