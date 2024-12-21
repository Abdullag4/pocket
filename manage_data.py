import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode

def show_manage_data(finance_data, db_file):
    st.title("Manage Financial Data")

    if finance_data.empty:
        st.info("No data available to manage.")
        return

    # Configure AgGrid for editing
    grid_options = GridOptionsBuilder.from_dataframe(finance_data)
    grid_options.configure_pagination(paginationAutoPageSize=True)
    grid_options.configure_default_column(editable=True)  # Enable inline editing

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

    # Edit button
    if st.button("💾 Save Changes"):
        updated_data = pd.DataFrame(grid_response["data"])
        save_data(updated_data, db_file)
        st.success("Changes saved successfully!")
        st.experimental_rerun()

    # Row deletion
    st.subheader("Delete Rows")
    st.write("Provide the index or value of rows you want to delete:")

    # Allow user to input indices or column values for deletion
    delete_input = st.text_area(
        "Enter row indices (comma-separated, e.g., 0,2,5) or column values.",
        placeholder="Indices or values..."
    )
    delete_mode = st.radio("Delete by:", ["Index", "Column Value"], horizontal=True)

    if st.button("❌ Delete Rows"):
        try:
            if delete_input:
                if delete_mode == "Index":
                    indices_to_delete = [int(idx.strip()) for idx in delete_input.split(",")]
                    updated_data = finance_data.drop(indices_to_delete).reset_index(drop=True)
                else:  # Delete by column value
                    column_name = st.selectbox("Select column to match values:", finance_data.columns)
                    values_to_delete = [val.strip() for val in delete_input.split(",")]
                    updated_data = finance_data[~finance_data[column_name].isin(values_to_delete)]

                save_data(updated_data, db_file)
                st.success("Rows removed successfully!")
                st.experimental_rerun()
            else:
                st.warning("No input provided for deletion.")
        except Exception as e:
            st.error(f"Error during row removal: {str(e)}")

    st.subheader("Current Data")
    st.dataframe(finance_data)

# Save data to the file
def save_data(finance_data, db_file):
    finance_data.to_csv(db_file, index=False)
