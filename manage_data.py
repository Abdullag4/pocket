import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_manage_data(finance_data, db_file):
    st.title("Manage Data")

    # Ensure the Date column is properly formatted
    if "Date" in finance_data.columns:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

    # Editable data grid
    st.subheader("Edit Data")
    editable_data = finance_data.copy()

    # Add an "index" column for row identification
    editable_data.reset_index(inplace=True)

    # Grid configuration for editing
    grid_options = GridOptionsBuilder.from_dataframe(editable_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(editable=True, wrapText=True)  # Enable editing
    grid_options.configure_selection("single", use_checkbox=True)  # Allow single row selection
    grid_response = AgGrid(
        editable_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        enable_enterprise_modules=False,
        height=400,
    )

    # Updated data from the grid
    updated_data = pd.DataFrame(grid_response["data"])

    # Save changes button
    if st.button("💾 Save Changes"):
        # Remove the "index" column before saving
        updated_data = updated_data.drop(columns=["index"], errors="ignore")
        finance_data = updated_data.copy()

        # Save updated data to the file
        finance_data.to_csv(db_file, index=False)

        # Update session state and notify user
        st.session_state["finance_data"] = finance_data
        st.success("Changes saved successfully!")

    # Dropdown for row deletion
    st.subheader("Delete a Row")
    row_options = [
        f"{row['index']}: {row['Date']} - {row['Category']} - {row['Amount']}"
        for _, row in updated_data.iterrows()
    ]
    selected_row = st.selectbox(
        "Select a row to delete:",
        options=row_options if row_options else ["No rows available"],
    )

    # Deletion button
    if st.button("❌ Remove Selected Row"):
        if "No rows available" in row_options:
            st.warning("No rows to delete!")
        else:
            # Extract row index
            row_index = int(selected_row.split(":")[0])

            # Remove the selected row
            updated_data = updated_data[updated_data["index"] != row_index].reset_index(drop=True)

            # Remove the "index" column before saving
            updated_data = updated_data.drop(columns=["index"], errors="ignore")
            finance_data = updated_data.copy()

            # Save updated data to the file
            finance_data.to_csv(db_file, index=False)

            # Update session state
            st.session_state["finance_data"] = finance_data

            st.success("Selected row deleted successfully!")
