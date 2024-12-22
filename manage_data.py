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

    grid_options = GridOptionsBuilder.from_dataframe(finance_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(editable=True, wrapText=True)  # Enable editing
    grid_options.configure_selection('single', use_checkbox=True)  # Allow selecting rows

    grid_response = AgGrid(
        finance_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        enable_enterprise_modules=False,
        height=400,
    )

    # Update the data if edited in the grid
    updated_data = grid_response["data"]
    updated_df = pd.DataFrame(updated_data)

    # Show updated dataframe in the app
    st.subheader("Updated Data Preview")
    st.dataframe(updated_df)

    # Save changes
    if st.button("💾 Save Changes"):
        try:
            updated_df.to_csv(db_file, index=False)
            st.success("Changes saved successfully!")
        except Exception as e:
            st.error("Failed to save changes.")
            st.write(f"Error details: {e}")

    # Delete selected rows
    selected_rows = grid_response["selected_rows"]
    if st.button("❌ Remove Selected Row"):
        if selected_rows:
            indices_to_remove = [
                row["_selectedRowNodeInfo"]["rowIndex"]
                for row in selected_rows
                if "_selectedRowNodeInfo" in row
            ]
            updated_df = updated_df.drop(indices_to_remove).reset_index(drop=True)
            updated_df.to_csv(db_file, index=False)
            st.success("Selected row removed successfully!")
            st.experimental_rerun()  # Refresh the app to show the updated data
        else:
            st.warning("No row selected for deletion.")
