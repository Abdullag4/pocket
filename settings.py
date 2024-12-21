def show_settings(finance_data, db_file):
    # Layout for settings page
    st.title("Manage Data")
    
    # Editable data grid
    grid_response = AgGrid(
        finance_data,
        editable=True,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        height=400,
        theme="streamlit",
        key="data_grid"
    )
    selected_rows = grid_response.get("selected_rows", [])

    # React to query parameters for refreshing
    query_params = st.query_params.to_dict()  # Convert query params to a dictionary
    if query_params.get("data_updated") == "true":
        st.query_params.clear()  # Clear the query parameters to reset
        st.session_state["page_refreshed"] = True

    # After saving or removing rows, set the query param to trigger a refresh
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Changes"):
            pd.DataFrame(grid_response['data']).to_csv(db_file, index=False)
            st.success("Changes saved successfully!")
            st.query_params.data_updated = "true"

    with col2:
        if st.button("❌ Remove Selected Rows"):
            if len(selected_rows) > 0:
                indices_to_remove = [
                    row["_selectedRowNodeInfo"]["rowIndex"]
                    for row in selected_rows
                    if "_selectedRowNodeInfo" in row
                ]
                updated_df = finance_data.drop(indices_to_remove).reset_index(drop=True)
                updated_df.to_csv(db_file, index=False)
                st.success("Selected rows removed successfully!")
                st.query_params.data_updated = "true"
            else:
                st.warning("No rows selected for deletion.")
