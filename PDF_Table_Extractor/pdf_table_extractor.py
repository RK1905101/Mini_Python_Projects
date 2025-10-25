import pdfplumber
import pandas as pd
import argparse
import os

def extract_tables(pdf_path, output_format):
    if not os.path.exists(pdf_path):
        print("❌ File not found. Please check the path.")
        return

    tables_extracted = 0
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    df = pd.DataFrame(table[1:], columns=table[0])  # First row as header
                    all_tables.append(df)
                    tables_extracted += 1
            else:
                print(f"⚠️ No tables found on page {i}")

    if not all_tables:
        print("❌ No tables found in the entire PDF.")
        return

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    for idx, df in enumerate(all_tables, start=1):
        output_file = os.path.join(output_dir, f"table_{idx}.{output_format}")

        if output_format == "csv":
            df.to_csv(output_file, index=False)
        elif output_format in ["xlsx", "xls"]:
            df.to_excel(output_file, index=False)
        else:
            print("❌ Unsupported format. Use 'csv' or 'xlsx'.")
            return

    print(f"✅ Extracted {tables_extracted} table(s). Files saved in '{output_dir}/' folder.")


def main():
    parser = argparse.ArgumentParser(description="Extract tables from a PDF and export as CSV or Excel.")
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument("--format", choices=["csv", "xlsx"], default="csv", help="Output format (default: csv).")

    args = parser.parse_args()
    extract_tables(args.pdf_path, args.format)


if __name__ == "__main__":
    main()
