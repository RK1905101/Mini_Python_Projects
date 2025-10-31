import hashlib
import os
import sys

def calculate_hash(file_path, hash_algorithm='sha256', block_size=65536):
    """
    Calculates the cryptographic hash (e.g., SHA-256) of a file efficiently.
    
    Reads the file in blocks to handle very large files without running out of memory.
    """
    if not os.path.exists(file_path):
        return None

    try:
        # Initialize the hasher object (defaulting to SHA-256)
        hasher = hashlib.new(hash_algorithm)
    except ValueError:
        print(f"Error: Unknown hash algorithm '{hash_algorithm}'. Using sha256.")
        hasher = hashlib.sha256()

    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as f:
            while True:
                # Read data in chunks
                data = f.read(block_size)
                if not data:
                    break
                # Update the hash object with the data chunk
                hasher.update(data)

        # Return the hexadecimal representation of the hash
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return None


def verify_file(file_path):
    """
    Calculates the file's hash and prompts the user to verify against an expected hash.
    """
    print("-" * 50)
    print(f"Analyzing file: {os.path.basename(file_path)}")
    
    # 1. Calculate the actual hash
    actual_hash = calculate_hash(file_path)
    
    if not actual_hash:
        print("Verification failed: Could not generate hash.")
        return

    print(f"Calculated SHA-256 Hash: {actual_hash}")
    print("-" * 50)
    
    # 2. Prompt for verification
    expected_hash = input("Enter the expected hash (or press Enter to skip verification): ").strip().lower()
    
    if expected_hash:
        if actual_hash == expected_hash:
            print("\n✅ SUCCESS: The file hash MATCHES the expected hash. Integrity verified!")
        else:
            print("\n❌ FAILURE: The file hash DOES NOT MATCH the expected hash. File integrity compromised!")
    else:
        print("\nVerification skipped. Hash calculated successfully.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Prompt the user if no filename was provided
        file_to_check = input("Enter the path to the file you want to check: ").strip()
        if not file_to_check:
            print("No file specified. Exiting.")
            sys.exit(1)
        
        # Check if file exists in current directory if path is not absolute
        if not os.path.isabs(file_to_check) and not os.path.exists(file_to_check):
             file_to_check = os.path.join(os.getcwd(), file_to_check)
        
        verify_file(file_to_check)
    else:
        # Use the first command-line argument as the file path
        verify_file(sys.argv[1])