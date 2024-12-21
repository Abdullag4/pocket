import streamlit as st
import pandas as pd
from datetime import date

def show_debt_page(debt_data, db_file):
    st.title("💳 Debt Management")

    # Current Debts
    st.subheader("Current Debts")
    if debt_data.empty:
        st.info("No debts recorded.")
    else:
        st.dataframe(debt_data)

    # Add a New Debt
    st.subheader("Add a New Debt")
    with st.form("add_debt_form"):
        debt_type = st.selectbox("Type", ["Owe Me", "I Owe"])
        name = st.text_input("Name (e.g., Creditor or Debtor)")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        due_date = st.date_input("Due Date", min_value=date.today())
        reason = st.text_area("Reason")
        status = st.selectbox("Status", ["Pending", "Paid"])
        submitted = st.form_submit_button("Add Debt")

        if submitted:
            new_debt = {
                "Type": debt_type,
                "Name": name,
                "Amount": amount,
                "Due Date": due_date.strftime("%Y-%m-%d"),
                "Reason": reason,
                "Status": status,
            }
            # Update the debt data in session state and save to file
            st.session_state["debt_data"] = st.session_state["debt_data"].append(new_debt, ignore_index=True)
            st.session_state["debt_data"].to_csv(db_file, index=False)
            st.success("Debt added successfully!")
            st.experimental_rerun()  # Refresh the page to display changes

    # Remove Debts
    st.subheader("Remove a Debt")
    debts_to_remove = st.multiselect("Select debts to remove by index:", debt_data.index.tolist())
    if st.button("Remove Selected Debts"):
        if debts_to_remove:
            st.session_state["debt_data"].drop(debts_to_remove, inplace=True)
            st.session_state["debt_data"].to_csv(db_file, index=False)
            st.success("Selected debts removed successfully!")
            st.experimental_rerun()  # Refresh the page to display changes
        else:
            st.warning("No debts selected for removal.")
