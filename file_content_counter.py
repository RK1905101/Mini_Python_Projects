import os
import sys

def count_file_contents(file_path):
    """
    Counts the number of lines, words, and characters in a text file.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return

    try:
        # Using 'r' for read mode and 'utf-8' for broad compatibility
        with open(file_path, 'r', encoding='utf-8') as f:
            line_count = 0
            word_count = 0
            char_count = 0
            
            for line in f:
                # 1. Count Lines: Each iteration is a new line
                line_count += 1
                
                # 2. Count Characters: Includes spaces and newline characters
                char_count += len(line)
                
                # 3. Count Words: Split the line and count the resulting items
                words = line.split()
                word_count += len(words)

            print(f"\n--- Analysis for '{os.path.basename(file_path)}' ---")
            print(f"Lines:        {line_count}")
            print(f"Words:        {word_count}")
            print(f"Characters:   {char_count}")
            print("---------------------------------------")

    except UnicodeDecodeError:
        print("Error: Cannot read file. It might be a binary file, or the encoding is not UTF-8.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Check if a filename was passed as a command-line argument
    if len(sys.argv) < 2:
        # Prompt the user if no argument was provided
        file_to_analyze = input("Enter the path to the file you want to analyze: ").strip()
        if not file_to_analyze:
            print("No file specified. Exiting.")
            sys.exit(1)
        count_file_contents(file_to_analyze)
    else:
        # Use the first command-line argument as the file path
        count_file_contents(sys.argv[1])