import streamlit as st
import pandas as pd

def show_overview(finance_data):
    st.title("💼 Financial Overview")

    # Summary Statistics
    total_income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
    total_expense = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expense

    st.metric("Total Income", f"${total_income:.2f}")
    st.metric("Total Expense", f"${total_expense:.2f}")
    st.metric("Balance", f"${balance:.2f}")

    # Budget Tips
    st.subheader("💡 Budget Tips")
    if total_income > 0:
        needs_limit = total_income * 0.50  # 50% for needs
        wants_limit = total_income * 0.30  # 30% for wants
        savings_target = total_income * 0.20  # 20% for savings

        # Calculate spending in each category
        needs_expense = finance_data[finance_data["Category"] == "Needs"]["Amount"].sum()
        wants_expense = finance_data[finance_data["Category"] == "Wants"]["Amount"].sum()

        if needs_expense > needs_limit:
            st.warning(f"You're spending more on 'Needs' (${needs_expense:.2f}) than recommended (${needs_limit:.2f}). Consider cutting back.")
        if wants_expense > wants_limit:
            st.warning(f"You're spending more on 'Wants' (${wants_expense:.2f}) than recommended (${wants_limit:.2f}). Reassess non-essential expenses.")
        if balance < savings_target:
            st.info(f"You're saving less than the recommended 20%. Aim to save at least ${savings_target:.2f}.")

    # Show spending chart
    if not finance_data.empty:
        st.subheader("📊 Spending by Category")
        category_expense = finance_data[finance_data["Type"] == "Expense"].groupby("Category")["Amount"].sum()
        st.bar_chart(category_expense)

    # Notify if overspending
    st.subheader("🚨 Alerts")
    if balance < 0:
        st.error("You're overspending and your balance is negative! Adjust your expenses immediately.")
