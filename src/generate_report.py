"""Generate a Word analysis report from output files created by main.py."""

from pathlib import Path
import csv
from docx import Document
from docx.shared import Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def read_csv_rows(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    doc = Document()
    title = doc.add_heading("Mall Customers – Spending Score Analysis", 0)
    title.alignment = 1
    doc.add_paragraph("Project code: PRCE-003")
    doc.add_paragraph("Technology: Python and PySpark")

    doc.add_heading("1. Objective", level=1)
    doc.add_paragraph(
        "The objective of this project is to load the Mall Customers dataset using "
        "PySpark and analyze customer behavior primarily on the basis of Spending Score."
    )

    doc.add_heading("2. Dataset and preparation", level=1)
    doc.add_paragraph(
        "The assignment dataset was obtained from the Google Drive link supplied in "
        "the project brief. The CSV was loaded with a header and inferred schema. "
        "Column names were standardized for easier processing. Review the notebook "
        "for the actual row count, schema, null values and duplicate count."
    )

    doc.add_heading("3. Spending Score analysis", level=1)
    rows = read_csv_rows(OUT / "spending_score_group_summary.csv")
    if rows:
        table = doc.add_table(rows=1, cols=3)
        table.style = "Light List Accent 1"
        for cell, label in zip(table.rows[0].cells, ["Spending Score group", "Customers", "Percentage"]):
            cell.text = label
        for row in rows:
            cells = table.add_row().cells
            cells[0].text = row.get("Spending_Group", "")
            cells[1].text = row.get("Customer_Count", "")
            cells[2].text = str(row.get("Percentage", ""))
    else:
        doc.add_paragraph(
            "Run main.py or the notebook to generate the spending group summary; "
            "then regenerate this report."
        )

    doc.add_paragraph(
        "Grouping rule used for descriptive interpretation: Low = 1–39, "
        "Medium = 40–60, High = 61–100. These are project-defined bands, not "
        "official classifications."
    )

    doc.add_heading("4. Interpretation and conclusion", level=1)
    doc.add_paragraph(
        "Use the summary table and charts to identify which spending-score group "
        "contains the largest share of customers. Discuss differences across "
        "available segments only where the dataset supports them. Spending Score "
        "is an assigned score in the dataset; it should not be interpreted as "
        "actual currency spent or as proof of causation."
    )
    doc.add_paragraph(
        "Complete this section after reviewing the actual results: state the key "
        "pattern, the largest group, and any meaningful segment differences."
    )

    doc.add_heading("5. Challenges faced", level=1)
    doc.add_paragraph("Document only the challenges that you personally encountered. Examples to verify:")
    for item in [
        "Accessing or downloading the dataset from Google Drive (if applicable).",
        "Configuring Java and PySpark correctly in the local VS Code environment (if applicable).",
        "Understanding and standardizing the dataset's column names and data types.",
        "Checking for missing values, duplicate records and unexpected Spending Score values.",
        "Interpreting score groups without treating descriptive bands as official labels."
    ]:
        doc.add_paragraph(item, style="List Bullet")
    doc.add_paragraph("Resolution: Describe how each actual challenge was resolved.")

    doc.add_heading("6. Tools used", level=1)
    doc.add_paragraph("Python, PySpark, Pandas, Matplotlib, and python-docx.")

    doc.add_heading("7. Submission checklist", level=1)
    doc.add_paragraph("Submit the completed .ipynb notebook and this reviewed Word report.")
    doc.save(REPORTS / "Mall_Customers_Analysis_Report.docx")
    print(f"Word report saved to: {REPORTS / 'Mall_Customers_Analysis_Report.docx'}")


if __name__ == "__main__":
    main()
