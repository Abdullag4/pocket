import streamlit as st
import pandas as pd

# Function to display the Debt Management page
def show_debt_page(debt_data, debt_file):
    # Initialize session state for debt_data if it does not exist
    if "debt_data" not in st.session_state:
        st.session_state["debt_data"] = pd.DataFrame(columns=["Type", "Name", "Amount", "Due Date", "Reason", "State"])  # Replace with your columns

    # Validate that debt_data is a DataFrame
    if not isinstance(st.session_state["debt_data"], pd.DataFrame):
        st.error("Error: Debt data is not a valid DataFrame.")
        return

    # Display the existing debt data
    st.title("Debt Management")
    st.subheader("Existing Debt Records")
    if st.session_state["debt_data"].empty:
        st.write("No debt records found. Add a new record below.")
    else:
        st.dataframe(st.session_state["debt_data"])

    # Form to add new debt record
    st.subheader("Add New Debt Record")
    with st.form("add_debt_form"):
        name = st.text_input("Name", placeholder="Enter the name")
        amount = st.number_input("Amount", min_value=0.0, step=1.0)
        due_date = st.date_input("Due Date")
        submitted = st.form_submit_button("Add Debt")

        if submitted:
            if name and amount and due_date:
                # Create a new debt record
                new_debt = {"Name": name, "Amount": amount, "Due Date": str(due_date)}

                # Append the new record to the DataFrame
                st.session_state["debt_data"] = pd.concat(
                    [st.session_state["debt_data"], pd.DataFrame([new_debt])], ignore_index=True
                )

                st.success("New debt record added successfully!")
            else:
                st.error("Please fill in all fields before submitting.")

    # Option to save debt data to a file
    st.subheader("Save Debt Data")
    if st.button("Save to File"):
        try:
            st.session_state["debt_data"].to_csv(debt_file, index=False)
            st.success(f"Debt data saved to {debt_file} successfully!")
        except Exception as e:
            st.error(f"Error saving data: {e}")

# File to store the debt data
DEBT_FILE = "debt_data.csv"

# Run the Debt Management page
if __name__ == "__main__":
    show_debt_page(st.session_state.get("debt_data", pd.DataFrame()), DEBT_FILE)
