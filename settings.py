    # React to query parameters for refreshing
    query_params = st.query_params.to_dict()  # Convert query params to a dictionary
    if query_params.get("data_updated") == "true":
        st.query_params.clear()  # Clear the query parameters to reset
        # Trigger a re-render indirectly by setting a key in session state
        st.session_state["page_refreshed"] = True

    # After saving or removing rows, set the query param to trigger a refresh
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
