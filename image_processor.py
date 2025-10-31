from PIL import Image
import os
import sys

def process_images_in_folder(input_dir, output_format=None, new_size=None):
    """
    Processes all image files in a directory: converting format and/or resizing.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Directory not found at '{input_dir}'")
        return

    output_dir = os.path.join(input_dir, "processed_images")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    files_processed = 0

    print("-" * 50)
    print(f"Starting image processing in: {input_dir}")
    print(f"Output Format: {output_format if output_format else 'Original'}")
    print(f"New Size: {new_size if new_size else 'Original'}")
    print("-" * 50)

    for item_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, item_name)

        if os.path.isfile(input_path):
            try:
                # Open the image using Pillow
                img = Image.open(input_path)
                
                # Determine new file name and format
                base_name, ext = os.path.splitext(item_name)
                
                if output_format:
                    # Use the specified output format
                    save_format = output_format.upper().replace('.', '')
                    output_name = f"{base_name}.{output_format.lower()}"
                else:
                    # Keep original format
                    save_format = img.format 
                    output_name = item_name

                # 1. Handle Resizing
                if new_size and len(new_size) == 2:
                    print(f"  Resizing {item_name} to {new_size[0]}x{new_size[1]}...")
                    # Use ANTIALIAS for high-quality downsampling filter
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # 2. Save the processed image
                output_path = os.path.join(output_dir, output_name)
                img.save(output_path, format=save_format)
                
                print(f"  SUCCESS: {item_name} -> {output_name}")
                files_processed += 1
                
            except FileNotFoundError:
                continue # Skip if file disappeared
            except Exception as e:
                print(f"  ERROR processing {item_name}: {e}")

    print("-" * 50)
    print(f"Processing complete! Total images processed: {files_processed}")
    

if __name__ == "__main__":
    print("--- Bulk Image Processor (Converter & Resizer) ---")
    
    # Get user inputs
    input_dir = input("Enter the directory containing images: ").strip()
    out_format_str = input("Enter new format (e.g., png, jpg, or press Enter to skip): ").strip()
    size_str = input("Enter new dimensions (e.g., 800x600, or press Enter to skip): ").strip()

    # Parse inputs
    output_format = out_format_str.strip().lower() if out_format_str else None
    new_size = None
    if size_str and 'x' in size_str:
        try:
            w, h = map(int, size_str.lower().split('x'))
            new_size = (w, h)
        except ValueError:
            print("Invalid size format. Please use WxH (e.g., 800x600). Resizing skipped.")

    if input_dir:
        process_images_in_folder(input_dir, output_format, new_size)
    else:
        print("Input directory required. Exiting.")