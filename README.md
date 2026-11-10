# PRCE-003: Mall Customers Analysis (PySpark)

This project follows the supplied assignment brief:
1. Load the Mall Customers data using PySpark.
2. Write an analysis report based on the Spending Score.
3. Document challenges faced.
4. Submit the `.ipynb` notebook and Word analysis report.

## Project files
- `notebooks/PRCE_003_Mall_Customers_Analysis.ipynb` — complete, step-by-step notebook.
- `src/mall_analysis.py` — reusable PySpark analysis functions.
- `main.py` — run the analysis from the VS Code terminal.
- `reports/` — generated Word report is saved here after running.
- `data/raw/` — downloaded CSV dataset location.
- `output/` — summary CSV files and charts.

## Requirements
- Windows 10/11
- Python 3.10 or 3.11 (recommended)
- Java JDK 17
- VS Code + Microsoft Python extension + Jupyter extension

## Setup in VS Code (PowerShell)
Open this extracted project folder in VS Code, then Terminal > New Terminal:

```powershell
python --version
java -version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this in the current terminal, then activate again:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

In VS Code press `Ctrl+Shift+P` > `Python: Select Interpreter` > choose `.venv`.

## Get the assignment dataset
The assignment's Google Drive file is:
https://drive.google.com/file/d/1k6A8r1cCdt0Ft0mPtvnYckruaTn2XXz0/view?usp=share_link

The project includes a downloader that attempts to retrieve that file. If access is restricted, open the link in your browser, download the CSV manually, and save it as:
`data/raw/Mall_Customers.csv`

Make sure the Google Drive sharing permission allows you to view/download the file.

## Run from terminal
```powershell
python main.py
```

## Run the notebook
1. Open `notebooks/PRCE_003_Mall_Customers_Analysis.ipynb` in VS Code.
2. Select the `.venv` Python kernel.
3. Run cells from top to bottom.

## What the analysis calculates
- Dataset shape, schema, nulls and duplicates
- Spending Score mean, median, standard deviation, minimum and maximum
- Low / Medium / High Spending Score groups (rule-based bands: 1–39, 40–60, 61–100)
- Counts and percentages in each score band
- Spending Score comparisons by gender and age group, where those columns exist
- Annual Income vs Spending Score relationship, where the column exists
- Charts and CSV summaries

The Low / Medium / High bands are descriptive categories for this assignment, not official labels or clinical/statistical standards. Interpret results using the dataset actually downloaded. Do not assume that one demographic group causes another group's spending behavior.

## Outputs
- `output/spending_score_distribution.png`
- `output/spending_score_groups.png`
- `output/average_spending_by_gender.png` (if Gender exists)
- `output/income_vs_spending_score.png` (if Annual Income exists)
- `output/spending_score_group_summary.csv`
- `reports/Mall_Customers_Analysis_Report.docx`

The Word report is generated from the actual run results. Review it and complete the Challenges Faced section with any issues you personally encountered before submission.
