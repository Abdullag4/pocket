import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_analysis(finance_data):
    st.header("Data Analysis")

    if finance_data.empty:
        st.warning("No data available for analysis.")
        return

    # Group data by category
    category_data = finance_data.groupby("Category")["Amount"].sum()

    # Exclude categories with negative totals
    category_data = category_data[category_data > 0]

    # Display summary stats
    st.subheader("Category-wise Summary")
    st.dataframe(category_data)

    # Plot pie chart
    st.subheader("Category-wise Distribution")
    if category_data.empty:
        st.warning("No positive data available for the pie chart.")
    else:
        fig, ax = plt.subplots()
        category_data.plot.pie(
            ax=ax, autopct="%1.1f%%", startangle=90, ylabel="", colormap="viridis"
        )
        st.pyplot(fig)

    # Display other insights
    st.subheader("General Insights")
    total_income = finance_data[finance_data["Amount"] > 0]["Amount"].sum()
    total_expense = finance_data[finance_data["Amount"] < 0]["Amount"].sum()

    st.write(f"Total Income: ${total_income:,.2f}")
    st.write(f"Total Expenses: ${abs(total_expense):,.2f}")
    st.write(f"Net Savings: ${total_income + total_expense:,.2f}")
