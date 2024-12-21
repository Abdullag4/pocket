import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

def show_overview(finance_data):
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

    if finance_data.empty:
        st.info("No data available. Start adding expenses and incomes.")
    else:
        # Ensure the Date column is properly formatted and sorted
        if "Date" in finance_data.columns:
            finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")
            finance_data = finance_data.sort_values(by="Date", ascending=False)

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
