# Advanced Business Analytics and Mathematics (with Personal Data Analysis Scripts)

This repository initially contained a collection of Google Colab notebooks (2018-2023) focused on advanced business analytics and mathematics. It has now been expanded to include Python scripts for personal finance and time tracking data analysis.

If you have some ideas, get in touch, [@dereknow](https://twitter.com/dereknow?lang=en)

--------------------

## Personal Data Analysis Scripts

This section provides tools to analyze your personal finance and time tracking data from CSV files.

### 1. Personal Finance Analyzer (`personal_finance_analyzer.py`)

**Purpose:**
This script analyzes your personal finance data from a CSV file. It provides summary statistics, spending by category, and monthly financial trends.

**Input CSV Format:**
The script expects a CSV file with the following columns:
*   `Date`: The date of the transaction (e.g., `YYYY-MM-DD`).
*   `Description`: A brief description of the transaction.
*   `Amount`: The transaction amount. Positive values are treated as income, negative values as expenses.
*   `Category` (Optional): The category of the transaction (e.g., `Food`, `Salary`, `Utilities`). If missing or mostly empty, the script will attempt to infer categories based on keywords in the `Description`.

**Usage:**
```bash
python personal_finance_analyzer.py <your_finance_data.csv>
```
Replace `<your_finance_data.csv>` with the path to your CSV file.

**Output:**
*   **Console:**
    *   Summary statistics (Total Income, Total Expenses, Net Savings).
    *   Spending breakdown by category.
    *   Monthly income, expenses, and net savings.
*   **Files:**
    *   `spending_by_category.png`: A bar chart showing spending per category.
    *   `monthly_trends.png`: Line charts showing monthly income, expenses, and net savings over time.

**Example:**
An example input file `example_finance_data.csv` is provided. You can test the script with:
```bash
python personal_finance_analyzer.py example_finance_data.csv
```

### 2. Time Tracking Analyzer (`time_tracking_analyzer.py`)

**Purpose:**
This script analyzes your time tracking data from a CSV file. It provides summary statistics, time allocation by project/task/category, and daily/weekly time tracking trends.

**Input CSV Format:**
The script expects a CSV file with the following columns:
*   `Date`: The date of the time entry (e.g., `YYYY-MM-DD`).
*   `Project` or `Task`: The name of the project or task. The script will look for either column.
*   `Duration`: The time spent, as a numeric value in **hours** (e.g., `1.5` for 1 hour 30 minutes).
*   `Category` (Optional): A broader category for the time entry (e.g., `Work`, `Learning`).
*   `Notes` (Optional): Any additional notes.

**Usage:**
```bash
python time_tracking_analyzer.py <your_time_data.csv> [options]
```
Replace `<your_time_data.csv>` with the path to your CSV file.

**Options:**
*   `--group_by <column_name>`: Specify the column to group time allocation by (e.g., `Project`, `Category`). Defaults to `Project` (or `Task` if `Project` is not found).
*   `--trend_period <D_or_W>`: Set the trend analysis period. `D` for daily, `W` for weekly. Defaults to `D`.

**Output:**
*   **Console:**
    *   Summary statistics (Total time tracked, date range, average time per day).
    *   Time allocation breakdown by the specified grouping column.
    *   Time tracked per period (daily or weekly).
*   **Files (Filenames are dynamic based on options):**
    *   `time_allocation_by_<group_by_column>.png`: A bar chart showing time allocation.
    *   `<trend_period>_time_trend.png`: A line chart showing time tracked over the specified period (e.g., `daily_time_trend.png`).

**Example:**
An example input file `example_time_data.csv` is provided. You can test the script with:
```bash
python time_tracking_analyzer.py example_time_data.csv
# To group by Category and see weekly trends:
python time_tracking_analyzer.py example_time_data.csv --group_by Category --trend_period W
```

--------------------

### Original Colab Notebook Links (For Reference)
### Risk Engineering

#### Anomaly Detection
1. [Cross Sectional Multivariate Data](https://colab.research.google.com/drive/1rYcc05NI0MU5IReWgOADHr5R1J9kxnbW#scrollTo=whB7cEvdjC_M)
1. [Time Series Univariate](https://colab.research.google.com/drive/1rYcc05NI0MU5IReWgOADHr5R1J9kxnbW#scrollTo=5W0uuEqWMKBQ)
1. [Time Series Multi-variate Real Time](https://colab.research.google.com/drive/1rYcc05NI0MU5IReWgOADHr5R1J9kxnbW#scrollTo=yflg8pWYVoKp)
1. [Time Series Multi-variate](https://colab.research.google.com/drive/1rYcc05NI0MU5IReWgOADHr5R1J9kxnbW#scrollTo=yflg8pWYVoKp)
#### Predictive Maintenance
#### Financial Risk

### Decision Science

#### Causal Analysis 
1. [Causal Inference from Observational Data](https://drive.google.com/file/d/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2/view?usp=sharing)
    1. [Causal Regressions](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=lPGhJMFbH5BJ)
    1. [Uplift Modelling](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=WpXXNFbuIeWe)
1. [A/B Testing](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=593TzsMzVquj)
    1. [Frequentist](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=2w8-8ZMPCzT0)
    1. [Regression](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=hejyQQ-CS93j)
    1. [Bayesian](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=NSBBCs8QfUIL)
1. [Causal Discovery](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=SWM4ZLp4he6i)

#### Operations Research
1. Convex Optimisation
    1. [Optimal Advertising Problem](https://colab.research.google.com/drive/1qyiIt3JQpmQnzilVwQGU_G3b0_Rc2Xck)
1. [Linear Programming](https://drive.google.com/file/d/1l56ZmbDKez15vlAt8neGEZHYIagciRsI/view?usp=sharing)
    1. [Production Models with Linear Constraints](https://colab.research.google.com/drive/1l56ZmbDKez15vlAt8neGEZHYIagciRsI#scrollTo=SRXossXvecIC)
    1. [Linear Blending Problems](https://colab.research.google.com/drive/1l56ZmbDKez15vlAt8neGEZHYIagciRsI#scrollTo=J8jKI-LbfvQl)
    1. [Task Allocation Problems](https://colab.research.google.com/drive/1l56ZmbDKez15vlAt8neGEZHYIagciRsI#scrollTo=kV1GH1r13ix6)
    1. [Assignment and Scheduling](https://colab.research.google.com/drive/1KSewu262VvzPjgfq1Mgpv3t13WtBuzS_#scrollTo=ALeiPMX3Dulx)
1. [Multiple Criteria Decisions](https://colab.research.google.com/drive/1qA_xbKQl8xZH_oqXwjywkI8spiD2vgE2#scrollTo=SWM4ZLp4he6i)
    1. [TOPSIS](https://colab.research.google.com/drive/1KSewu262VvzPjgfq1Mgpv3t13WtBuzS_#scrollTo=cPLWJzdU9N3v)
    1. [SKCriteria](https://colab.research.google.com/drive/1KSewu262VvzPjgfq1Mgpv3t13WtBuzS_#scrollTo=JRmRHMlxYLVD)
    1. [Goal Programming](https://colab.research.google.com/drive/1KSewu262VvzPjgfq1Mgpv3t13WtBuzS_#scrollTo=ALeiPMX3Dulx)


### Predictive Analytics

#### Employee
#### Customer

### Segmentation Research

#### Clustering Problems
