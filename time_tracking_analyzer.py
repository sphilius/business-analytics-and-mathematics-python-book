import pandas as pd
import matplotlib.pyplot as plt
import argparse

def load_time_data(csv_path):
    """
    Loads time tracking data from a CSV file.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded data as a DataFrame.
                          Returns None if essential columns are missing or file not found.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: File not found at {csv_path}")
        return None, None
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file at {csv_path} is empty.")
        return None, None
    except Exception as e:
        print(f"Error reading CSV file at {csv_path}: {e}")
        return None, None

    # Essential columns check
    required_cols = ['Date', 'Duration']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {', '.join(missing_cols)}")
        return None, None

    # Project/Task column detection and validation
    project_col_options = ['Project', 'Task']
    project_col_name = None
    for col_option in project_col_options:
        if col_option in df.columns:
            project_col_name = col_option
            break

    if not project_col_name:
        print(f"Error: Missing one of the required project/task columns: {', '.join(project_col_options)}. At least one must be present.")
        return None, None

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    # Assume Duration is a numeric value in hours. Add a note if conversion is needed.
    print("Note: Assuming 'Duration' column is in hours. If it's in minutes or other formats, please convert it to hours (numeric) in the CSV.")
    df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')

    # Drop rows where essential conversions failed (Date or Duration)
    df.dropna(subset=['Date', 'Duration'], inplace=True)

    if df.empty:
        print("No valid data remaining after handling missing values or conversion errors.")
        return None, None

    return df, project_col_name

def calculate_summary_stats(df):
    """
    Calculates and prints summary time tracking statistics.
    """
    if df is None or df.empty:
        print("No data available for summary statistics.")
        return

    total_time_tracked = df['Duration'].sum()
    date_range_start = df['Date'].min().strftime('%Y-%m-%d')
    date_range_end = df['Date'].max().strftime('%Y-%m-%d')

    # Number of unique days with entries
    num_unique_days = df['Date'].nunique()
    average_time_per_day = total_time_tracked / num_unique_days if num_unique_days > 0 else 0

    print("\n--- Summary Statistics ---")
    print(f"Total Time Tracked: {total_time_tracked:.2f} hours")
    print(f"Date Range: {date_range_start} to {date_range_end}")
    print(f"Number of Days with Entries: {num_unique_days}")
    print(f"Average Time Tracked per Day: {average_time_per_day:.2f} hours/day")
    print("-------------------------\n")

def analyze_time_allocation(df, main_group_col):
    """
    Analyzes time allocation by a specified column (e.g., Project, Task, Category).
    Generates a bar chart of the time allocation.
    """
    if df is None or df.empty:
        print("No data available for time allocation analysis.")
        return

    if main_group_col not in df.columns:
        print(f"Error: Grouping column '{main_group_col}' not found for time allocation analysis.")
        return

    time_by_group = df.groupby(main_group_col)['Duration'].sum().sort_values(ascending=False)

    if time_by_group.empty:
        print(f"No time data found for any groups in column '{main_group_col}'.")
        return

    print(f"\n--- Time Allocation by {main_group_col} ---")
    print(time_by_group)
    print("---------------------------------------\n")

    # Generate and save bar chart
    plt.figure(figsize=(10, 7))
    time_by_group.plot(kind='bar', color='coral')
    plt.title(f'Time Allocation by {main_group_col}')
    plt.xlabel(main_group_col)
    plt.ylabel('Total Duration (hours)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    chart_filename = f'time_allocation_by_{main_group_col.lower().replace(" ", "_")}.png'
    try:
        plt.savefig(chart_filename)
        print(f"Bar chart '{chart_filename}' saved successfully.")
    except Exception as e:
        print(f"Error saving time allocation chart: {e}")
    plt.close()

def analyze_time_trends(df, period='D'):
    """
    Analyzes daily or weekly time tracking trends and generates a line chart.
    """
    if df is None or df.empty:
        print("No data available for time trend analysis.")
        return

    trends_df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(trends_df['Date']):
        trends_df['Date'] = pd.to_datetime(trends_df['Date'], errors='coerce')
        trends_df.dropna(subset=['Date'], inplace=True)
        if trends_df.empty:
            print("No valid date data available for trend analysis after conversion.")
            return

    trends_df.set_index('Date', inplace=True)

    # Resample data
    # For weekly trends, 'W' defaults to 'W-SUN'. Use 'W-MON' for weeks starting Monday if desired.
    rule = 'W-MON' if period == 'W' else 'D'
    time_over_period = trends_df['Duration'].resample(rule).sum()

    if time_over_period.empty:
        print(f"No time data found for the {('Daily' if period == 'D' else 'Weekly')} trend analysis.")
        return

    print(f"\n--- {'Daily' if period == 'D' else 'Weekly'} Time Tracking Trends ---")
    print(time_over_period)
    print("---------------------------------------------------\n")

    # Generate and save line chart
    plt.figure(figsize=(12, 6))
    time_over_period.plot(kind='line', marker='o', linestyle='-', color='teal')
    period_name = 'Daily' if period == 'D' else 'Weekly'
    plt.title(f'{period_name} Time Tracked Over Period')
    plt.xlabel('Period Start Date' if period == 'W' else 'Date')
    plt.ylabel('Total Duration (hours)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()

    chart_filename = f'{period_name.lower()}_time_trend.png'
    try:
        plt.savefig(chart_filename)
        print(f"Line chart '{chart_filename}' saved successfully.")
    except Exception as e:
        print(f"Error saving {period_name.lower()} time trend chart: {e}")
    plt.close()

def main():
    """
    Main function to orchestrate the time tracking analysis.
    """
    parser = argparse.ArgumentParser(description="Time Tracking Analyzer")
    parser.add_argument("csv_file", help="Path to the CSV file containing time tracking data.")
    parser.add_argument("--group_by", default="Project", help="Column to group by for allocation analysis (e.g., Project, Task, Category). Default: Project")
    parser.add_argument("--trend_period", default="D", choices=['D', 'W'], help="Period for time trend analysis ('D' for daily, 'W' for weekly). Default: D")
    args = parser.parse_args()

    # Pass args.csv_file instead of args.csv_filepath
    df, project_col_name = load_time_data(args.csv_file)

    if df is None:
        print("Failed to load or validate time data. Exiting.")
        return # Or import sys; sys.exit(1)

    # Determine the actual grouping column to use
    actual_group_col = args.group_by
    if actual_group_col not in df.columns:
        print(f"Warning: Specified group_by column '{args.group_by}' not found. Defaulting to '{project_col_name}'.")
        actual_group_col = project_col_name
        # Ensure this default project_col_name itself exists (it should, due to load_time_data logic)
        if actual_group_col not in df.columns:
             print(f"Error: Default project column '{actual_group_col}' also not found. Cannot perform allocation analysis.")
             # Optionally skip this analysis or exit
        else:
            calculate_summary_stats(df)
            analyze_time_allocation(df, main_group_col=actual_group_col)
            analyze_time_trends(df, period=args.trend_period)
    else:
        calculate_summary_stats(df)
        analyze_time_allocation(df, main_group_col=actual_group_col)
        analyze_time_trends(df, period=args.trend_period)


if __name__ == "__main__":
    main()
