import fitz  # PyMuPDF is imported as 'fitz'
import os
import sys

def extract_pdf_data(pdf_path):
    """
    Extracts text and metadata from a PDF file.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        return

    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)

        # 1. Report Metadata
        metadata = doc.metadata
        print("-" * 60)
        print(f"PDF Analysis for: {os.path.basename(pdf_path)}")
        print(f"Total Pages: {doc.page_count}")
        print("-" * 60)
        print("METADATA:")
        for key, value in metadata.items():
             # Basic cleaning for output readability
            if value and key not in ['modDate', 'creationDate']:
                print(f"  {key.replace(':', '').title():<20}: {value}")
            
        print("-" * 60)

        # 2. Extract Text
        print("TEXT EXTRACTION (First 500 characters):")
        full_text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text += page.get_text("text") + "\n\n"
        
        # Display extracted text snippet
        print(full_text[:500].strip() + "...")
        print("-" * 60)
        
        # Optionally save the extracted text to a file
        text_output_name = os.path.splitext(pdf_path)[0] + "_extracted.txt"
        with open(text_output_name, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Successfully saved full text to: {text_output_name}")

    except Exception as e:
        print(f"An error occurred during PDF processing: {e}")
    finally:
        if 'doc' in locals() and doc:
            doc.close()

if __name__ == "__main__":
    print("--- Powerful PDF Text and Metadata Extractor ---")

    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
    else:
        pdf_file = input("Enter the path to the PDF file: ").strip()

    if pdf_file:
        # Ensure path is absolute or correct relative path
        if not os.path.isabs(pdf_file) and not os.path.exists(pdf_file):
             pdf_file = os.path.join(os.getcwd(), pdf_file)
        
        extract_pdf_data(pdf_file)
    else:
        print("No PDF file specified. Exiting.")