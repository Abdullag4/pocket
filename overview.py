import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

def show_overview(finance_data):
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

    if finance_data.empty:
        st.info("No data available. Start adding expenses and incomes.")
    else:
        st.subheader("📋 All Transactions")
        grid_options = GridOptionsBuilder.from_dataframe(finance_data)
        grid_options.configure_pagination(paginationAutoPageSize=True)
        grid_options.configure_default_column(wrapText=True)
        AgGrid(finance_data, gridOptions=grid_options.build(), height=400)

    # Metrics
    total_income = finance_data.loc[finance_data['Type'] == "Income", "Amount"].sum()
    total_expenses = finance_data.loc[finance_data['Type'] == "Expense", "Amount"].sum()
    net_balance = total_income + total_expenses  # Expenses are negative
    st.metric(label="💰 Total Income", value=f"${total_income:,.2f}")
    st.metric(label="💸 Total Expenses", value=f"${-total_expenses:,.2f}")
    st.metric(label="📊 Net Balance", value=f"${net_balance:,.2f}")
