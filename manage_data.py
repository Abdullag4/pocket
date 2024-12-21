import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_manage_data(finance_data, db_file):
    st.title("Manage Financial Data")

    if finance_data.empty:
        st.info("No data available to manage.")
        return

    # Configure AgGrid for editing and selection
    grid_options = GridOptionsBuilder.from_dataframe(finance_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(editable=True)  # Enable inline editing
    grid_options.configure_selection("multiple", use_checkbox=True)  # Enable row selection

    # Display the data using AgGrid
    grid_response = AgGrid(
        finance_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        enable_enterprise_modules=False,
        height=400,
        fit_columns_on_grid_load=True,
        key="data_grid"
    )

    # Get selected rows
    selected_rows = grid_response.get("selected_rows", [])

    col1, col2 = st.columns(2)

    with col1:
        # Save changes button
        if st.button("💾 Save Changes"):
            updated_data = pd.DataFrame(grid_response["data"])
            save_data(updated_data, db_file)
            st.success("Changes saved successfully!")
            st.experimental_rerun()

    with col2:
        # Delete selected rows button
        if st.button("❌ Remove Selected Rows"):
            if selected_rows:
                indices_to_remove = [
                    row["_selectedRowNodeInfo"]["rowIndex"]
                    for row in selected_rows
                    if "_selectedRowNodeInfo" in row
                ]
                updated_data = finance_data.drop(indices_to_remove).reset_index(drop=True)
                save_data(updated_data, db_file)
                st.success("Selected rows removed successfully!")
                st.experimental_rerun()
            else:
                st.warning("No rows selected for deletion.")

    st.subheader("Current Data")
    st.dataframe(finance_data)

# Save data to the file
def save_data(finance_data, db_file):
    finance_data.to_csv(db_file, index=False)
