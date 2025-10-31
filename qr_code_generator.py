import qrcode
import os

def generate_qr_code(data, filename):
    """
    Generates a QR code from a string and saves it as a PNG file.
    
    Args:
        data (str): The text or URL to encode in the QR code.
        filename (str): The name for the output PNG file.
    """
    
    print(f"Generating QR code for data: '{data}'")
    
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Add the data to the instance
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image object
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save the image
        img.save(filename)
        
        print("-" * 40)
        print(f"Successfully created: {filename}")
        print(f"Path: {os.path.abspath(filename)}")
        print("-" * 40)

    except Exception as e:
        print(f"An error occurred during QR code generation: {e}")

if __name__ == "__main__":
    print("--- Simple QR Code Generator ---")
    
    # Get the data to encode from the user
    input_data = input("Enter the text or URL you want to encode: ").strip()
    
    if not input_data:
        print("No data entered. Exiting.")
    else:
        # Get the desired filename, ensuring it ends with .png
        default_filename = "qrcode_output.png"
        file_name = input(f"Enter output filename (default: {default_filename}): ").strip()
        
        if not file_name:
            file_name = default_filename
        elif not file_name.lower().endswith('.png'):
            file_name += '.png'
            
        generate_qr_code(input_data, file_name)