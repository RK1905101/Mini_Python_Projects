import cv2
import numpy as np

def enhance_color_image(input_image_path, output_image_path):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found.")

    denoised = cv2.bilateralFilter(image, d=9, sigmaColor=30, sigmaSpace=30)

    hsv = cv2.cvtColor(denoised, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.add(s, 20)
    s = np.clip(s, 0, 255)
    hsv_boosted = cv2.merge([h, s, v])
    color_boosted = cv2.cvtColor(hsv_boosted, cv2.COLOR_HSV2BGR)

    sharpening_kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    sharpened = cv2.filter2D(color_boosted, -1, sharpening_kernel)

    gamma = 1.5
    look_up_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in np.arange(256)]).astype("uint8")
    final_output = cv2.LUT(sharpened, look_up_table)

    cv2.imwrite(output_image_path, final_output)
    print(f"Enhanced color image saved to {output_image_path}")
