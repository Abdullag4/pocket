import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_manage_data(finance_data, db_file):
    st.title("Manage Data")

    # Ensure the Date column is properly formatted
    if "Date" in finance_data.columns:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

    # Create a copy of the DataFrame for editing
    editable_data = finance_data.copy()

    # Create grid options
    grid_options = GridOptionsBuilder.from_dataframe(editable_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(editable=True, wrapText=True)  # Enable editing
    grid_options.configure_selection('single', use_checkbox=True)  # Enable row selection with a checkbox

    # Render the grid
    grid_response = AgGrid(
        editable_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        enable_enterprise_modules=False,
        height=400,
    )

    # Get selected rows and the edited data
    selected_rows = grid_response["selected_rows"]
    updated_data = grid_response["data"]

    # Save changes button
    if st.button("💾 Save Changes"):
        # Save updated data to CSV
        finance_data = pd.DataFrame(updated_data)
        finance_data.to_csv(db_file, index=False)

        # Update session state and notify
        st.session_state["finance_data"] = finance_data
        st.success("Changes saved successfully!")

    # Remove selected row button
    if st.button("❌ Remove Selected Row"):
        if selected_rows:
            # Find the index of the selected row
            row_to_delete = selected_rows[0]
            row_to_delete_index = editable_data.index[
                (editable_data["Date"] == row_to_delete["Date"]) &
                (editable_data["Category"] == row_to_delete["Category"]) &
                (editable_data["Amount"] == row_to_delete["Amount"]) &
                (editable_data["Notes"] == row_to_delete["Notes"]) &
                (editable_data["Type"] == row_to_delete["Type"])
            ].tolist()

            if row_to_delete_index:
                # Drop the selected row(s)
                editable_data = editable_data.drop(row_to_delete_index).reset_index(drop=True)

                # Update session state and notify
                st.session_state["finance_data"] = editable_data
                st.success("Selected row removed successfully!")

                # Display the updated grid
                AgGrid(
                    editable_data,
                    gridOptions=grid_options.build(),
                    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                    update_mode=GridUpdateMode.MODEL_CHANGED,
                    enable_enterprise_modules=False,
                    height=400,
                )
            else:
                st.warning("Row index could not be determined for deletion.")
        else:
            st.warning("No row selected for deletion.")
