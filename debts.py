import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

# Debt Management Page
def show_debt_page(debt_data, db_file):
    st.title("Debt Management")

    # Section: Summary
    st.header("Debt Summary")
    total_owed = debt_data[debt_data["Type"] == "Owed"]["Amount"].sum()
    total_owing = debt_data[debt_data["Type"] == "Owing"]["Amount"].sum()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Owed", f"${total_owed:,.2f}")
    with col2:
        st.metric("Total Owing", f"${total_owing:,.2f}")

    # Section: Add New Debt
    st.header("Add New Debt")
    with st.form("add_debt_form", clear_on_submit=True):
        debt_type = st.selectbox("Debt Type", ["Owed", "Owing"])
        name = st.text_input("Name (Person/Entity)")
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        due_date = st.date_input("Due Date")
        reason = st.text_area("Reason for Debt")
        submit = st.form_submit_button("Add Debt")

        if submit:
            new_debt = {
                "Type": debt_type,
                "Name": name,
                "Amount": amount,
                "Due Date": str(due_date),
                "Reason": reason,
                "Status": "Active"
            }
            debt_data = debt_data.append(new_debt, ignore_index=True)
            save_data(debt_data, db_file)
            st.success("New debt added successfully!")
            st.experimental_rerun()

    # Section: Manage Debts
    st.header("Manage Debts")
    grid_options = GridOptionsBuilder.from_dataframe(debt_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(editable=True)
    grid_options.configure_selection("multiple", use_checkbox=True)

    grid_response = AgGrid(
        debt_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        enable_enterprise_modules=False,
        height=400
    )

    # Capture updated data
    updated_data = pd.DataFrame(grid_response["data"])

    # Save changes button
    if st.button("💾 Save Changes"):
        save_data(updated_data, db_file)
        st.success("Changes saved successfully!")
        st.experimental_rerun()

    # Mark debts as paid
    st.subheader("Mark Debts as Paid")
    selected_rows = grid_response.get("selected_rows", [])
    if st.button("Mark as Paid"):
        if selected_rows:
            indices_to_remove = [
                row["_selectedRowNodeInfo"]["rowIndex"]
                for row in selected_rows
                if "_selectedRowNodeInfo" in row
            ]
            updated_data.loc[indices_to_remove, "Status"] = "Paid"
            save_data(updated_data, db_file)
            st.success("Selected debts marked as paid!")
            st.experimental_rerun()
        else:
            st.warning("No rows selected.")

    # Show current debts
    st.header("All Debts")
    st.dataframe(debt_data)


# Save data to file
def save_data(data, db_file):
    data.to_csv(db_file, index=False)
