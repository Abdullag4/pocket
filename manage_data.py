import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_manage_data(finance_data, db_file):
    st.title("Manage Data")

    # Ensure the Date column is properly formatted
    if "Date" in finance_data.columns:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

    # Add an index column explicitly
    editable_data = finance_data.reset_index(names="original_index")

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
        # Remove the index column before saving
        updated_data = updated_data.drop(columns=["original_index"], errors="ignore")
        finance_data = pd.DataFrame(updated_data)
        finance_data.to_csv(db_file, index=False)

        # Update session state and notify
        st.session_state["finance_data"] = finance_data
        st.success("Changes saved successfully!")

    # Remove selected row button
    if st.button("❌ Remove Selected Row"):
        if len(selected_rows) > 0:  # Check if any row is selected
            # Retrieve the original index of the selected row
            row_to_delete = selected_rows[0].get("original_index")

            if row_to_delete is not None:  # Ensure the index exists
                # Drop the row using the original index
                finance_data = finance_data.drop(index=row_to_delete).reset_index(drop=True)

                # Save changes to the file
                finance_data.to_csv(db_file, index=False)

                # Update session state and notify
                st.session_state["finance_data"] = finance_data
                st.success("Selected row removed successfully!")
            else:
                st.warning("No valid row index found for deletion.")
        else:
            st.warning("No row selected for deletion.")
