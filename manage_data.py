import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_manage_data(finance_data, db_file):
    st.title("Manage Data")

    # Ensure the Date column is properly formatted
    if "Date" in finance_data.columns:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

    # Display the current data in an editable grid
    st.subheader("Edit or Remove Transactions")

    # Create grid options
    grid_options = GridOptionsBuilder.from_dataframe(finance_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(editable=True, wrapText=True)  # Enable editing
    grid_options.configure_selection('single', use_checkbox=True)  # Allow single-row selection with checkbox

    # Render AgGrid
    grid_response = AgGrid(
        finance_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.NO_UPDATE,
        enable_enterprise_modules=False,
        height=400,
    )

    # Capture the selected row(s)
    selected_rows = grid_response["selected_rows"]

    # Delete selected rows
    if st.button("❌ Remove Selected Row"):
        if selected_rows:
            # Get the index of the selected row from the `_selectedRowNodeInfo`
            row_indices = [
                row["_selectedRowNodeInfo"]["rowIndex"]
                for row in selected_rows
                if "_selectedRowNodeInfo" in row
            ]

            # Drop the selected rows from the DataFrame
            updated_data = finance_data.drop(index=row_indices).reset_index(drop=True)

            # Save the updated data back to the file
            updated_data.to_csv(db_file, index=False)

            # Update session state and display success
            st.session_state["finance_data"] = updated_data
            st.success("Selected row(s) removed successfully!")

            # Refresh the page to reflect the change
            st.experimental_rerun()
        else:
            st.warning("No row selected for deletion.")
