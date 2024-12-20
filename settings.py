import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_settings(finance_data, db_file):
    st.markdown('<div class="section-title">Manage Data</div>', unsafe_allow_html=True)

    if finance_data.empty:
        st.info("No data available. Add some transactions first.")
        return

    st.subheader("Edit or Remove Transactions")

    # AgGrid Configuration for Editable Table
    grid_options = GridOptionsBuilder.from_dataframe(finance_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(wrapText=True, editable=True)  # Enable inline editing
    grid_options.configure_grid_options(domLayout='normal')

    # Display Editable Table
    grid_response = AgGrid(
        finance_data,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MANUAL,  # Allow manual updates
        enable_enterprise_modules=False,
        height=400
    )

    # Edited data from AgGrid
    updated_data = grid_response['data']

    # Buttons for Save and Delete
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Changes"):
            # Save the updated data back to CSV
            pd.DataFrame(updated_data).to_csv(db_file, index=False)
            st.success("Changes saved successfully!")
            st.experimental_rerun()  # Refresh the app to reflect changes

    with col2:
        if st.button("❌ Remove Selected Rows"):
            selected_rows = grid_response['selected_rows']
            if selected_rows:
                # Filter out selected rows to remove
                updated_df = finance_data[~finance_data.index.isin([row['_selectedRowNodeInfo']['nodeRowIndex'] for row in selected_rows])]
                updated_df.to_csv(db_file, index=False)
                st.success("Selected rows removed successfully!")
                st.experimental_rerun()
            else:
                st.warning("Please select rows to delete.")
