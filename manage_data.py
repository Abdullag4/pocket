import streamlit as st
import pandas as pd

def show_manage_data(finance_data, db_file):
    st.title("Manage Data")

    # Ensure the Date column is properly formatted
    if "Date" in finance_data.columns:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

    # Display current data as a table
    st.subheader("Current Data")
    st.dataframe(finance_data)

    # Dropdown to select a row to delete based on a unique column or content
    st.subheader("Delete a Row")
    row_options = [
        f"{index}: {row['Date']} - {row['Category']} - {row['Amount']}"
        for index, row in finance_data.iterrows()
    ]
    
    selected_row = st.selectbox(
        "Select a row to delete:", 
        options=row_options if row_options else ["No rows available"],
    )

    # Confirm deletion
    if st.button("❌ Delete Selected Row"):
        if "No rows available" in row_options:
            st.warning("No rows to delete!")
        else:
            # Extract the row index from the selected option
            row_index = int(selected_row.split(":")[0])

            # Delete the row
            finance_data = finance_data.drop(index=row_index).reset_index(drop=True)

            # Save updated data to file
            finance_data.to_csv(db_file, index=False)

            # Update session state
            st.session_state["finance_data"] = finance_data

            st.success("Selected row deleted successfully!")

    # Save changes after editing
    st.subheader("Edit Data")
    updated_data = st.experimental_data_editor(finance_data, use_container_width=True)

    if st.button("💾 Save Changes"):
        # Save the edited data
        updated_data.to_csv(db_file, index=False)

        # Update session state
        st.session_state["finance_data"] = updated_data

        st.success("Changes saved successfully!")
