import csv
import os

def merge_csv_files(input_files, output_file):
    """
    Merges multiple CSV files into a single output file.
    It assumes all CSVs have the same header row.
    """
    if not input_files:
        print("Error: No input files provided.")
        return

    # 1. Determine the header from the first file
    try:
        with open(input_files[0], 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_files[0]}")
        return
    except Exception as e:
        print(f"Error reading header from {input_files[0]}: {e}")
        return

    total_rows = 0
    
    # 2. Open the output file and write the data
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            
            # Write the header only once
            writer.writerow(header)
            
            # Process each input file
            for filename in input_files:
                try:
                    with open(filename, 'r', newline='', encoding='utf-8') as infile:
                        reader = csv.reader(infile)
                        # Skip the header row (already written)
                        next(reader, None) 
                        
                        # Write all data rows
                        for row in reader:
                            writer.writerow(row)
                            total_rows += 1
                    print(f"Successfully processed: {filename}")
                except FileNotFoundError:
                    print(f"Warning: Input file not found, skipping: {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    except Exception as e:
        print(f"Fatal Error writing to output file {output_file}: {e}")
        return

    print(f"\nMerge complete! {len(input_files)} files merged into {output_file}.")
    print(f"Total data rows written (excluding header): {total_rows}")


if __name__ == "__main__":
    # --- Example Usage ---
    print("CSV Merger Utility")
    
    # NOTE: User would need to have existing CSV files for this to run locally.
    # For demonstration, assume files named file1.csv and file2.csv exist.
    print("Please list the CSV files you want to merge (e.g., file1.csv,file2.csv):")
    
    input_str = input("Input CSV files (comma-separated): ").strip()
    if not input_str:
        print("No files specified. Exiting.")
    else:
        input_list = [f.strip() for f in input_str.split(',')]
        output_name = input("Enter the name for the merged output file (e.g., merged_data.csv): ").strip() or "merged_output.csv"
        
        merge_csv_files(input_list, output_name)