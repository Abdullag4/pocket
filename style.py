import pandas as pd

def apply_styles(df):
    """
    Apply styling to a DataFrame for visualization.
    Highlights positive values (income) in green and negative values (expenses) in red.
    """
    if df.empty:
        return df  # Return as-is if DataFrame is empty

    # Ensure 'Amount' column exists and is numeric
    if 'Amount' not in df.columns:
        raise ValueError("The DataFrame must contain an 'Amount' column for styling.")

    # Convert Amount column to numeric (coerce errors to NaN, replace NaN with 0)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

    # Apply styling to highlight values
    styled_df = df.style.applymap(
        lambda x: 'color: green; font-weight: bold' if x > 0 else 'color: red; font-weight: bold',
        subset=['Amount']
    )
    return styled_df
