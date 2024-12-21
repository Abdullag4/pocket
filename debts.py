import streamlit as st
import pandas as pd

def show_debt_page(debt_data, db_file):
    st.title("💳 Debt Management")
    st.subheader("Manage Your Debts")

    # Display current debts
    st.header("Current Debts")
    if debt_data.empty:
        st.info("No debts recorded. Add some debts to get started.")
    else:
        st.dataframe(debt_data)

    # Add a new debt
    st.subheader("Add a New Debt")
    with st.form("add_debt_form", clear_on_submit=True):
        debt_type = st.selectbox("Debt Type", ["Owe Someone", "Owed by Someone"])
        name = st.text_input("Name of Person/Entity")
        amount = st.number_input("Debt Amount", min_value=0.01, format="%.2f")
        due_date = st.date_input("Due Date")
        reason = st.text_area("Reason for Debt")
        status = st.selectbox("Status", ["Pending", "Paid"])
        submitted = st.form_submit_button("Add Debt")

        if submitted:
            if not name:
                st.warning("Please provide the name of the person/entity.")
            else:
                new_debt = pd.DataFrame(
                    [{
                        "Type": debt_type,
                        "Name": name,
                        "Amount": amount,
                        "Due Date": due_date,
                        "Reason": reason,
                        "Status": status,
                    }]
                )
                # Use pd.concat to append the new debt
                debt_data = pd.concat([debt_data, new_debt], ignore_index=True)
                debt_data.to_csv(db_file, index=False)
                st.success("Debt added successfully!")

    # Option to delete debts
    st.subheader("Delete Debts")
    indices_to_delete = st.multiselect(
        "Select rows to delete by index:",
        debt_data.index.tolist()
    )
    if st.button("Delete Selected Debts"):
        if indices_to_delete:
            debt_data = debt_data.drop(indices_to_delete).reset_index(drop=True)
            debt_data.to_csv(db_file, index=False)
            st.success("Selected debts removed successfully!")
        else:
            st.warning("No debts selected for deletion.")
