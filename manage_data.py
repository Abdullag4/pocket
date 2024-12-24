import streamlit as st
import pandas as pd

def show_manage_data(finance_data, db_file):
    st.title("Manage Data")

    # Ensure the Date column is properly formatted
    if "Date" in finance_data.columns:
        finance_data["Date"] = pd.to_datetime(finance_data["Date"], errors="coerce")

    # Editable DataFrame
    st.subheader("Edit Data")
    updated_data = st.experimental_data_editor(finance_data, use_container_width=True)

    # Save Changes Button
    if st.button("💾 Save Changes"):
        # Save the updated data to file
        updated_data.to_csv(db_file, index=False)

        # Update session state
        st.session_state["finance_data"] = updated_data

        st.success("Changes saved successfully!")

    # Dropdown for row deletion
    st.subheader("Delete a Row")

    # Ensure "index" column exists for dropdown options
    if "index" not in updated_data.columns:
        updated_data = updated_data.reset_index()

    row_options = [
        f"{row['index']}: {row.get('Date', 'N/A')} - {row.get('Category', 'N/A')} - {row.get('Amount', 'N/A')}"
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
