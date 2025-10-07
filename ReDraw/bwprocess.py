import cv2
import numpy as np
import os

def improve_image_quality(input_image_path, output_image_path):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found.")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_thresh = cv2.adaptiveThreshold(
        gray_image, 
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        5,
        2
    )
    median_blurred = cv2.medianBlur(adaptive_thresh, 3)
    cv2.imwrite(output_image_path, median_blurred)
    print(f"Reduced Median Blurred Enhanced image saved to {output_image_path}")

def main():
    input_image_path = os.environ.get('INPUT_IMAGE_PATH')
    if input_image_path is None or not os.path.exists(input_image_path):
        raise ValueError("Input image path not found or invalid.")
    output_image_path = 'output/enhanced_image.jpg'
    improve_image_quality(input_image_path, output_image_path)

if __name__ == "__main__":
    main()
