import pandas as pd

def apply_styles(data):
    try:
        # Convert numerical values to integers
        for col in data.select_dtypes(include=['float', 'int']).columns:
            data[col] = data[col].astype(int)

        # Apply highlighting styles
        styled_data = data.style.highlight_max(axis=0, props='color:white; background-color:green;') \
                             .highlight_min(axis=0, props='color:white; background-color:red;')
        return styled_data
    except Exception as e:
        print(f"Error applying styles: {e}")
        return data  # Return raw data if styling fails
