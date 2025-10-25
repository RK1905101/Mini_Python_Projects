import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import os
import argparse
from PIL import Image
from PIL.ExifTags import TAGS

def get_image_timestamp(image_path):
    """Optional: extract timestamp from image metadata"""
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "DateTime":
                    return value
    except:
        pass
    return None

def scan_folder(folder_path, output_format):
    data = []

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("No image files found in the folder.")
        return

    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        img = cv2.imread(img_path)
        qr_codes = decode(img)
        if qr_codes:
            for qr in qr_codes:
                qr_data = qr.data.decode('utf-8')
                timestamp = get_image_timestamp(img_path)
                data.append({
                    "filename": img_file,
                    "qr_data": qr_data,
                    "timestamp": timestamp
                })
            print(f"{img_file}: {len(qr_codes)} QR code(s) found")
        else:
            print(f"{img_file}: No QR codes found")

    if not data:
        print("No QR codes found in any images.")
        return

    os.makedirs("outputs", exist_ok=True)
    output_file = os.path.join("outputs", f"qr_catalog.{output_format}")

    df = pd.DataFrame(data)
    if output_format == "csv":
        df.to_csv(output_file, index=False)
    elif output_format == "json":
        df.to_json(output_file, orient="records", indent=4)
    else:
        print("Unsupported format. Use 'csv' or 'json'.")
        return

    print(f"\n✅ Catalog created: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Scan folder for QR codes and create a catalog.")
    parser.add_argument("folder_path", help="Path to the folder containing images")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Output format (default: csv)")
    args = parser.parse_args()

    scan_folder(args.folder_path, args.format)


if __name__ == "__main__":
    main()
