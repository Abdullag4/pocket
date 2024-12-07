import streamlit as st
import pandas as pd

# Sample structure for financial data
st.title("Monthly Finance Manager")

# Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Menu", ["Overview", "Add Expense", "Add Income", "Settings"])

# Placeholder for storing data
if "finance_data" not in st.session_state:
    st.session_state["finance_data"] = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Notes"])

finance_data = st.session_state["finance_data"]

# Overview Page
if menu == "Overview":
    st.header("Overview")
    if not finance_data.empty:
        st.subheader("Transaction History")
        st.dataframe(finance_data)

        st.subheader("Summary")
        total_income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
        total_expenses = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
        balance = total_income - total_expenses

        st.write(f"**Total Income:** ${total_income}")
        st.write(f"**Total Expenses:** ${total_expenses}")
        st.write(f"**Balance:** ${balance}")
    else:
        st.info("No transactions added yet. Use the menu to add income or expenses.")

# Add Expense Page
elif menu == "Add Expense":
    st.header("Add Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.text_input("Category (e.g., Food, Rent, Utilities)")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = {
            "Date": date.strftime("%Y-%m-%d"),
            "Type": "Expense",
            "Category": category,
            "Amount": -amount,
            "Notes": notes
        }
        finance_data = finance_data.append(new_data, ignore_index=True)
        st.session_state["finance_data"] = finance_data
        st.success("Expense added successfully!")

# Add Income Page
elif menu == "Add Income":
    st.header("Add Income")
    with st.form("income_form"):
        date = st.date_input("Date")
        category = st.text_input("Category (e.g., Salary, Investment)")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Income")

    if submitted:
        new_data = {
            "Date": date.strftime("%Y-%m-%d"),
            "Type": "Income",
            "Category": category,
            "Amount": amount,
            "Notes": notes
        }
        finance_data = finance_data.append(new_data, ignore_index=True)
        st.session_state["finance_data"] = finance_data
        st.success("Income added successfully!")

# Settings Page
elif menu == "Settings":
    st.header("Settings")
    clear = st.button("Clear All Data")
    if clear:
        st.session_state["finance_data"] = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Notes"])
        st.success("All data cleared!")

