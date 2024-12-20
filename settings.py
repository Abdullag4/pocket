import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_settings(finance_data, db_file):
    st.markdown('<div class="section-title">Manage Data</div>', unsafe_allow_html=True)

    if finance_data.empty:
        st.info("No data available. Add some transactions first.")
        return

    st.subheader("Edit or Remove Transactions")

    # Configure the AgGrid table
    grid_options = GridOptionsBuilder.from_dataframe(finance_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(wrapText=True, editable=True)  # Enable inline editing
    grid_options.configure_selection('multiple', use_checkbox=True)  # Add checkboxes for row selection
    grid_options.configure_grid_options(domLayout='normal')

    # Add index column for easier identification
    finance_data.reset_index(inplace=True)

    # Display the AgGrid table
    grid_response = AgGrid(
        finance_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        enable_enterprise_modules=False,
        height=400
    )

    # Capture selected rows
    selected_rows = grid_response.get("selected_rows", [])

    # Buttons for saving changes and removing rows
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Changes"):
            # Save the updated data back to CSV
            pd.DataFrame(grid_response['data']).to_csv(db_file, index=False)
            st.success("Changes saved successfully!")
            st.experimental_rerun()  # Refresh the app to reflect changes

    with col2:
        if st.button("❌ Remove Selected Rows"):
            if len(selected_rows) > 0:  # Safely check if rows are selected
                # Use the index for deletion
                indices_to_remove = [row["index"] for row in selected_rows]
                updated_df = finance_data.drop(indices_to_remove).reset_index(drop=True)
                updated_df.to_csv(db_file, index=False)
                st.success("Selected rows removed successfully!")
                st.experimental_rerun()  # Refresh the app to reflect changes
            else:
                st.warning("No rows selected for deletion.")

    # Show the updated data
    st.subheader("Updated Transactions")
    st.write(finance_data.drop(columns=["index"]))
