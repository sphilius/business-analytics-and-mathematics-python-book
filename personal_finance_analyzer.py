import pandas as pd
import matplotlib.pyplot as plt
import argparse

def load_finance_data(csv_path):
    """
    Loads financial data from a CSV file.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded data as a DataFrame.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: File not found at {csv_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file at {csv_path} is empty.")
        return None
    except Exception as e:
        print(f"Error reading CSV file at {csv_path}: {e}")
        return None

    required_cols = ['Date', 'Description', 'Amount']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {', '.join(missing_cols)}")
        return None

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

    # Drop rows where Date could not be parsed
    df.dropna(subset=['Date'], inplace=True)

    return df

def calculate_summary_stats(df):
    """
    Calculates and prints summary financial statistics.
    """
    # For now, assume Amount > 0 is income, Amount < 0 is expense.
    # This can be adapted if a 'Type' column (income/expense) exists.
    if 'Type' in df.columns:
        # Example: income_df = df[df['Type'].str.lower() == 'income']
        # expenses_df = df[df['Type'].str.lower() == 'expense']
        # total_income = income_df['Amount'].sum()
        # total_expenses = expenses_df['Amount'].sum() # Assuming expenses are positive in this case
        # For now, we'll stick to the single 'Amount' column logic
        print("Note: 'Type' column detected. Current version uses positive/negative 'Amount' for income/expense. Future versions could adapt.")
        total_income = df[df['Amount'] > 0]['Amount'].sum()
        total_expenses = df[df['Amount'] < 0]['Amount'].sum() * -1 # Make expenses positive
    else:
        total_income = df[df['Amount'] > 0]['Amount'].sum()
        total_expenses = df[df['Amount'] < 0]['Amount'].sum() * -1 # Make expenses positive

    net_savings = total_income - total_expenses

    print("\n--- Summary Statistics ---")
    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expenses: {total_expenses:.2f}")
    print(f"Net Savings: {net_savings:.2f}")
    print("-------------------------\n")

# Define a global keyword mapping for easy extension
KEYWORD_CATEGORIES = {
    'Groceries': ['grocery', 'supermarket', 'market', 'food lion', 'trader joe', 'walmart'],
    'Transport': ['uber', 'lyft', 'taxi', 'gas', 'fuel', 'metro', 'subway', 'bus'],
    'Utilities': ['bill', 'electricity', 'water', 'internet', 'phone', 'gas com'],
    'Dining': ['restaurant', 'cafe', 'dinner', 'lunch', 'brunch', 'starbucks'],
    'Shopping': ['amazon', 'store', 'shop', 'clothing', 'electronics'],
    'Healthcare': ['pharmacy', 'doctor', 'hospital', 'clinic'],
    'Entertainment': ['movie', 'concert', 'show', 'game'],
    'Travel': ['flight', 'hotel', 'airbnb', 'booking'],
    'Rent/Mortgage': ['rent', 'mortgage'],
    'Income': ['salary', 'deposit', 'paycheck'] # To exclude from expense categorization
}

def infer_category(description, amount):
    """Helper function to infer category based on description keywords."""
    if amount > 0: # Skip categorization for income
        return 'Income'
    description_lower = str(description).lower()
    for category, keywords in KEYWORD_CATEGORIES.items():
        if any(keyword in description_lower for keyword in keywords):
            if category == 'Income': # Ensure income keywords are only for positive amounts
                return 'Income' if amount > 0 else 'Miscellaneous Expense'
            return category
    return 'Miscellaneous Expense'

def analyze_spending_by_category(df, category_col='Category'):
    """
    Analyzes spending by category and generates a bar chart.
    """
    if df is None or df.empty:
        print("No data available for category analysis.")
        return

    expenses_df = df[df['Amount'] < 0].copy() # Work with expenses only
    if expenses_df.empty:
        print("No expense data available for category analysis.")
        return

    # Determine which category column to use
    use_inferred_category = False
    cat_col_to_use = category_col

    if category_col not in expenses_df.columns or expenses_df[category_col].isnull().sum() > 0.7 * len(expenses_df):
        print(f"'{category_col}' column is missing or largely empty. Attempting to infer categories from 'Description'.")
        expenses_df['InferredCategory'] = expenses_df.apply(lambda row: infer_category(row['Description'], row['Amount']), axis=1)
        expenses_df = expenses_df[expenses_df['InferredCategory'] != 'Income'] # Ensure income is not treated as expense category
        cat_col_to_use = 'InferredCategory'
        if expenses_df[cat_col_to_use].nunique() == 0 or \
           (expenses_df[cat_col_to_use].nunique() == 1 and expenses_df[cat_col_to_use].iloc[0] == 'Miscellaneous Expense'):
            print("Could not infer meaningful categories from descriptions for expense analysis.")
            # Optionally, could proceed without category breakdown or return
            # For now, let's print a message and proceed if there's any data.
            # If 'Miscellaneous Expense' is the only one, it will be plotted.
            if expenses_df[cat_col_to_use].nunique() == 0 :
                 print("No categories found or inferred for spending analysis.")
                 return
        use_inferred_category = True
    else:
        # Exclude 'Income' category from expense analysis if it exists in the original category column
        if 'income' in expenses_df[cat_col_to_use].str.lower().unique():
            expenses_df = expenses_df[~expenses_df[cat_col_to_use].str.lower().isin(['income'])]

    if cat_col_to_use not in expenses_df.columns:
        print(f"Error: Category column '{cat_col_to_use}' not found for analysis after inference/selection process.")
        return

    if expenses_df.empty or expenses_df[cat_col_to_use].nunique() == 0:
        print(f"No expense data available for category '{cat_col_to_use}' analysis after filtering.")
        return

    # Calculate spending: make amounts positive for summing expenses
    spending_by_cat = expenses_df.groupby(cat_col_to_use)['Amount'].sum().abs().sort_values(ascending=False)

    print("\n--- Spending By Category ---")
    if use_inferred_category:
        print("(Categories were inferred from descriptions)")
    print(spending_by_cat)
    print("---------------------------\n")

    # Generate and save bar chart
    if not spending_by_cat.empty:
        plt.figure(figsize=(10, 7))
        spending_by_cat.plot(kind='bar', color='skyblue')
        plt.title(f'Spending by {"Inferred " if use_inferred_category else ""}Category')
        plt.xlabel('Category')
        plt.ylabel('Total Spending ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        try:
            plt.savefig('spending_by_category.png')
            print("Bar chart 'spending_by_category.png' saved successfully.")
        except Exception as e:
            print(f"Error saving spending by category chart: {e}")
        plt.close()
    else:
        print("No data to plot for spending by category.")


def analyze_monthly_trends(df):
    """
    Analyzes monthly financial trends and generates line charts.
    """
    if df is None or df.empty:
        print("No data available for monthly trend analysis.")
        return

    monthly_df = df.copy()
    monthly_df['YearMonth'] = monthly_df['Date'].dt.to_period('M')

    # Separate income and expenses
    monthly_df['Income'] = monthly_df[monthly_df['Amount'] > 0]['Amount']
    monthly_df['Expenses'] = monthly_df[monthly_df['Amount'] < 0]['Amount'].abs() # Expenses as positive values

    # Group by YearMonth and sum income and expenses
    monthly_summary = monthly_df.groupby('YearMonth').agg(
        TotalIncome=('Income', 'sum'),
        TotalExpenses=('Expenses', 'sum')
    ).reset_index()

    monthly_summary['NetSavings'] = monthly_summary['TotalIncome'] - monthly_summary['TotalExpenses']
    # Convert Period to string for printing and plotting if necessary, or use as Period object
    monthly_summary['YearMonth'] = monthly_summary['YearMonth'].astype(str)


    print("\n--- Monthly Trends ---")
    print(monthly_summary)
    print("----------------------\n")

    # Generate and save line charts
    if not monthly_summary.empty:
        plt.figure(figsize=(12, 8))

        plt.subplot(3, 1, 1) # 3 rows, 1 column, 1st subplot
        plt.plot(monthly_summary['YearMonth'], monthly_summary['TotalIncome'], marker='o', color='green', label='Total Income')
        plt.title('Monthly Income')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.legend()

        plt.subplot(3, 1, 2) # 3 rows, 1 column, 2nd subplot
        plt.plot(monthly_summary['YearMonth'], monthly_summary['TotalExpenses'], marker='o', color='red', label='Total Expenses')
        plt.title('Monthly Expenses')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.legend()

        plt.subplot(3, 1, 3) # 3 rows, 1 column, 3rd subplot
        plt.plot(monthly_summary['YearMonth'], monthly_summary['NetSavings'], marker='o', color='blue', label='Net Savings')
        plt.title('Monthly Net Savings')
        plt.xlabel('Year-Month')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        try:
            plt.savefig('monthly_trends.png')
            print("Line chart 'monthly_trends.png' saved successfully.")
        except Exception as e:
            print(f"Error saving monthly trends chart: {e}")
        plt.close()
    else:
        print("No data to plot for monthly trends.")


def main():
    """
    Main function to orchestrate the financial analysis.
    """
    parser = argparse.ArgumentParser(description="Personal Finance Analyzer")
    parser.add_argument("csv_file", help="Path to the CSV file containing financial data.")
    args = parser.parse_args()

    df = load_finance_data(args.csv_file)

    if df is None:
        print("Failed to load or validate financial data. Exiting.")
        return # Or import sys; sys.exit(1)

    calculate_summary_stats(df)
    analyze_spending_by_category(df) # Default category_col is 'Category'
    analyze_monthly_trends(df)

if __name__ == "__main__":
    main()
