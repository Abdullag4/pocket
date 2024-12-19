from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

def show_overview(finance_data):
    st.title("Overview")

    # Interactive AgGrid table
    st.subheader("Financial Data")
    gb = GridOptionsBuilder.from_dataframe(finance_data)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()  # Add a sidebar for filtering
    gb.configure_default_column(editable=True, sortable=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        finance_data,
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        update_mode="MODEL_CHANGED",
        fit_columns_on_grid_load=True,
        theme="alpine",  # Other options: 'streamlit', 'balham', 'material'
    )

    # Summary Statistics
    st.subheader("Summary")
    total_expense = finance_data.loc[finance_data["Type"] == "Expense", "Amount"].sum()
    total_income = finance_data.loc[finance_data["Type"] == "Income", "Amount"].sum()
    balance = total_income + total_expense  # Expenses are negative

    st.metric("Total Income", f"${total_income:,.2f}")
    st.metric("Total Expense", f"${total_expense:,.2f}")
    st.metric("Balance", f"${balance:,.2f}")

    st.success("Overview loaded successfully!")
